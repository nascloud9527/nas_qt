import requests
import sys
import os
from typing import List, Dict

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import config


class DeleteAPI:
    def __init__(self, token: str = ""):
        self.token = token
        self.headers = {
            "Authorization": f"Bearer {token}" if token else "",
            "Content-Type": "application/json"
        }
    
    def set_token(self, token: str):
        """设置认证 token"""
        self.token = token
        self.headers["Authorization"] = f"Bearer {token}"
    
    def delete_files(self, files: List[str]) -> Dict:
        """
        删除文件或文件夹
        
        Args:
            files: 要删除的文件路径列表（相对路径）
            
        Returns:
            Dict: 包含删除结果的响应数据
        """
        url = f"{config.get_api_base_url()}/api/file/delete"
        
        data = {
            "files": files
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            
            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "data": response.json() if response.status_code == 200 else None,
                "error": response.text if response.status_code != 200 else None
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "status_code": 0,
                "data": None,
                "error": str(e)
            }
        except Exception as e:
            return {
                "success": False,
                "status_code": 0,
                "data": None,
                "error": f"删除文件失败: {str(e)}"
            }

