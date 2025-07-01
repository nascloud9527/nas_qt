import requests
import sys
import os
from typing import List, Dict

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import config


class Dlna2API:
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
    
    def list_dlna2(self) -> List[Dict]:
        """获取DLNA2设备列表"""
        try:
            url = f"{config.API_BASE_URL}/dlna2/list"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get("dlna", [])
        except requests.exceptions.RequestException as e:
            print(f"获取DLNA2设备列表失败: {e}")
            return []
    
    def play_on_dlna2(self, relpath: str, dlna_id: str) -> Dict:
        """在DLNA2设备上播放"""
        try:
            url = f"{config.API_BASE_URL}/dlna2/play"
            payload = {
                "relpath": relpath,
                "dlna": dlna_id
            }
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"在DLNA2设备上播放失败: {e}")
            return {"error": str(e)}
    
    def dlna_command2(self, dlna_id: str, cmd: str, val: int = 0) -> Dict:
        """控制DLNA2设备
        
        Args:
            dlna_id: DLNA设备ID
            cmd: 控制命令，支持的命令：
                - "Pause": 暂停
                - "Unpause": 继续播放
                - "Stop": 停止
                - "FastForward": 快进10秒
                - "Rewind": 后退10秒
                - "SetVolume": 设置音量（需要val参数）
            val: 音量值（0-100），仅在cmd为"SetVolume"时使用
        """
        try:
            url = f"{config.API_BASE_URL}/dlna2/controll"
            payload = {
                "dlna": dlna_id,
                "cmd": cmd,
                "val": val
            }
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"控制DLNA2设备失败: {e}")
            return {"error": str(e)}
      