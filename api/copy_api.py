import requests
import sys
import os
from typing import List, Dict

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import config


class CopyAPI:
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
    
    def copy_files(self, files: List[str], to_dir: str, action: str = "copy") -> Dict:
        """
        复制或移动文件
        
        Args:
            files: 要复制的文件路径列表
            to_dir: 目标目录路径
            action: 操作类型，"copy" 或 "move"，默认为 "copy"
        
        Returns:
            Dict: 包含操作结果的 JSON 响应
        """
        try:
            # 构建请求URL
            api_url = f"{config.get_api_base_url()}/file/copy"
            
            # 构建请求数据，与服务器端接口参数结构保持一致
            request_data = {
                "action": action,
                "todir": to_dir,
                "files": files
            }
            
            # 发送POST请求
            response = requests.post(
                api_url,
                json=request_data,
                headers=self.headers,
                timeout=30
            )
            
            # 检查响应状态
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json(),
                    "message": "操作成功"
                }
            else:
                return {
                    "success": False,
                    "error": f"请求失败，状态码: {response.status_code}",
                    "data": response.json() if response.content else None
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"网络请求异常: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"操作异常: {str(e)}"
            }
        