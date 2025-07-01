import requests
from urllib.parse import quote
from typing import Optional, Union, Dict, Any
from config import config

class ThumbnailAPI:
    def __init__(self, token: str = ""):
        self.token = token
        self.headers = {
            "Accept": "image/*",  # 明确表示接受图片响应
            "Content-Type": "application/json"
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def set_token(self, token: str):
        self.token = token
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
        elif "Authorization" in self.headers:
            del self.headers["Authorization"]

    # def get_thumbnail_files(
    #     self,
    #     fullpath: str,
    #     width: Optional[int] = None,
    #     height: Optional[int] = None,
    #     quality: Optional[int] = None,
    #     timeout: float = 10.0
    # ) -> Union[bytes, Dict[str, Any]]:
    #     """
    #     获取文件缩略图
        
    #     Args:
    #         fullpath: 文件完整路径
    #         width: 可选，缩略图宽度(像素)
    #         height: 可选，缩略图高度(像素)
    #         quality: 可选，缩略图质量(1-100)
    #         timeout: 请求超时时间(秒)
            
    #     Returns:
    #         bytes: 成功时返回缩略图二进制数据
    #         dict: 失败时返回错误信息字典
    #     """
    #     try:
    #         # 构建查询参数
    #         params = {"fullpath": quote(fullpath)}
    #         if width:
    #             params["width"] = str(width)
    #         if height:
    #             params["height"] = str(height)
    #         if quality:
    #             params["quality"] = str(max(1, min(100, quality)))  # 确保质量在1-100范围内

    #         response = requests.get(
    #             f"{config.get_api_base_url()}/api/file/thumbnail",
    #             headers=self.headers,
    #             params=params,
    #             timeout=timeout,
    #             stream=True  # 使用流式传输提高大文件处理效率
    #         )

    #         # 检查响应状态
    #         if response.status_code == 200:
    #             content_type = response.headers.get('Content-Type', '')
    #             if content_type.startswith('image/'):
    #                 return response.content
    #             else:
    #                 # 尝试解析可能的JSON错误信息
    #                 try:
    #                     return response.json()
    #                 except ValueError:
    #                     return {
    #                         "error": "Invalid response format",
    #                         "content_type": content_type,
    #                         "status_code": response.status_code
    #                     }
    #         else:
    #             # 处理错误响应
    #             try:
    #                 return response.json()
    #             except ValueError:
    #                 return {
    #                     "error": "Failed to get thumbnail",
    #                     "status_code": response.status_code,
    #                     "content": response.text[:500]  # 限制错误内容长度
    #                 }

    #     except requests.exceptions.Timeout:
    #         return {"error": "Request timeout", "type": "Timeout"}
    #     except requests.exceptions.RequestException as e:
    #         return {
    #             "error": str(e),
    #             "type": type(e).__name__
    #         }

    def get_thumbnail_files(
        self,
        fullpath: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        quality: Optional[int] = None,
        timeout: float = 10.0
    ) -> Union[bytes, Dict[str, Any]]:
        try:
            # 直接传 fullpath，不要 quote
            params = {"fullpath": fullpath}
            if width:
                params["width"] = str(width)
            if height:
                params["height"] = str(height)
            if quality:
                params["quality"] = str(max(1, min(100, quality)))  # 1-100

            response = requests.get(
                f"{config.get_api_base_url()}/api/file/thumbnail",
                headers=self.headers,
                params=params,
                timeout=timeout,
                stream=True
            )

            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                if content_type.startswith('image/'):
                    return response.content
                else:
                    try:
                        return response.json()
                    except ValueError:
                        return {
                            "error": "Invalid response format",
                            "content_type": content_type,
                            "status_code": response.status_code
                        }
            else:
                try:
                    return response.json()
                except ValueError:
                    return {
                        "error": "Failed to get thumbnail",
                        "status_code": response.status_code,
                        "content": response.text[:500]
                    }
        except requests.exceptions.Timeout:
            return {"error": "Request timeout", "type": "Timeout"}
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "type": type(e).__name__
            }
        