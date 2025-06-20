# 鼠标操作功能说明

本文档详细说明了 NAS 文件管理系统中新增的鼠标操作功能。

## 🖱️ 鼠标操作概览

### 左键操作

#### 1. 左键单击 (Single Click)
- **功能**: 选中文件或文件夹
- **行为**: 
  - 点击文件/文件夹时，会清除其他项目的选中状态
  - 只选中当前点击的项目
  - 复选框状态会同步更新

#### 2. 左键双击 (Double Click)
- **功能**: 打开文件或进入文件夹
- **行为**:
  - **文件夹**: 双击文件夹会进入该文件夹，加载其内容
  - **文件**: 双击文件会使用系统默认程序打开该文件

### 右键操作

#### 右键菜单 (Right Click)
- **功能**: 显示上下文菜单，提供文件操作选项
- **菜单项**:
  - **打开**: 打开文件或进入文件夹
  - **复制**: 复制文件（待实现）
  - **删除**: 删除文件（待实现）
  - **重命名**: 重命名文件（待实现）
  - **属性**: 查看文件属性（待实现）

## 🔧 技术实现

### ViewModel 层 (file_vm.py)

#### 新增方法

```python
@Slot(int)
def select_file(self, index: int):
    """选中文件（单击）"""
    # 清除其他文件的选中状态，只选中指定文件

@Slot(int)
def open_file_or_folder(self, index: int):
    """打开文件或进入文件夹（双击）"""
    # 根据文件类型执行不同操作

@Slot(str)
def open_file_with_system(self, file_path: str):
    """使用系统默认程序打开文件"""
    # 跨平台文件打开支持

@Slot(int, int, int)
def show_context_menu(self, x: int, y: int, index: int):
    """显示右键菜单"""
    # 发出右键菜单信号
```

#### 新增信号

```python
fileOpened = Signal(str)           # 文件打开信号
directoryChanged = Signal(str)     # 目录改变信号
contextMenuRequested = Signal(int, int, int)  # 右键菜单信号
```

### UI 层 (FileListArea.qml)

#### 鼠标事件处理

```qml
MouseArea {
    // 单击选中文件
    onClicked: {
        if (mouse.button === Qt.LeftButton) {
            fileVM.select_file(index)
        }
    }
    
    // 双击打开文件或文件夹
    onDoubleClicked: {
        if (mouse.button === Qt.LeftButton) {
            fileVM.open_file_or_folder(index)
        }
    }
    
    // 右键菜单
    onPressAndHold: {
        if (mouse.button === Qt.RightButton) {
            contextMenu.contextIndex = index
            contextMenu.popup()
        }
    }
    
    // 右键点击（兼容桌面平台）
    onReleased: {
        if (mouse.button === Qt.RightButton) {
            contextMenu.contextIndex = index
            contextMenu.popup()
        }
    }
}
```

#### 右键菜单组件

```qml
Menu {
    id: contextMenu
    property int contextIndex: -1
    
    MenuItem {
        text: "打开"
        onTriggered: {
            if (contextMenu.contextIndex >= 0) {
                fileVM.open_file_or_folder(contextMenu.contextIndex)
            }
        }
    }
    
    // 其他菜单项...
}
```

## 🌐 跨平台支持

### 文件打开功能

系统会根据不同平台使用相应的命令打开文件：

- **Windows**: `os.startfile(file_path)`
- **macOS**: `open file_path`
- **Linux**: `xdg-open file_path`

### 右键菜单兼容性

- **桌面平台**: 使用 `onReleased` 事件
- **移动平台**: 使用 `onPressAndHold` 事件

## 📝 使用示例

### 基本操作流程

1. **浏览文件夹**:
   - 左键单击选中文件夹
   - 左键双击进入文件夹

2. **打开文件**:
   - 左键单击选中文件
   - 左键双击打开文件

3. **文件操作**:
   - 右键点击文件显示菜单
   - 选择相应的操作选项

### 快捷键支持

- **Ctrl+A**: 全选文件（通过复选框实现）
- **空格键**: 切换选中状态（待实现）

## 🔮 未来扩展

### 计划实现的功能

1. **文件操作**:
   - 复制文件
   - 删除文件
   - 重命名文件
   - 查看文件属性

2. **拖拽支持**:
   - 文件拖拽移动
   - 文件拖拽复制

3. **多选操作**:
   - Ctrl+点击多选
   - Shift+点击范围选择

4. **键盘快捷键**:
   - 方向键导航
   - Enter键打开
   - Delete键删除

## 🐛 故障排除

### 常见问题

1. **文件无法打开**:
   - 检查文件路径是否正确
   - 确认系统有默认程序关联该文件类型
   - 查看控制台错误信息

2. **右键菜单不显示**:
   - 确认鼠标右键功能正常
   - 检查QML组件是否正确加载

3. **双击响应慢**:
   - 检查网络连接（文件列表加载）
   - 确认API响应正常

### 调试方法

1. **查看控制台输出**:
   ```bash
   python3 main.py
   ```

2. **检查信号连接**:
   - 确认ViewModel信号正确连接
   - 验证QML事件处理正常

3. **测试API连接**:
   - 确认NAS服务器可访问
   - 验证认证token有效

---

**注意**: 本功能需要 PySide6 支持，确保已正确安装相关依赖。 