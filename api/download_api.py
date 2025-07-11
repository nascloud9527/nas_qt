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
        # print(f"DownloadAPI.set_token: 设置token={token[:10] if token else 'None'}...")
        self.token = token
        self.headers["Authorization"] = f"Bearer {token}"
        # print(f"DownloadAPI.set_token: 认证头已设置为={self.headers.get('Authorization', 'None')}")

    def download_file(self, relpath: str, save_path: str = None) -> dict:
        """
        下载指定路径的文件（修复 URL 编码问题）
        Args:
            relpath: 文件的相对路径（如 "admin/图片/file.jpg"）
            save_path: 保存到本地的路径（可选）
        """
        # 使用 params 参数让 requests 正确处理 URL 编码
        url = f"{config.get_api_base_url()}/api/file/download"
        params = {"relpath": relpath}
        
        print(f"download_file: 下载文件 relpath={relpath}")
        print(f"download_file: 请求URL={url}")
        print(f"download_file: 请求参数={params}")
        print(f"download_file: 认证头={self.headers.get('Authorization', 'None')}")
        
        try:
            response = requests.get(url, headers=self.headers, params=params, stream=True)
            print(f"download_file: 实际请求URL={response.url}")
            print(f"download_file: 响应状态码={response.status_code}")
            
            if response.status_code == 200:
                # 获取文件名（优先从 Content-Disposition 头获取）
                filename = relpath.split('/')[-1]
                content_disposition = response.headers.get('Content-Disposition', '')
                if 'filename=' in content_disposition:
                    filename = content_disposition.split('filename=')[-1].strip('"')
                
                # 确定保存路径
                file_path = save_path if save_path else filename
                
                print(f"download_file: 保存文件到 {file_path}")
                
                # 保存文件
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return {
                    "success": True,
                    "filename": file_path,
                    "error": None
                }
            else:
                error = response.json().get("error", response.text) if response.text else "Unknown error"
                print(f"download_file: 下载失败 - {error}")
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {error}"
                }
        except Exception as e:
            print(f"download_file: 异常 - {e}")
            return {
                "success": False,
                "error": str(e)
            }