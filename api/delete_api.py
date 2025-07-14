import requests
import sys
import json
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
    
    def delete_files(self, files: List[str], is_admin: bool = True) -> Dict:
        """
        删除文件或文件夹

        Args:
            files: 要删除的文件路径列表（相对路径）
            is_admin: 是否为admin账户，默认为True。非admin账户会去掉文件路径最前面的一级和二级目录
        Returns:
            Dict: 包含删除结果的响应数据
        """
        url = f"{config.get_api_base_url()}/api/file/delete"
        
        # 处理文件路径
        processed_files = []
        for file_path in files:
            # 分割路径
            path_parts = file_path.split('/')
            
            if is_admin:
                # admin账户去掉第一级目录
                if len(path_parts) > 1:
                    processed_path = '/'.join(path_parts[1:])
                    processed_files.append(processed_path)
                else:
                    processed_files.append(file_path)
            else:
                # 非admin账户去掉第一级和第二级目录
                if len(path_parts) > 2:
                    processed_path = '/'.join(path_parts[2:])
                    processed_files.append(processed_path)
                elif len(path_parts) > 1:
                    processed_path = '/'.join(path_parts[1:])
                    processed_files.append(processed_path)
                else:
                    processed_files.append(file_path)
        
        data = {
            "files": processed_files
        }
        
        print("=== 开始删除文件 ===")
        print(f"请求 URL: {url}")
        print(f"请求 Headers: {self.headers}")
        print(f"原始文件路径: {files}")
        print(f"处理后的文件路径: {processed_files}")
        print(f"请求数据 (JSON): {json.dumps(data, ensure_ascii=False)}")
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            
            print(f"响应状态码: {response.status_code}")
            try:
                response_json = response.json()
                print(f"响应 JSON 数据: {json.dumps(response_json, ensure_ascii=False, indent=2)}")
            except Exception:
                print(f"响应文本数据: {response.text}")
                response_json = None

            return {
                "success": response.status_code == 200,
                "status_code": response.status_code,
                "data": response_json if response.status_code == 200 else None,
                "error": response.text if response.status_code != 200 else None
            }

        except requests.exceptions.RequestException as e:
            print(f"[RequestException] 删除文件请求异常: {str(e)}")
            return {
                "success": False,
                "status_code": 0,
                "data": None,
                "error": str(e)
            }
        except Exception as e:
            print(f"[Exception] 删除文件发生未知异常: {str(e)}")
            return {
                "success": False,
                "status_code": 0,
                "data": None,
                "error": f"删除文件失败: {str(e)}"
            }
