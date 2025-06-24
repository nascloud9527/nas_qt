from PySide6.QtCore import QObject, Signal, Slot, Property
from api.upload_api import UploadAPI
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class UploadViewModel(QObject):
    """文件上传ViewModel，专门处理文件上传相关功能"""
    
    # 信号定义
    uploadProgressChanged = Signal(int)  # 上传进度信号
    uploadFinished = Signal(bool, str)  # 上传完成信号 (success, message)
    uploadStarted = Signal(str)  # 上传开始信号 (file_name)
    uploadCancelled = Signal()  # 上传取消信号
    
    def __init__(self):
        super().__init__()
        self._upload_api = UploadAPI()
        self._upload_progress = 0
        self._is_uploading = False
        self._current_upload_file = ""
        self._current_directory = ""
        self._upload_queue = []  # 上传队列
        self._current_upload_index = -1
    
    @Slot(str)
    def set_token(self, token: str):
        """设置认证 token"""
        self._upload_api.set_token(token)
    
    @Slot(str)
    def set_current_directory(self, directory: str):
        """设置当前上传目录"""
        self._current_directory = directory
    
    @Slot(str)
    def upload_file(self, file_path: str):
        """上传单个文件到当前目录"""
        # 首先验证文件
        validation_result = self._upload_api.validate_file(file_path)
        if not validation_result["valid"]:
            self.uploadFinished.emit(False, validation_result["error"])
            return
        
        self._is_uploading = True
        self._upload_progress = 0
        self._current_upload_file = os.path.basename(file_path)
        self.uploadProgressChanged.emit(0)
        self.uploadStarted.emit(self._current_upload_file)
        
        # 定义进度回调函数
        def progress_callback(progress):
            self._upload_progress = progress
            self.uploadProgressChanged.emit(progress)
        
        # 调用上传API
        result = self._upload_api.upload_file_with_progress(
            file_path, 
            self._current_directory,
            progress_callback
        )
        
        if result["success"]:
            self._upload_progress = 100
            self.uploadProgressChanged.emit(100)
            self.uploadFinished.emit(True, f"文件 '{self._current_upload_file}' 上传成功")
        else:
            error_msg = result.get("error", "上传失败")
            self.uploadFinished.emit(False, f"文件 '{self._current_upload_file}' 上传失败: {error_msg}")
        
        self._is_uploading = False
        self._current_upload_file = ""
        self.uploadProgressChanged.emit(0)  # 重置进度
    
    @Slot()
    def select_file_for_upload(self):
        """选择文件进行上传"""
        from PySide6.QtWidgets import QFileDialog, QApplication
        
        # 获取当前应用实例
        app = QApplication.instance()
        if not app:
            self.uploadFinished.emit(False, "无法获取应用程序实例")
            return
        
        # 打开文件选择对话框
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "选择要上传的文件",
            "",
            "所有文件 (*.*)"
        )
        
        if file_path:
            self.upload_file(file_path)
    
    @Slot()
    def select_multiple_files_for_upload(self):
        """选择多个文件进行上传"""
        from PySide6.QtWidgets import QFileDialog, QApplication
        
        # 获取当前应用实例
        app = QApplication.instance()
        if not app:
            self.uploadFinished.emit(False, "无法获取应用程序实例")
            return
        
        # 打开多文件选择对话框
        file_paths, _ = QFileDialog.getOpenFileNames(
            None,
            "选择要上传的文件",
            "",
            "所有文件 (*.*)"
        )
        
        if file_paths:
            self.add_files_to_upload_queue(file_paths)
    
    @Slot(list)
    def add_files_to_upload_queue(self, file_paths: list):
        """添加文件到上传队列"""
        for file_path in file_paths:
            if file_path not in self._upload_queue:
                self._upload_queue.append(file_path)
        
        # 如果当前没有在上传，开始上传队列
        if not self._is_uploading:
            self.start_upload_queue()
    
    @Slot()
    def start_upload_queue(self):
        """开始上传队列中的文件"""
        if not self._upload_queue or self._is_uploading:
            return
        
        self._current_upload_index = 0
        self.upload_next_file()
    
    def upload_next_file(self):
        """上传队列中的下一个文件"""
        if self._current_upload_index >= len(self._upload_queue):
            # 队列完成
            self._upload_queue.clear()
            self._current_upload_index = -1
            return
        
        file_path = self._upload_queue[self._current_upload_index]
        self.upload_file(file_path)
    
    @Slot()
    def cancel_current_upload(self):
        """取消当前上传"""
        if self._is_uploading:
            self._is_uploading = False
            self._current_upload_file = ""
            self.uploadCancelled.emit()
            self.uploadProgressChanged.emit(0)
    
    @Slot()
    def clear_upload_queue(self):
        """清空上传队列"""
        self._upload_queue.clear()
        self._current_upload_index = -1
        if self._is_uploading:
            self.cancel_current_upload()
    
    @Slot(str)
    def remove_file_from_queue(self, file_path: str):
        """从上传队列中移除指定文件"""
        if file_path in self._upload_queue:
            index = self._upload_queue.index(file_path)
            self._upload_queue.pop(index)
            
            # 如果移除的是当前正在上传的文件，取消上传
            if index == self._current_upload_index and self._is_uploading:
                self.cancel_current_upload()
            # 如果移除的文件在当前文件之前，调整索引
            elif index < self._current_upload_index:
                self._current_upload_index -= 1
    
    def on_upload_finished(self, success: bool, message: str):
        """上传完成后的处理"""
        if success and self._current_upload_index >= 0:
            # 上传成功，继续下一个文件
            self._current_upload_index += 1
            self.upload_next_file()
    
    @Slot(str)
    def upload_file_with_callback(self, file_path: str, on_finished=None):
        """上传文件并执行回调"""
        # 首先验证文件
        validation_result = self._upload_api.validate_file(file_path)
        if not validation_result["valid"]:
            if on_finished:
                on_finished(False, validation_result["error"])
            return
        
        self._is_uploading = True
        self._upload_progress = 0
        self._current_upload_file = os.path.basename(file_path)
        self.uploadProgressChanged.emit(0)
        self.uploadStarted.emit(self._current_upload_file)
        
        # 定义进度回调函数
        def progress_callback(progress):
            self._upload_progress = progress
            self.uploadProgressChanged.emit(progress)
        
        # 调用上传API
        result = self._upload_api.upload_file_with_progress(
            file_path, 
            self._current_directory,
            progress_callback
        )
        
        if result["success"]:
            self._upload_progress = 100
            self.uploadProgressChanged.emit(100)
            success_message = f"文件 '{self._current_upload_file}' 上传成功"
            self.uploadFinished.emit(True, success_message)
            if on_finished:
                on_finished(True, success_message)
        else:
            error_msg = result.get("error", "上传失败")
            error_message = f"文件 '{self._current_upload_file}' 上传失败: {error_msg}"
            self.uploadFinished.emit(False, error_message)
            if on_finished:
                on_finished(False, error_message)
        
        self._is_uploading = False
        self._current_upload_file = ""
        self.uploadProgressChanged.emit(0)  # 重置进度
    
    # 属性定义
    @Property(int, notify=uploadProgressChanged)
    def upload_progress(self):
        """上传进度百分比"""
        return self._upload_progress
    
    @Property(bool, notify=uploadProgressChanged)
    def is_uploading(self):
        """是否正在上传"""
        return self._is_uploading
    
    @Property(str, notify=uploadStarted)
    def current_upload_file(self):
        """当前正在上传的文件名"""
        return self._current_upload_file
    
    @Property(list, notify=uploadProgressChanged)
    def upload_queue(self):
        """上传队列"""
        return self._upload_queue.copy()
    
    @Property(int, notify=uploadProgressChanged)
    def queue_progress(self):
        """队列进度（当前文件索引/总文件数）"""
        if not self._upload_queue:
            return 0
        return self._current_upload_index + 1 if self._current_upload_index >= 0 else 0
    
    @Property(int, notify=uploadProgressChanged)
    def queue_total(self):
        """队列总文件数"""
        return len(self._upload_queue) 