from PySide6.QtCore import QObject, Signal, Slot
from api.login_api import LoginAPI

class LoginViewModel(QObject):
    loginResult = Signal(str)
    showPasswordInput = Signal(bool)

    def __init__(self):
        super().__init__()
        self._username = ""
        self._password = ""

    @Slot(str)
    def selectUser(self, username):
        self._username = username
        self.showPasswordInput.emit(True)

    @Slot(str)
    def setPassword(self, password):
        self._password = password

    @Slot()
    def doLogin(self):
        data, status = LoginAPI.login(self._username, self._password)
        if status == 200:
            self.loginResult.emit("登录成功")
        else:
            self.loginResult.emit(data.get("error", "登录失败")) 