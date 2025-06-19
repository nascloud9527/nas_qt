from PySide6.QtCore import QObject, Signal, Slot, Property
from api.file_api import FileAPI

class FileViewModel(QObject):
    fileListChanged = Signal()
    loadingChanged = Signal()
    errorChanged = Signal()
    
    def __init__(self):
        super().__init__()
        self._file_api = FileAPI()
        self._file_list = []
        self._current_directory = ""
        self._current_username = ""  # 当前登录的用户名
        self._is_loading = False
        self._error_message = ""
    
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
            files_data = result["data"].get("files", [])
            
            # 转换文件数据格式
            self._file_list = []
            for file_data in files_data:
                transformed_file = self._file_api.transform_file_data(file_data)
                self._file_list.append(transformed_file)
            
            self._error_message = ""
        else:
            self._error_message = result.get("error", "获取文件列表失败")
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
        if 0 <= index < len(self._file_list):
            self._file_list[index]["selected"] = selected
            self.fileListChanged.emit()
    
    @Slot(bool)
    def select_all_files(self, selected: bool):
        """全选/取消全选文件"""
        for file_item in self._file_list:
            file_item["selected"] = selected
        self.fileListChanged.emit()
    
    @Slot()
    def get_selected_files(self):
        """获取选中的文件列表"""
        return [file_item for file_item in self._file_list if file_item.get("selected", False)]
    
    @Property(list, notify=fileListChanged)
    def file_list(self):
        return self._file_list
    
    @Property(str, notify=fileListChanged)
    def current_directory(self):
        return self._current_directory
    
    @Property(bool, notify=loadingChanged)
    def is_loading(self):
        return self._is_loading
    
    @Property(str, notify=errorChanged)
    def error_message(self):
        return self._error_message 