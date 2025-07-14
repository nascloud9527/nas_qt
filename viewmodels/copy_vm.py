from PySide6.QtCore import QObject, Signal, Slot, Property
from api.copy_api import CopyAPI
import sys
import os
import json

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
    directoryTreeChanged = Signal(str)  # 目录树改变信号（使用JSON字符串）
    directoryTreeRequested = Signal()  # 目录树请求信号
    
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
        self._pending_operation = ""  # 待执行的操作类型
        self._directory_tree = []  # 目录树数据
        self._current_operation_type = ""  # 当前操作类型，用于目录选择
        self._current_username = ""  # 当前登录的用户名
    
    @Slot(str)
    def set_token(self, token: str):
        """设置认证 token"""
        self._copy_api.set_token(token)
    
    @Slot(str)
    def set_username(self, username: str):
        """设置当前登录的用户名"""
        self._current_username = username
        print(f"CopyViewModel.set_username: 设置用户名 = {username}")
    
    def _is_admin_user(self) -> bool:
        """判断当前用户是否为admin账户"""
        is_admin = self._current_username == "admin"
        print(f"CopyViewModel._is_admin_user: 当前用户 = {self._current_username}, 是否为admin = {is_admin}")
        return is_admin
    
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
        
        print(f"_start_operation: 开始执行 {operation_type} 操作，文件数量: {len(file_paths)}")
        print(f"_start_operation: 目标目录: {self._target_directory}")
        print(f"_start_operation: 文件路径: {file_paths}")

        # 调用API执行操作
        is_admin = self._is_admin_user()
        result = self._copy_api.copy_files(
            files=file_paths,
            to_dir=self._target_directory,
            action=operation_type,
            is_admin=is_admin
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
            # 如果有选中的文件且有待执行的操作，自动执行相应操作
            if self._selected_files and self._pending_operation:
                if self._pending_operation == "copy":
                    self.copy_files(directory)
                elif self._pending_operation == "move":
                    self.move_files(directory)
                self._pending_operation = ""  # 清除待执行的操作
    
    @Slot()
    def copy_selected_files(self):
        """复制选中的文件（需要先选择目标目录）"""
        if not self._selected_files:
            self.copyFinished.emit(False, "没有选中任何文件")
            return
        
        # 设置当前操作类型
        self._current_operation_type = "copy"
        # 先获取目录树数据
        self.get_directory_tree()
    
    @Slot()
    def move_selected_files(self):
        """移动选中的文件（需要先选择目标目录）"""
        if not self._selected_files:
            self.copyFinished.emit(False, "没有选中任何文件")
            return
        
        # 设置当前操作类型
        self._current_operation_type = "move"
        # 先获取目录树数据
        self.get_directory_tree()
    
    @Slot(str)
    def copy_files_with_directory(self, target_directory: str):
        """使用指定目录执行复制操作"""
        print(f"copy_files_with_directory: 接收到的目标目录 = '{target_directory}'")
        
        if not self._selected_files:
            self.copyFinished.emit(False, "没有选中任何文件")
            return
        
        # 设置待执行的操作类型
        self._pending_operation = "copy"
        print(f"copy_files_with_directory: 设置目标目录前 _target_directory = '{self._target_directory}'")
        self.set_target_directory(target_directory)
        print(f"copy_files_with_directory: 设置目标目录后 _target_directory = '{self._target_directory}'")
        self.copy_files(target_directory)
    
    @Slot(str)
    def move_files_with_directory(self, target_directory: str):
        """使用指定目录执行移动操作"""
        print(f"move_files_with_directory: 接收到的目标目录 = '{target_directory}'")
        
        if not self._selected_files:
            self.copyFinished.emit(False, "没有选中任何文件")
            return
        
        # 设置待执行的操作类型
        self._pending_operation = "move"
        print(f"move_files_with_directory: 设置目标目录前 _target_directory = '{self._target_directory}'")
        self.set_target_directory(target_directory)
        print(f"move_files_with_directory: 设置目标目录后 _target_directory = '{self._target_directory}'")
        self.move_files(target_directory)
    
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
    
    @Property(list, notify=directoryTreeChanged)
    def directory_tree(self):
        """目录树数据"""
        return self._directory_tree.copy()
    
    @Slot()
    def get_directory_tree(self):
        """获取目录树"""
        self.directoryTreeRequested.emit()
        
        # 调用API获取目录树
        result = self._copy_api.get_directory_tree()
        
        if result["success"]:
            # 解析目录树数据
            tree_data = result["data"].get("dirs", []) if result["data"] else []
            print(f"API返回的目录树数据: {tree_data}")
            print(f"数据类型: {type(tree_data)}")
            if tree_data:
                print(f"第一个元素: {tree_data[0] if len(tree_data) > 0 else 'None'}")
                print(f"第一个元素类型: {type(tree_data[0]) if len(tree_data) > 0 else 'None'}")
            
            self._directory_tree = self._parse_directory_tree(tree_data)
            print(f"解析后的目录树: {self._directory_tree}")
            
            # 转换为QML可理解的格式
            qml_tree_data = self._convert_to_qml_format(self._directory_tree)
            print(f"QML格式的目录树: {qml_tree_data}")
            
            # 转换为JSON字符串
            try:
                json_data = json.dumps(qml_tree_data, ensure_ascii=False)
                print(f"JSON字符串: {json_data}")
                self.directoryTreeChanged.emit(json_data)
            except Exception as e:
                print(f"JSON序列化失败: {e}")
                self.copyFinished.emit(False, f"目录树数据序列化失败: {str(e)}")
        else:
            error_msg = result.get("error", "获取目录树失败")
            self.copyFinished.emit(False, f"获取目录树失败: {error_msg}")
    
    def _parse_directory_tree(self, tree_data):
        """解析目录树数据"""
        parsed_tree = []
        
        def parse_node(node_data):
            if not node_data:
                return None
            
            # 确保node_data是字典类型
            if not isinstance(node_data, dict):
                return None
            
            node = {}
            node["value"] = str(node_data.get("value", ""))
            node["title"] = str(node_data.get("title", ""))
            node["children"] = []
            
            # 递归解析子节点
            children = node_data.get("children", [])
            if isinstance(children, list):
                for child in children:
                    child_node = parse_node(child)
                    if child_node:
                        node["children"].append(child_node)
            
            return node
        
        # 解析所有根节点
        if isinstance(tree_data, list):
            for node_data in tree_data:
                node = parse_node(node_data)
                if node:
                    parsed_tree.append(node)
        
        return parsed_tree
    
    def _convert_to_qml_format(self, tree_data):
        """将Python目录树数据转换为QML可理解的格式"""
        def convert_node(node):
            if not node:
                return None
            
            # 创建简单的JavaScript对象格式
            qml_node = {
                "value": str(node.get("value", "")),
                "title": str(node.get("title", "")),
                "children": []
            }
            
            # 递归转换子节点
            children = node.get("children", [])
            if isinstance(children, list):
                for child in children:
                    child_node = convert_node(child)
                    if child_node:
                        qml_node["children"].append(child_node)
            
            return qml_node
        
        # 转换所有根节点
        qml_tree = []
        if isinstance(tree_data, list):
            for node in tree_data:
                qml_node = convert_node(node)
                if qml_node:
                    qml_tree.append(qml_node)
        
        return qml_tree
    
    @Slot(result=list)
    def get_directory_tree_data(self):
        """获取目录树数据"""
        return self._directory_tree.copy()
    
    @Slot(result=str)
    def get_current_operation_type(self):
        """获取当前操作类型"""
        return self._current_operation_type
    