from PySide6.QtCore import QObject, Signal, Slot, Property
from api.login_api import LoginAPI

class LoginViewModel(QObject):
    loginResult = Signal(str)
    showPasswordInput = Signal(bool)

    def __init__(self):
        super().__init__()
        self._username = ""
        self._password = ""
        self._token = ""

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
            # 保存 token
            self._token = data.get("token", "")
            self.loginResult.emit("登录成功")
        else:
            self.loginResult.emit(data.get("error", "登录失败"))
    
    @Slot(result=str)
    def get_token(self):
        """获取登录 token"""
        return self._token
    
    @Slot(result=str)
    def get_username(self):
        """获取当前登录的用户名"""
        return self._username 