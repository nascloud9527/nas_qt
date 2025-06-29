import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from viewmodels.login_vm import LoginViewModel
from viewmodels.theme_manager import ThemeManager
from viewmodels.file_vm import FileViewModel
from viewmodels.usb_monitor import USBMonitor
from viewmodels.download_vm import DownloadViewModel
from viewmodels.typefiles_vm import TypeFilesViewModel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # 添加 ui 目录到导入路径
    ui_path = os.path.join(os.path.dirname(__file__), "ui")
    engine.addImportPath(ui_path)
    
    # 添加 components 目录到导入路径
    components_path = os.path.join(ui_path, "components")
    engine.addImportPath(components_path)

    # 创建 ViewModels 并设置为全局上下文属性
    login_vm = LoginViewModel()
    theme_manager = ThemeManager()
    file_vm = FileViewModel()
    usb_monitor = USBMonitor()
    download_vm = DownloadViewModel() 
    typefiles_vm = TypeFilesViewModel()

    engine.rootContext().setContextProperty("loginVM", login_vm)
    engine.rootContext().setContextProperty("themeManager", theme_manager)
    engine.rootContext().setContextProperty("fileVM", file_vm)
    engine.rootContext().setContextProperty("usbMonitor", usb_monitor)
    engine.rootContext().setContextProperty("downloadVM", download_vm)
    engine.rootContext().setContextProperty("typefilesVM", typefiles_vm)

    # 加载主窗口
    engine.load("ui/MainWindow.qml")
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec()) 