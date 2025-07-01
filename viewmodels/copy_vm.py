from PySide6.QtCore import QObject, Signal, Slot, Property
from api.copy_api import CopyAPI
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class CopyViewModel(QObject):
    """文件复制/移动ViewModel，专门处理文件复制和移动相关功能"""
    
    # 信号定义
    copyProgressChanged = Signal(int)  # 复制进度信号
    copyFinished = Signal(bool, str)  # 复制完成信号 (success, message)
    copyStarted = Signal(str)  # 复制开始信号 (operation_type)
    copyCancelled = Signal()  # 复制取消信号
    targetDirectoryChanged = Signal(str)  # 目标目录改变信号
    
    def __init__(self):
        super().__init__()
        self._copy_api = CopyAPI()
        self._copy_progress = 0
        self._is_copying = False
        self._current_operation = ""  # "copy" 或 "move"
        self._target_directory = ""
        self._selected_files = []  # 选中的文件列表
        self._operation_queue = []  # 操作队列
        self._current_operation_index = -1
    
    @Slot(str)
    def set_token(self, token: str):
        """设置认证 token"""
        self._copy_api.set_token(token)
    
    @Slot(list)
    def set_selected_files(self, files: list):
        """设置选中的文件列表"""
        self._selected_files = files
    
    @Slot(str)
    def set_target_directory(self, directory: str):
        """设置目标目录"""
        if self._target_directory != directory:
            self._target_directory = directory
            self.targetDirectoryChanged.emit(directory)
    
    @Slot(str)
    def copy_files(self, target_directory: str = ""):
        """复制文件到指定目录"""
        if not self._selected_files:
            self.copyFinished.emit(False, "没有选中任何文件")
            return
        
        if target_directory:
            self.set_target_directory(target_directory)
        
        if not self._target_directory:
            self.copyFinished.emit(False, "请指定目标目录")
            return
        
        self._start_operation("copy")
    
    @Slot(str)
    def move_files(self, target_directory: str = ""):
        """移动文件到指定目录"""
        if not self._selected_files:
            self.copyFinished.emit(False, "没有选中任何文件")
            return
        
        if target_directory:
            self.set_target_directory(target_directory)
        
        if not self._target_directory:
            self.copyFinished.emit(False, "请指定目标目录")
            return
        
        self._start_operation("move")
    
    def _start_operation(self, operation_type: str):
        """开始复制或移动操作"""
        self._is_copying = True
        self._copy_progress = 0
        self._current_operation = operation_type
        self.copyProgressChanged.emit(0)
        self.copyStarted.emit(operation_type)
        
        # 获取文件路径列表
        file_paths = []
        for file_item in self._selected_files:
            if isinstance(file_item, dict):
                file_path = file_item.get("relPath", "")
            else:
                file_path = str(file_item)
            
            if file_path:
                file_paths.append(file_path)
        
        if not file_paths:
            self.copyFinished.emit(False, "没有有效的文件路径")
            self._is_copying = False
            return
        
        # 调用API执行操作
        result = self._copy_api.copy_files(
            files=file_paths,
            to_dir=self._target_directory,
            action=operation_type
        )
        
        if result["success"]:
            self._copy_progress = 100
            self.copyProgressChanged.emit(100)
            operation_name = "复制" if operation_type == "copy" else "移动"
            self.copyFinished.emit(True, f"文件{operation_name}成功")
        else:
            error_msg = result.get("error", "操作失败")
            operation_name = "复制" if operation_type == "copy" else "移动"
            self.copyFinished.emit(False, f"文件{operation_name}失败: {error_msg}")
        
        self._is_copying = False
        self._current_operation = ""
        self.copyProgressChanged.emit(0)  # 重置进度
    
    @Slot()
    def select_target_directory(self):
        """选择目标目录"""
        from PySide6.QtWidgets import QFileDialog, QApplication
        
        # 获取当前应用实例
        app = QApplication.instance()
        if not app:
            self.copyFinished.emit(False, "无法获取应用程序实例")
            return
        
        # 打开目录选择对话框
        directory = QFileDialog.getExistingDirectory(
            None,
            "选择目标目录",
            "",
            QFileDialog.ShowDirsOnly
        )
        
        if directory:
            self.set_target_directory(directory)
    
    @Slot()
    def cancel_operation(self):
        """取消当前操作"""
        if self._is_copying:
            self._is_copying = False
            self._current_operation = ""
            self.copyCancelled.emit()
            self.copyProgressChanged.emit(0)
    
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
    
    @Slot(result=bool)
    def can_perform_operation(self):
        """检查是否可以执行操作"""
        return len(self._selected_files) > 0 and bool(self._target_directory)
    
    # 属性定义
    @Property(int, notify=copyProgressChanged)
    def copy_progress(self):
        """复制进度"""
        return self._copy_progress
    
    @Property(bool, notify=copyProgressChanged)
    def is_copying(self):
        """是否正在复制"""
        return self._is_copying
    
    @Property(str, notify=copyStarted)
    def current_operation(self):
        """当前操作类型"""
        return self._current_operation
    
    @Property(str, notify=targetDirectoryChanged)
    def target_directory(self):
        """目标目录"""
        return self._target_directory
    
    @Property(list, notify=copyProgressChanged)
    def selected_files(self):
        """选中的文件列表"""
        return self._selected_files.copy()
    
    @Property(int, notify=copyProgressChanged)
    def selected_files_count(self):
        """选中文件的数量"""
        return len(self._selected_files)