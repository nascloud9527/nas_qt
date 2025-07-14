from PySide6.QtCore import QObject, Signal, Slot, Property
from api.delete_api import DeleteAPI
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class DeleteViewModel(QObject):
    """文件删除ViewModel，专门处理文件删除相关功能"""
    
    # 信号定义
    deleteProgressChanged = Signal(int)  # 删除进度信号
    deleteFinished = Signal(bool, str)  # 删除完成信号 (success, message)
    deleteStarted = Signal(str)  # 删除开始信号 (operation_info)
    deleteCancelled = Signal()  # 删除取消信号
    confirmationRequested = Signal(list)  # 删除确认请求信号 (files_to_delete)
    
    def __init__(self):
        super().__init__()
        self._delete_api = DeleteAPI()
        self._delete_progress = 0
        self._is_deleting = False
        self._current_operation_info = ""
        self._selected_files = []  # 选中的文件列表
        self._files_to_delete = []  # 待删除的文件列表
        self._operation_queue = []  # 操作队列
        self._current_operation_index = -1
        self._current_username = ""  # 当前登录的用户名
    
    @Slot(str)
    def set_token(self, token: str):
        """设置认证 token"""
        self._delete_api.set_token(token)
    
    @Slot(list)
    def set_selected_files(self, files: list):
        """设置选中的文件列表"""
        self._selected_files = files
    
    @Slot(str)
    def set_username(self, username: str):
        """设置当前登录的用户名"""
        self._current_username = username
        print(f"DeleteViewModel.set_username: 设置用户名 = {username}")
    
    def _is_admin_user(self) -> bool:
        """判断当前用户是否为admin账户"""
        is_admin = self._current_username == "admin"
        print(f"DeleteViewModel._is_admin_user: 当前用户 = {self._current_username}, 是否为admin = {is_admin}")
        return is_admin
    
    @Slot(list)
    def set_files_to_delete(self, files: list):
        """设置待删除的文件列表"""
        self._files_to_delete = files
    
    @Slot()
    def delete_selected_files(self):
        """删除选中的文件"""
        if not self._selected_files:
            self.deleteFinished.emit(False, "没有选中任何文件")
            return
        
        # 获取文件路径列表
        file_paths = []
        file_names = []
        for file_item in self._selected_files:
            if isinstance(file_item, dict):
                file_path = file_item.get("relPath", "")
                file_name = file_item.get("name", "")
            else:
                file_path = str(file_item)
                file_name = os.path.basename(file_path)
            
            if file_path:
                file_paths.append(file_path)
                file_names.append(file_name)
        
        if not file_paths:
            self.deleteFinished.emit(False, "没有有效的文件路径")
            return
        
        # 设置待删除文件列表
        self.set_files_to_delete(file_paths)
        
        # 请求删除确认
        self.confirmationRequested.emit(file_names)
    
    @Slot()
    def confirm_delete(self):
        """确认删除操作"""
        if not self._files_to_delete:
            self.deleteFinished.emit(False, "没有待删除的文件")
            return
        
        self._start_delete_operation()
    
    @Slot()
    def cancel_delete(self):
        """取消删除操作"""
        self._files_to_delete.clear()
        self.deleteCancelled.emit()
    
    def _start_delete_operation(self):
        """开始删除操作"""
        self._is_deleting = True
        is_admin = self._is_admin_user()
        
        self._delete_progress = 0
        self._current_operation_info = f"正在删除 {len(self._files_to_delete)} 个文件"
        self.deleteProgressChanged.emit(0)
        self.deleteStarted.emit(self._current_operation_info)
        
        # 调用API执行删除操作
        result = self._delete_api.delete_files(files=self._files_to_delete, is_admin=is_admin)
        
        if result["success"]:
            self._delete_progress = 100
            self.deleteProgressChanged.emit(100)
            self.deleteFinished.emit(True, f"成功删除 {len(self._files_to_delete)} 个文件")
        else:
            error_msg = result.get("error", "删除失败")
            self.deleteFinished.emit(False, f"删除文件失败: {error_msg}")
        
        self._is_deleting = False
        self._current_operation_info = ""
        self._files_to_delete.clear()
        self.deleteProgressChanged.emit(0)  # 重置进度
    
    @Slot(str)
    def delete_single_file(self, file_path: str):
        """删除单个文件"""
        if not file_path:
            self.deleteFinished.emit(False, "文件路径为空")
            return
        
        self.set_files_to_delete([file_path])
        self._start_delete_operation()
    
    @Slot(list)
    def delete_multiple_files(self, file_paths: list):
        """删除多个文件"""
        if not file_paths:
            self.deleteFinished.emit(False, "文件路径列表为空")
            return
        
        # 过滤有效的文件路径
        valid_paths = [path for path in file_paths if path]
        
        if not valid_paths:
            self.deleteFinished.emit(False, "没有有效的文件路径")
            return
        
        self.set_files_to_delete(valid_paths)
        self._start_delete_operation()
    
    @Slot()
    def clear_selected_files(self):
        """清空选中的文件列表"""
        self._selected_files.clear()
    
    @Slot(str)
    def add_file_to_selection(self, file_path: str):
        """添加文件到选中列表"""
        if file_path not in self._selected_files:
            self._selected_files.append(file_path)
    
    @Slot(str)
    def remove_file_from_selection(self, file_path: str):
        """从选中列表中移除文件"""
        if file_path in self._selected_files:
            self._selected_files.remove(file_path)
    
    @Slot(result=list)
    def get_selected_files(self):
        """获取选中的文件列表"""
        return self._selected_files.copy()
    
    @Slot(result=int)
    def get_selected_files_count(self):
        """获取选中文件的数量"""
        return len(self._selected_files)
    
    @Slot(result=bool)
    def has_selected_files(self):
        """检查是否有选中的文件"""
        return len(self._selected_files) > 0
    
    @Slot(result=list)
    def get_files_to_delete(self):
        """获取待删除的文件列表"""
        return self._files_to_delete.copy()
    
    @Slot(result=int)
    def get_files_to_delete_count(self):
        """获取待删除文件的数量"""
        return len(self._files_to_delete)
    
    @Slot(result=bool)
    def can_delete_files(self):
        """检查是否可以删除文件"""
        return len(self._selected_files) > 0
    
    @Slot(result=bool)
    def is_confirming_delete(self):
        """检查是否正在等待删除确认"""
        return len(self._files_to_delete) > 0 and not self._is_deleting
    
    # 属性定义
    @Property(int, notify=deleteProgressChanged)
    def delete_progress(self):
        """删除进度"""
        return self._delete_progress
    
    @Property(bool, notify=deleteProgressChanged)
    def is_deleting(self):
        """是否正在删除"""
        return self._is_deleting
    
    @Property(str, notify=deleteStarted)
    def current_operation_info(self):
        """当前操作信息"""
        return self._current_operation_info
    
    @Property(list, notify=deleteProgressChanged)
    def selected_files(self):
        """选中的文件列表"""
        return self._selected_files.copy()
    
    @Property(int, notify=deleteProgressChanged)
    def selected_files_count(self):
        """选中文件的数量"""
        return len(self._selected_files)
    
    @Property(list, notify=deleteProgressChanged)
    def files_to_delete(self):
        """待删除的文件列表"""
        return self._files_to_delete.copy()
    
    @Property(int, notify=deleteProgressChanged)
    def files_to_delete_count(self):
        """待删除文件的数量"""
        return len(self._files_to_delete)