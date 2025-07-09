from PySide6.QtCore import QObject, Signal, Slot, Property
from api.file_api import FileAPI
from viewmodels.upload_vm import UploadViewModel
# from vlc_player import MyVLCPlayer
import subprocess
import platform
import os
import sys

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import config

class FileViewModel(QObject):
    fileListChanged = Signal()
    loadingChanged = Signal()
    errorChanged = Signal()
    fileOpened = Signal(str)  # 文件打开信号
    directoryChanged = Signal(str)  # 目录改变信号
    contextMenuRequested = Signal(int, int, int)  # 右键菜单信号 (x, y, index)
    createFolderFinished = Signal(bool, str)  # 创建文件夹完成信号 (success, message)
    creatingFolderChanged = Signal()  # 创建文件夹状态变化信号
    showCreateFolderDialogRequested = Signal()  # 显示创建文件夹对话框信号
    
    def __init__(self):
        super().__init__()
        self._file_api = FileAPI()
        self._upload_vm = UploadViewModel()  # 新增上传ViewModel实例
        
        # 连接上传ViewModel的信号
        self._upload_vm.uploadProgressChanged.connect(self._on_upload_progress_changed)
        self._upload_vm.uploadFinished.connect(self._on_upload_finished)
        self._upload_vm.uploadStarted.connect(self._on_upload_started)
        self._upload_vm.uploadCancelled.connect(self._on_upload_cancelled)
        
        self._file_list = []
        self._current_directory = ""
        self._current_username = ""  # 当前登录的用户名
        self._is_loading = False
        self._error_message = ""
        self._is_creating_folder = False
    
    @Slot(str)
    def set_token(self, token: str):
        """设置认证 token"""
        self._file_api.set_token(token)
        self._upload_vm.set_token(token)  # 同时设置上传ViewModel的token
    
    @Slot(str)
    def set_username(self, username: str):
        """设置当前登录的用户名"""
        self._current_username = username
    
    @Slot(str)
    def load_file_list(self, directory: str = ""):
        """加载文件列表"""
        self._is_loading = True
        self._error_message = ""
        self.loadingChanged.emit()
        self.errorChanged.emit()
        
        # # 如果没有指定目录，使用用户名作为默认目录
        # if not directory and self._current_username:
        #     directory = self._current_username
        if not directory and self._current_username == "admin":
            directory = self._current_username
        
        # 调用 API 获取文件列表
        result = self._file_api.get_file_list(directory)
        
        if result["success"]:
            self._current_directory = directory
            self._upload_vm.set_current_directory(directory)  # 同步设置上传目录
            files_data = result["data"].get("files", []) if result["data"] else []
            
            # 转换文件数据格式
            self._file_list = []
            if files_data:
                for file_data in files_data:
                    if file_data:  # 确保file_data不为None
                        transformed_file = self._file_api.transform_file_data(file_data)
                        self._file_list.append(transformed_file)
            
            self._error_message = ""
        else:
            self._error_message = result.get("error", "获取文件列表失败")
            self._file_list = []
        
        # 确保_file_list永远不会是None
        if self._file_list is None:
            self._file_list = []
        
        self._is_loading = False
        self.fileListChanged.emit()
        self.loadingChanged.emit()
        self.errorChanged.emit()
    
    @Slot()
    def refresh_file_list(self):
        """刷新当前目录的文件列表"""
        self.load_file_list(self._current_directory)
    
    @Slot(int, bool)
    def toggle_file_selection(self, index: int, selected: bool):
        """切换文件选择状态"""
        if self._file_list and 0 <= index < len(self._file_list):
            old_selected = self._file_list[index].get("selected", False)
            if old_selected != selected:
                self._file_list[index]["selected"] = selected
                self.fileListChanged.emit()
    
    @Slot(bool)
    def select_all_files(self, selected: bool):
        """全选/取消全选文件"""
        if self._file_list:
            changed = False
            for file_item in self._file_list:
                if file_item.get("selected", False) != selected:
                    file_item["selected"] = selected
                    changed = True
            
            if changed:
                self.fileListChanged.emit()
    
    @Slot(result=list)  # 显式声明返回类型为 list
    def get_selected_files(self):
        """获取选中的文件列表"""
        if not self._file_list:
            return []
            
        return [file_item for file_item in self._file_list if file_item.get("selected", False)]
    
    @Slot(int)
    def open_file_or_folder(self, index: int):
        """打开文件或进入文件夹（双击）"""
        if self._file_list and 0 <= index < len(self._file_list):
            file_item = self._file_list[index]
            
            if file_item.get("isDir", False):
                # 如果是文件夹，进入该文件夹
                new_directory = file_item.get("relPath", "")
                if new_directory:
                    self.load_file_list(new_directory)
                    self.directoryChanged.emit(new_directory)
            else:
                # 如果是文件，发出文件打开信号并尝试打开文件
                file_path = file_item.get("relPath", "")
                if file_path:
                    self.fileOpened.emit(file_path)
                    self.open_file_with_system(file_path)
    
    @Slot(str)
    def open_file_with_system(self, relative_path: str):
        """使用系统默认程序打开文件；若为视频则调用系统 ffplay 播放"""
        try:
            full_path = config.get_full_file_path(relative_path)
            print(f"尝试打开文件: {full_path}")

            if not os.path.exists(full_path):
                print(f"文件不存在: {full_path}")
                return

            # 根据扩展名判断是否为视频
            ext = os.path.splitext(full_path)[-1].lower().strip(".")
            video_exts = ["mp4", "avi", "mov", "wmv", "flv", "mkv", "webm"]

            if ext in video_exts:
                # 用系统全局 ffplay
                try:
                    subprocess.Popen(["ffplay", full_path])
                except FileNotFoundError:
                    print("ffplay 未安装，改用系统默认打开")
                    subprocess.run(["xdg-open", full_path], check=True)
                return

            # 非视频，系统默认打开
            subprocess.run(["xdg-open", full_path], check=True)

        except Exception as e:
            print(f"无法打开文件 {relative_path}: {e}")

    @Slot()
    def go_to_parent_directory(self):
        """返回上一级目录"""
        # 主页就是用户名
        if self._current_directory == self._current_username or not self._current_directory:
            return  # 已经在主页或根目录
        parent_directory = self._file_api.get_parent_directory(self._current_directory)
        self.load_file_list(parent_directory)
        self.directoryChanged.emit(parent_directory)
    
    @Slot()
    def can_go_to_parent(self) -> bool:
        """检查是否可以返回上一级目录"""
        return bool(self._current_directory)
    
    @Slot(int, int, int)
    def show_context_menu(self, x: int, y: int, index: int):
        """显示右键菜单"""
        self.contextMenuRequested.emit(x, y, index)
    
    @Slot(int, bool)
    def select_file(self, index: int, ctrl_key_pressed: bool = False):
        """选中文件（单击）- 根据Ctrl键状态决定选择行为"""
        if self._file_list and 0 <= index < len(self._file_list):
            if ctrl_key_pressed:
                # 按住Ctrl键：切换当前文件的选中状态，不影响其他文件
                self._file_list[index]["selected"] = not self._file_list[index].get("selected", False)
            else:
                # 没有按Ctrl键：检查当前文件是否已经选中
                current_selected = self._file_list[index].get("selected", False)
                if current_selected:
                    # 如果当前文件已经选中，则取消选中
                    self._file_list[index]["selected"] = False
                else:
                    # 如果当前文件未选中，则取消其他文件的选中状态，只选中当前文件
                    for i, file_item in enumerate(self._file_list):
                        self._file_list[i]["selected"] = (i == index)
            
            self.fileListChanged.emit()
    @Slot(str)
    def create_folder(self, folder_name: str):
        """创建文件夹"""
        if not folder_name or not folder_name.strip():
            self.createFolderFinished.emit(False, "文件夹名称不能为空")
            return
        
        folder_name = folder_name.strip()
        
        # 检查文件夹名称是否包含非法字符
        invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        for char in invalid_chars:
            if char in folder_name:
                self.createFolderFinished.emit(False, f"文件夹名称不能包含字符: {char}")
                return
        
        self._is_creating_folder = True
        self.creatingFolderChanged.emit()
        
        # 调用API创建文件夹
        result = self._file_api.create_directory(
            root_dir="",  # 用户目录
            cur_dir=self._current_directory,
            name=folder_name
        )
        
        if result["success"]:
            self.createFolderFinished.emit(True, f"文件夹 '{folder_name}' 创建成功")
            # 创建成功后刷新文件列表
            self.refresh_file_list()
        else:
            error_msg = result.get("error", "创建文件夹失败")
            self.createFolderFinished.emit(False, error_msg)
        
        self._is_creating_folder = False
        self.creatingFolderChanged.emit()
    
    @Slot()
    def show_create_folder_dialog(self):
        """显示创建文件夹对话框"""
        # 使用QML对话框而不是QInputDialog
        # 这个方法将在QML中调用，所以我们需要发出一个信号
        # 让QML层处理对话框的显示
        self.showCreateFolderDialogRequested.emit()
    
    # 上传相关的方法委托给UploadViewModel
    @Slot(str)
    def upload_file(self, file_path: str):
        """上传文件到当前目录"""
        self._upload_vm.upload_file(file_path)
    
    @Slot()
    def select_file_for_upload(self):
        """选择文件进行上传"""
        self._upload_vm.select_file_for_upload()
    
    @Slot()
    def select_multiple_files_for_upload(self):
        """选择多个文件进行上传"""
        self._upload_vm.select_multiple_files_for_upload()
    
    @Slot()
    def cancel_current_upload(self):
        """取消当前上传"""
        self._upload_vm.cancel_current_upload()
    
    @Slot()
    def clear_upload_queue(self):
        """清空上传队列"""
        self._upload_vm.clear_upload_queue()
    
    # 属性定义
    @Property(bool, notify=creatingFolderChanged)
    def is_creating_folder(self):
        return self._is_creating_folder
    
    @Property(list, notify=fileListChanged)
    def file_list(self):
        return self._file_list if self._file_list is not None else []
    
    @Property(str, notify=fileListChanged)
    def current_directory(self):
        return self._current_directory
    
    @Property(bool, notify=loadingChanged)
    def is_loading(self):
        return self._is_loading
    
    @Property(str, notify=errorChanged)
    def error_message(self):
        return self._error_message
    
    @Property(bool, notify=fileListChanged)
    def is_at_home(self):
        return self._current_directory == self._current_username or not self._current_directory
    
    @Property(bool, notify=fileListChanged)
    def all_files_selected(self):
        """是否所有文件都被选中"""
        if not self._file_list:
            return False
        return all(file_item.get("selected", False) for file_item in self._file_list)
    
    @Property(bool, notify=fileListChanged)
    def some_files_selected(self):
        """是否有部分文件被选中"""
        if not self._file_list:
            return False
        selected_count = sum(1 for file_item in self._file_list if file_item.get("selected", False))
        return 0 < selected_count < len(self._file_list)
    
    # 上传相关的属性委托给UploadViewModel
    @Property(int, notify=fileListChanged)
    def upload_progress(self):
        return self._upload_vm.upload_progress
    
    @Property(bool, notify=fileListChanged)
    def is_uploading(self):
        return self._upload_vm.is_uploading
    
    @Property(str, notify=fileListChanged)
    def current_upload_file(self):
        return self._upload_vm.current_upload_file
    
    @Property(list, notify=fileListChanged)
    def upload_queue(self):
        return self._upload_vm.upload_queue
    
    @Property(int, notify=fileListChanged)
    def queue_progress(self):
        return self._upload_vm.queue_progress
    
    @Property(int, notify=fileListChanged)
    def queue_total(self):
        return self._upload_vm.queue_total
    
    # 获取UploadViewModel实例的方法
    def get_upload_viewmodel(self):
        """获取上传ViewModel实例"""
        return self._upload_vm
    
    def _on_upload_progress_changed(self, progress: int):
        """处理上传进度变化"""
        self.fileListChanged.emit()  # 触发属性更新
    
    def _on_upload_finished(self, success: bool, message: str):
        """处理上传完成"""
        if success:
            # 上传成功后刷新文件列表
            self.refresh_file_list()
        self.fileListChanged.emit()  # 触发属性更新
    
    def _on_upload_started(self, file_name: str):
        """处理上传开始"""
        self.fileListChanged.emit()  # 触发属性更新
    
    def _on_upload_cancelled(self):
        """处理上传取消"""
        self.fileListChanged.emit()  # 触发属性更新 