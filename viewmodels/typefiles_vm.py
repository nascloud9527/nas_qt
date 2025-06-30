from PySide6.QtCore import QObject, Signal, Slot, Property
from api.typefiles_api import TypeFilesAPI

class TypeFilesViewModel(QObject):
    filesChanged = Signal()
    errorChanged = Signal()
    filesFetchedSuccess = Signal(str, list)

    def __init__(self, token: str = "", parent=None):
        super().__init__(parent)
        self.api = TypeFilesAPI(token)
        self._type_files = []
        self._last_error = ""

    @Slot(str, int, int)
    def fetchTypeFiles(self, file_type, page=1, pagesize=30):
        result = self.api.get_type_files(file_type, page, pagesize)
        if result["success"]:
            files = result["data"].get("files", [])
            self._type_files = [self.transform_file_data(f) for f in files]
            self._last_error = ""
            self.filesFetchedSuccess.emit(file_type, self._type_files)
        else:
            self._type_files = []
            self._last_error = result.get("error", "未知错误")
        self.filesChanged.emit()
        self.errorChanged.emit()

    def getFiles(self):
        return self._type_files

    def getError(self):
        return self._last_error

    files = Property('QVariantList', fget=getFiles, notify=filesChanged)
    lastError = Property(str, fget=getError, notify=errorChanged)

    @Slot(str)
    def set_token(self, token: str):
        self.api.set_token(token)

    @staticmethod
    def transform_file_data(file_data: dict) -> dict:
        return {
            "id": str(file_data.get("ID", "")),
            "name": str(file_data.get("Filename", "")),
            "relPath": str(file_data.get("RelPath", "")),
            "owner": str(file_data.get("Owner", "")),
            "isPublic": bool(file_data.get("IsPublic", False)),
            "size": int(file_data.get("Size", 0)),
            "type": str(file_data.get("Type", "")),
            "createdAt": str(file_data.get("CreatedAt", "")),
            "updatedAt": str(file_data.get("UpdatedAt", "")),
        }
