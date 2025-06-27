import requests
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import config

class LoginAPI:
    def __init__(self):
        self.base_url = config.get_api_base_url()
    
    @staticmethod
    def login(username: str, password: str):
        """用户登录"""
        try:
            url = f"{config.get_api_base_url()}/api/user/login"
            data = {
                "username": username,
                "password": password
            }
            response = requests.post(url, json=data)
            return response.json(), response.status_code
        except Exception as e:
            return {"error": str(e)}, 500 