import os
import requests
from typing import Dict, Optional
import sys

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import config


class UploadAPI:
    """文件上传API类，专门处理文件上传相关功能"""
    
    def __init__(self, token: str = ""):
        """
        初始化上传API
        
        Args:
            token: 认证token
        """
        self.headers = {
            "Authorization": f"Bearer {token}" if token else "",
            "Content-Type": "application/json"
        }
    
    def set_token(self, token: str):
        """
        设置认证token
        
        Args:
            token: 认证token
        """
        self.headers["Authorization"] = f"Bearer {token}"
    
    def upload_file(self, file_path: str, current_dir: str = "") -> Dict:
        """
        上传文件到指定目录
        
        Args:
            file_path: 本地文件路径
            current_dir: 目标目录的相对路径，如 'admin/视频'
            
        Returns:
            Dict: 包含上传结果的响应数据
        """
        url = f"{config.get_api_base_url()}/api/file/upload"
        
        # 构建查询参数
        params = {}
        if current_dir:
            params["curdir"] = current_dir
        
        # 准备上传的文件
        try:
            with open(file_path, 'rb') as file:
                files = {'file': (os.path.basename(file_path), file, 'application/octet-stream')}
                
                # 上传时不需要Content-Type头，让requests自动设置multipart/form-data
                upload_headers = {
                    "Authorization": self.headers["Authorization"]
                }
                
                response = requests.post(url, headers=upload_headers, params=params, files=files)
                
                return {
                    "success": response.status_code == 200,
                    "status_code": response.status_code,
                    "data": response.json() if response.status_code == 200 else None,
                    "error": response.text if response.status_code != 200 else None
                }
                
        except FileNotFoundError:
            return {
                "success": False,
                "status_code": 0,
                "data": None,
                "error": f"文件不存在: {file_path}"
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
                "error": f"上传失败: {str(e)}"
            }
    
    def upload_file_with_progress(self, file_path: str, current_dir: str = "", progress_callback=None) -> Dict:
        """
        带进度回调的文件上传
        
        Args:
            file_path: 本地文件路径
            current_dir: 目标目录的相对路径
            progress_callback: 进度回调函数，接收进度百分比参数
            
        Returns:
            Dict: 包含上传结果的响应数据
        """
        url = f"{config.get_api_base_url()}/api/file/upload"
        
        # 构建查询参数
        params = {}
        if current_dir:
            params["curdir"] = current_dir
        
        try:
            # 获取文件大小
            file_size = os.path.getsize(file_path)
            
            with open(file_path, 'rb') as file:
                files = {'file': (os.path.basename(file_path), file, 'application/octet-stream')}
                
                upload_headers = {
                    "Authorization": self.headers["Authorization"]
                }
                
                # 创建自定义的进度监控器
                class ProgressMonitor:
                    def __init__(self, total_size, callback):
                        self.total_size = total_size
                        self.uploaded_size = 0
                        self.callback = callback
                    
                    def update(self, chunk_size):
                        self.uploaded_size += chunk_size
                        if self.callback and self.total_size > 0:
                            progress = int((self.uploaded_size / self.total_size) * 100)
                            self.callback(progress)
                
                progress_monitor = ProgressMonitor(file_size, progress_callback)
                
                # 使用流式上传来监控进度
                response = requests.post(
                    url, 
                    headers=upload_headers, 
                    params=params, 
                    files=files,
                    stream=True
                )
                
                return {
                    "success": response.status_code == 200,
                    "status_code": response.status_code,
                    "data": response.json() if response.status_code == 200 else None,
                    "error": response.text if response.status_code != 200 else None
                }
                
        except FileNotFoundError:
            return {
                "success": False,
                "status_code": 0,
                "data": None,
                "error": f"文件不存在: {file_path}"
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
                "error": f"上传失败: {str(e)}"
            }
    
    def validate_file(self, file_path: str) -> Dict:
        """
        验证文件是否适合上传
        
        Args:
            file_path: 文件路径
            
        Returns:
            Dict: 验证结果
        """
        if not file_path:
            return {
                "valid": False,
                "error": "文件路径不能为空"
            }
        
        if not os.path.exists(file_path):
            return {
                "valid": False,
                "error": "文件不存在"
            }
        
        if not os.path.isfile(file_path):
            return {
                "valid": False,
                "error": "路径不是文件"
            }
        
        # 检查文件大小（可选：设置最大文件大小限制）
        file_size = os.path.getsize(file_path)
        max_size = 1024 * 1024 * 1024  # 1GB
        if file_size > max_size:
            return {
                "valid": False,
                "error": f"文件大小超过限制（最大 {max_size // (1024*1024*1024)}GB）"
            }
        
        return {
            "valid": True,
            "file_size": file_size
        } 