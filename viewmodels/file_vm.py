from PySide6.QtCore import QObject, Signal, Slot, Property
from api.file_api import FileAPI
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
    uploadProgressChanged = Signal(int)  # 上传进度信号
    uploadFinished = Signal(bool, str)  # 上传完成信号 (success, message)
    createFolderFinished = Signal(bool, str)  # 创建文件夹完成信号 (success, message)
    creatingFolderChanged = Signal()  # 创建文件夹状态变化信号
    showCreateFolderDialogRequested = Signal()  # 显示创建文件夹对话框信号
    
    def __init__(self):
        super().__init__()
        self._file_api = FileAPI()
        self._file_list = []
        self._current_directory = ""
        self._current_username = ""  # 当前登录的用户名
        self._is_loading = False
        self._error_message = ""
        self._upload_progress = 0
        self._is_uploading = False
        self._is_creating_folder = False
    
    @Slot(str)
    def set_token(self, token: str):
        """设置认证 token"""
        self._file_api.set_token(token)
    
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
        
        # 如果没有指定目录，使用用户名作为默认目录
        if not directory and self._current_username:
            directory = self._current_username
        
        # 调用 API 获取文件列表
        result = self._file_api.get_file_list(directory)
        
        if result["success"]:
            self._current_directory = directory
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
            self._file_list[index]["selected"] = selected
            self.fileListChanged.emit()
    
    @Slot(bool)
    def select_all_files(self, selected: bool):
        """全选/取消全选文件"""
        if self._file_list:
            for file_item in self._file_list:
                file_item["selected"] = selected
            self.fileListChanged.emit()
    
    @Slot()
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
        """使用系统默认程序打开文件"""
        try:
            # 获取完整的文件路径
            full_path = config.get_full_file_path(relative_path)
            print(f"尝试打开文件: {full_path}")
            
            # 检查文件是否存在
            if not os.path.exists(full_path):
                print(f"文件不存在: {full_path}")
                return
            
            system = platform.system()
            
            if system == "Windows":
                os.startfile(full_path)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", full_path], check=True)
            else:  # Linux
                subprocess.run(["xdg-open", full_path], check=True)
                
        except Exception as e:
            print(f"无法打开文件 {relative_path}: {e}")
            # 这里可以发出错误信号给UI显示
    
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
                current_selected = self._file_list[index].get("selected", False)
                self._file_list[index]["selected"] = not current_selected
            else:
                # 没有按Ctrl键：取消其他文件的选中状态，只选中当前文件
                for i, file_item in enumerate(self._file_list):
                    if i == index:
                        # 当前文件设置为选中
                        self._file_list[i]["selected"] = True
                    else:
                        # 其他文件取消选中
                        self._file_list[i]["selected"] = False
            
            self.fileListChanged.emit()
    
    @Slot(str)
    def upload_file(self, file_path: str):
        """上传文件到当前目录"""
        if not file_path or not os.path.exists(file_path):
            self.uploadFinished.emit(False, "文件不存在")
            return
        
        self._is_uploading = True
        self._upload_progress = 0
        self.uploadProgressChanged.emit(0)
        
        # 调用API上传文件
        result = self._file_api.upload_file(file_path, self._current_directory)
        
        if result["success"]:
            self._upload_progress = 100
            self.uploadProgressChanged.emit(100)
            self.uploadFinished.emit(True, "文件上传成功")
            # 上传成功后刷新文件列表
            self.refresh_file_list()
        else:
            error_msg = result.get("error", "上传失败")
            self.uploadFinished.emit(False, error_msg)
        
        self._is_uploading = False
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
    
    @Property(int, notify=uploadProgressChanged)
    def upload_progress(self):
        return self._upload_progress
    
    @Property(bool, notify=uploadProgressChanged)
    def is_uploading(self):
        return self._is_uploading
    
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