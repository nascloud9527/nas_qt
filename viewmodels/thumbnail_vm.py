import base64
from PySide6.QtCore import QObject, Signal, Slot, QUrl
from PySide6.QtGui import QImage
from api.thumbnail_api import ThumbnailAPI
from typing import Optional


class ThumbnailVM(QObject):
    """
    直接使用后端缩略图服务，不维护本地缓存
    """
    thumbnailReady = Signal(str, QUrl)  # 文件路径, 缩略图数据URL
    thumbnailFailed = Signal(str, str)  # 文件路径, 错误信息

    def __init__(self, api: Optional[ThumbnailAPI] = None):
        super().__init__()
        self._api = api if api is not None else ThumbnailAPI()

    @Slot(str)
    def set_token(self, token: str):
        """设置认证 token"""
        print(f"ThumbnailVM.set_token: 设置token={token[:10] if token else 'None'}...")
        self._api.set_token(token)
        print(f"ThumbnailVM.set_token: token设置完成")

    # 根据数据头判断图片格式
    def _detect_image_mime(data: bytes) -> str:
        if data.startswith(b'\x89PNG\r\n\x1a\n'):
            return "image/png"
        elif data.startswith(b'\xff\xd8'):
            return "image/jpeg"
        elif data.startswith(b'GIF8'):
            return "image/gif"
        # 其他类型按需补充
        return "application/octet-stream"

    @Slot(str)
    @Slot(str, int)
    @Slot(str, int, int)
    def requestThumbnail(self, 
                    file_path: str,
                    width: Optional[int] = None,
                    height: Optional[int] = None):
        print(f"[ThumbnailVM] requestThumbnail: file_path={file_path}, width={width}, height={height}")

        result = self._api.get_thumbnail_files(
            fullpath=file_path,
            width=width,
            height=height
        )

        print(f"[ThumbnailVM] get_thumbnail_files 返回类型: {type(result)}")

        if isinstance(result, bytes):
            print(f"[ThumbnailVM] 缩略图字节长度: {len(result)}")
            print(f"[ThumbnailVM] 数据前10字节: {result[:10]}")

            image = QImage.fromData(result)
            print(f"[ThumbnailVM] QImage.isNull: {image.isNull()}")

            if not image.isNull():
                mime = self._detect_image_mime(result)
                print(f"[ThumbnailVM] 检测到图片类型: {mime}")
                data_url = f"data:{mime};base64,{base64.b64encode(result).decode('utf-8')}"
                print(f"[ThumbnailVM] data_url前100: {data_url[:100]} ...")
                self.thumbnailReady.emit(file_path, QUrl(data_url))
                print(f"[ThumbnailVM] thumbnailReady 信号已发射: {file_path}")
            else:
                print(f"[ThumbnailVM] QImage 解析失败")
                self.thumbnailFailed.emit(file_path, "Invalid image data")
        else:
            print(f"[ThumbnailVM] 返回非字节类型: {result}")
            error = result.get("error", "Unknown error") if isinstance(result, dict) else str(result)
            self.thumbnailFailed.emit(file_path, error)

    def _detect_image_mime(self, data: bytes) -> str:
        if data.startswith(b'\x89PNG\r\n\x1a\n'):
            return "image/png"
        elif data.startswith(b'\xff\xd8'):
            return "image/jpeg"
        elif data.startswith(b'GIF8'):
            return "image/gif"
        return "application/octet-stream"
