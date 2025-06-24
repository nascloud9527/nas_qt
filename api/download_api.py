import requests
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import config

class DownloadAPI:
    def __init__(self, token: str = ""):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}" if token else ""
        }

    def set_token(self, token: str):
        """设置认证 token"""
        self.token = token
        self.headers["Authorization"] = f"Bearer {token}"

    def download_file(self, relpath: str, save_path: str = None) -> dict:
        """
        下载指定路径的文件
        Args:
            relpath: 文件的相对路径
            save_path: 保存到本地的路径（可选），不传则只返回二进制内容
        Returns:
            dict: {success, status_code, data/filename/content, error}
        """
        url = f"{config.get_api_base_url()}/api/download"
        params = {"relpath": relpath}
        try:
            response = requests.get(url, headers=self.headers, params=params, stream=True)
            if response.status_code == 200:
                # 获取文件名
                content_disposition = response.headers.get('Content-Disposition', '')
                filename = relpath.split('/')[-1]
                if 'filename=' in content_disposition:
                    filename = content_disposition.split('filename=')[-1].strip('"')
                # 保存文件
                if save_path:
                    file_path = save_path
                else:
                    file_path = filename
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return {
                    "success": True,
                    "status_code": 200,
                    "filename": file_path,
                    "error": None
                }
            else:
                # 尝试解析json错误信息
                try:
                    err = response.json().get('error', response.text)
                except Exception:
                    err = response.text
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "data": None,
                    "error": err
                }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "status_code": 0,
                "data": None,
                "error": str(e)
            }
