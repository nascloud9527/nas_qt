import requests
from typing import Optional, Dict, List
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import config

class USBAPI:
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
    
    def get_usb_devices(self) -> Dict:
        """
        获取已挂载的USB设备列表
        
        Returns:
            Dict: 包含USB设备列表的响应数据
        """
        url = f"{config.get_api_base_url()}/api/usb/list"
        
        try:
            response = requests.get(url, headers=self.headers)
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
    
    def get_usb_info(self) -> Dict:
        """
        获取USB挂载信息
        
        Returns:
            Dict: 包含USB挂载信息的响应数据
        """
        url = f"{config.get_api_base_url()}/api/usb/info"
        
        try:
            response = requests.get(url, headers=self.headers)
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