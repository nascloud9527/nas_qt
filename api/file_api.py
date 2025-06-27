import requests
from typing import Optional, Dict, List
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import config

class FileAPI:
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
    
    def get_file_list(self, currentdir: Optional[str] = None) -> Dict:
        """
        获取文件列表
        
        Args:
            currentdir: 目标目录的相对路径，如果为空则获取根目录
            
        Returns:
            Dict: 包含文件列表的响应数据
        """
        url = f"{config.get_api_base_url()}/api/file/files"
        
        # 构建查询参数
        params = {}
        if currentdir:
            params["currentdir"] = currentdir
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
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
    
    def create_directory(self, root_dir: str = "", cur_dir: str = "", name: str = "") -> Dict:
        """
        创建文件夹
        
        Args:
            root_dir: 根目录类型，空字符串表示用户目录，"public" 表示公共目录
            cur_dir: 当前目录的相对路径，空字符串表示根目录
            name: 要创建的目录名称
            
        Returns:
            Dict: 包含创建结果的响应数据
        """
        url = f"{config.get_api_base_url()}/api/mkdir"
        
        data = {
            "rootDir": root_dir,
            "curDir": cur_dir,
            "name": name
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
                "error": f"创建文件夹失败: {str(e)}"
            }
    
    def format_file_size(self, size_bytes: int) -> str:
        """
        格式化文件大小显示
        
        Args:
            size_bytes: 文件大小（字节）
            
        Returns:
            str: 格式化后的大小字符串
        """
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = 0
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        return f"{size_bytes:.1f} {size_names[i]}"
    
    def format_date(self, date_string: str) -> str:
        """
        格式化日期显示
        
        Args:
            date_string: ISO 格式的日期字符串
            
        Returns:
            str: 格式化后的日期字符串
        """
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return dt.strftime("%Y-%m-%d %H:%M")
        except:
            return date_string
    
    def transform_file_data(self, file_data: Dict) -> Dict:
        """
        转换文件数据格式，适配前端显示
        
        Args:
            file_data: 原始文件数据
            
        Returns:
            Dict: 转换后的文件数据
        """
        return {
            "name": file_data.get("Filename", ""),
            "relPath": file_data.get("RelPath", ""),
            "isDir": file_data.get("IsDir", False),
            "isPublic": file_data.get("IsPublic", False),
            "size": self.format_file_size(file_data.get("Size", 0)),
            "sizeBytes": file_data.get("Size", 0),
            "updatedAt": self.format_date(file_data.get("UpdatedAt", "")),
            "rawUpdatedAt": file_data.get("UpdatedAt", ""),
            "selected": False,  # 前端选择状态
            "type": self.get_file_type(file_data.get("Filename", ""), file_data.get("IsDir", False))
        }
    
    def get_file_type(self, filename: str, is_dir: bool) -> str:
        """
        根据文件名和目录状态获取文件类型
        
        Args:
            filename: 文件名
            is_dir: 是否为目录
            
        Returns:
            str: 文件类型
        """
        if is_dir:
            return "文件夹"
        
        # 根据文件扩展名判断类型
        ext = filename.lower().split('.')[-1] if '.' in filename else ""
        
        type_mapping = {
            # 文档类型
            "doc": "文档", "docx": "文档", "pdf": "文档", "txt": "文档",
            "xls": "文档", "xlsx": "文档", "ppt": "文档", "pptx": "文档",
            
            # 图片类型
            "jpg": "图片", "jpeg": "图片", "png": "图片", "gif": "图片",
            "bmp": "图片", "svg": "图片", "webp": "图片",
            
            # 视频类型
            "mp4": "视频", "avi": "视频", "mov": "视频", "wmv": "视频",
            "flv": "视频", "mkv": "视频", "webm": "视频",
            
            # 音频类型
            "mp3": "音频", "wav": "音频", "flac": "音频", "aac": "音频",
            "ogg": "音频", "wma": "音频",
            
            # 压缩包类型
            "zip": "压缩包", "rar": "压缩包", "7z": "压缩包", "tar": "压缩包",
            "gz": "压缩包"
        }
        
        return type_mapping.get(ext, "其他")
    
    def get_parent_directory(self, current_directory: str) -> str:
        """
        获取父目录路径
        
        Args:
            current_directory: 当前目录路径
            
        Returns:
            str: 父目录路径，如果已经是根目录则返回空字符串
        """
        if not current_directory:
            return ""
        
        # 移除末尾的斜杠
        current_directory = current_directory.rstrip('/')
        
        # 如果路径为空，说明已经是根目录
        if not current_directory:
            return ""
        
        # 获取父目录
        parent_directory = '/'.join(current_directory.split('/')[:-1])
        return parent_directory 