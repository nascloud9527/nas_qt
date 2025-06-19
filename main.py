import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from viewmodels.login_vm import LoginViewModel

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # 添加 ui 目录到导入路径
    ui_path = os.path.join(os.path.dirname(__file__), "ui")
    engine.addImportPath(ui_path)

    # 创建 loginVM 并设置为全局上下文属性
    login_vm = LoginViewModel()
    engine.rootContext().setContextProperty("loginVM", login_vm)

    # 加载主窗口
    engine.load("ui/MainWindow.qml")
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec()) 