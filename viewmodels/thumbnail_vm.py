from PySide6.QtCore import QObject, Signal, Slot, QUrl
from PySide6.QtGui import QImage
from api.thumbnail_api import ThumbnailAPI
from typing import Optional
import base64

class ThumbnailVM(QObject):
    thumbnailReady = Signal(str, str)  # 文件路径, 缩略图数据URL（字符串）
    thumbnailFailed = Signal(str, str)  # 文件路径, 错误信息

    def __init__(self, api: Optional[ThumbnailAPI] = None):
        super().__init__()
        self._api = api if api is not None else ThumbnailAPI()

    @Slot(str)
    def set_token(self, token: str):
        self._api.set_token(token)

    def _detect_image_mime(self, data: bytes) -> str:
        if data.startswith(b'\x89PNG\r\n\x1a\n'):
            return "image/png"
        elif data.startswith(b'\xff\xd8'):
            return "image/jpeg"
        elif data.startswith(b'GIF8'):
            return "image/gif"
        return "application/octet-stream"

    @Slot(str)
    @Slot(str, int)
    @Slot(str, int, int)
    def requestThumbnail(self, file_path: str, width: Optional[int] = None, height: Optional[int] = None):
        # print(f"[ThumbnailVM] requestThumbnail: file_path={file_path}, width={width}, height={height}")
        result = self._api.get_thumbnail_files(fullpath=file_path, width=width, height=height)

        if isinstance(result, bytes):
            image = QImage.fromData(result)
            if not image.isNull():
                mime = self._detect_image_mime(result)
                base64_str = base64.b64encode(result).decode("utf-8")
                data_url = f"data:{mime};base64,{base64_str}"
                self.thumbnailReady.emit(file_path, data_url)  # 这里直接传字符串
            else:
                self.thumbnailFailed.emit(file_path, "Invalid image data")
        else:
            error = result.get("error", "Unknown error") if isinstance(result, dict) else str(result)
            self.thumbnailFailed.emit(file_path, error)
