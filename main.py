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
from viewmodels.thumbnail_vm import ThumbnailVM
from viewmodels.copy_vm import CopyViewModel
from viewmodels.delete_vm import DeleteViewModel
from viewmodels.dlna2_vm import Dlna2ViewModel


if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # 添加 ui 目录到导入路径
    ui_path = os.path.join(os.path.dirname(__file__), "ui")
    engine.addImportPath(ui_path)
    
    # 添加 components 目录到导入路径
    components_path = os.path.join(ui_path, "components")
    engine.addImportPath(components_path)
    
    # 添加 pages 目录到导入路径
    pages_path = os.path.join(ui_path, "pages")
    engine.addImportPath(pages_path)

    # 创建 ViewModels 并设置为全局上下文属性
    login_vm = LoginViewModel()
    theme_manager = ThemeManager()
    file_vm = FileViewModel()
    usb_monitor = USBMonitor()
    download_vm = DownloadViewModel() 
    typefiles_vm = TypeFilesViewModel()
    thumbnail_vm = ThumbnailVM()
    copy_vm = CopyViewModel()
    delete_vm = DeleteViewModel()
    dlna2_vm = Dlna2ViewModel()

    engine.rootContext().setContextProperty("loginVM", login_vm)
    engine.rootContext().setContextProperty("themeManager", theme_manager)
    engine.rootContext().setContextProperty("fileVM", file_vm)
    engine.rootContext().setContextProperty("usbMonitor", usb_monitor)
    engine.rootContext().setContextProperty("downloadVM", download_vm)
    engine.rootContext().setContextProperty("typefilesVM", typefiles_vm)
    engine.rootContext().setContextProperty("thumbnailVM", thumbnail_vm)
    engine.rootContext().setContextProperty("copyVM", copy_vm)
    engine.rootContext().setContextProperty("deleteVM", delete_vm)
    engine.rootContext().setContextProperty("dlna2VM", dlna2_vm)

    # 加载主窗口
    engine.load("ui/MainWindow.qml")
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec()) 