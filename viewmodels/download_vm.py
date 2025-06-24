from PySide6.QtCore import QObject, Signal, Slot, Property
from api.download_api import DownloadAPI
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class DownloadViewModel(QObject):
    """文件下载ViewModel，处理文件下载相关功能"""
    
    # 信号定义
    downloadProgressChanged = Signal(int)  # 下载进度信号 (progress)
    downloadFinished = Signal(bool, str)  # 下载完成信号 (success, message)
    downloadStarted = Signal(str)  # 下载开始信号 (file_name)
    downloadCancelled = Signal()  # 下载取消信号
    
    def __init__(self):
        super().__init__()
        self._download_api = DownloadAPI()
        self._download_progress = 0
        self._is_downloading = False
        self._current_download_file = ""
        self._download_queue = []  # 下载队列
        self._current_download_index = -1
        # 使用用户主目录下的Downloads文件夹作为默认保存目录
        self._default_save_dir = os.path.expanduser("~/Downloads")
        
        # 确保默认保存目录存在
        try:
            os.makedirs(self._default_save_dir, exist_ok=True)
        except PermissionError:
            # 如果无法创建Downloads目录，使用当前工作目录
            self._default_save_dir = os.getcwd()
    
    @Slot(str)
    def set_token(self, token: str):
        """设置认证 token"""
        self._download_api.set_token(token)
    
    @Slot(str, str)
    @Slot(str)
    def download_file(self, relpath: str, save_path: str = None):
        """下载单个文件"""
        if not relpath:
            self.downloadFinished.emit(False, "文件路径不能为空")
            return
        
        filename = os.path.basename(relpath)
        
        # 如果没有提供保存路径，使用默认路径
        if save_path is None:
            save_path = os.path.join(self._default_save_dir, filename)
        
        self._perform_download(relpath, save_path)

    def _perform_download(self, relpath: str, save_path: str):
        """执行实际的下载操作"""
        self._is_downloading = True
        self._download_progress = 0
        self._current_download_file = os.path.basename(relpath)
        self.downloadProgressChanged.emit(0)
        self.downloadStarted.emit(self._current_download_file)
        
        # 确保目录存在
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # 调用下载API
        result = self._download_api.download_file(relpath, save_path)
        
        if result["success"]:
            self._download_progress = 100
            self.downloadProgressChanged.emit(100)
            self.downloadFinished.emit(True, f"文件 '{self._current_download_file}' 下载成功到 {save_path}")
        else:
            error_msg = result.get("error", "下载失败")
            self.downloadFinished.emit(False, f"文件 '{self._current_download_file}' 下载失败: {error_msg}")
        
        self._is_downloading = False
        self._current_download_file = ""
        self.downloadProgressChanged.emit(0)  # 重置进度
    
    @Slot(list, str)
    @Slot(list) 
    def download_multiple_files(self, file_list: list, target_dir: str = None):
        """下载多个文件"""
        if not file_list:
            self.downloadFinished.emit(False, "没有选择要下载的文件")
            return
        
        # 如果没有提供目标目录，使用默认目录
        if target_dir is None:
            target_dir = self._default_save_dir
        
        # 确保目标目录存在
        os.makedirs(target_dir, exist_ok=True)
        
        # 将文件添加到下载队列
        for file_info in file_list:
            relpath = file_info.get("relPath", "")
            if relpath and not file_info.get("isDir", False):
                save_path = os.path.join(target_dir, os.path.basename(relpath))
                self._download_queue.append((relpath, save_path))
        
        if not self._is_downloading:
            self.start_download_queue()
    
    @Slot(str)
    def set_default_save_directory(self, directory: str):
        """设置默认保存目录"""
        if directory and os.path.exists(directory):
            self._default_save_dir = directory
            # 确保目录存在
            os.makedirs(self._default_save_dir, exist_ok=True)
    
    @Slot()
    def start_download_queue(self):
        """开始下载队列中的文件"""
        if not self._download_queue or self._is_downloading:
            return
        
        self._current_download_index = 0
        self.download_next_file()
    
    def download_next_file(self):
        """下载队列中的下一个文件"""
        if self._current_download_index >= len(self._download_queue):
            # 队列完成
            self._download_queue.clear()
            self._current_download_index = -1
            return
        
        relpath, save_path = self._download_queue[self._current_download_index]
        self._perform_download(relpath, save_path)
    
    @Slot()
    def cancel_current_download(self):
        """取消当前下载"""
        if self._is_downloading:
            self._is_downloading = False
            self._current_download_file = ""
            self.downloadCancelled.emit()
            self.downloadProgressChanged.emit(0)
    
    @Slot()
    def clear_download_queue(self):
        """清空下载队列"""
        self._download_queue.clear()
        self._current_download_index = -1
        if self._is_downloading:
            self.cancel_current_download()
    
    @Slot(str)
    def remove_file_from_queue(self, file_path: str):
        """从下载队列中移除指定文件"""
        for i, (relpath, _) in enumerate(self._download_queue):
            if relpath == file_path:
                self._download_queue.pop(i)
                
                # 如果移除的是当前正在下载的文件，取消下载
                if i == self._current_download_index and self._is_downloading:
                    self.cancel_current_download()
                # 如果移除的文件在当前文件之前，调整索引
                elif i < self._current_download_index:
                    self._current_download_index -= 1
                break
    
    def on_download_finished(self, success: bool, message: str):
        """下载完成后的处理"""
        if success and self._current_download_index >= 0:
            # 下载成功，继续下一个文件
            self._current_download_index += 1
            self.download_next_file()
    
    # 属性定义
    @Property(int, notify=downloadProgressChanged)
    def download_progress(self):
        """下载进度百分比"""
        return self._download_progress
    
    @Property(bool, notify=downloadProgressChanged)
    def is_downloading(self):
        """是否正在下载"""
        return self._is_downloading
    
    @Property(str, notify=downloadStarted)
    def current_download_file(self):
        """当前正在下载的文件名"""
        return self._current_download_file
    
    @Property(list, notify=downloadProgressChanged)
    def download_queue(self):
        """下载队列"""
        return [relpath for relpath, _ in self._download_queue]
    
    @Property(int, notify=downloadProgressChanged)
    def queue_progress(self):
        """队列进度（当前文件索引/总文件数）"""
        if not self._download_queue:
            return 0
        return self._current_download_index + 1 if self._current_download_index >= 0 else 0
    
    @Property(int, notify=downloadProgressChanged)
    def queue_total(self):
        """队列总文件数"""
        return len(self._download_queue)
    
    @Property(str)
    def default_save_directory(self):
        """默认保存目录"""
        return self._default_save_dir