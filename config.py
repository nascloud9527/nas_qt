"""
配置文件
管理应用程序的各种配置参数
"""

import os
from pathlib import Path

class Config:
    """应用程序配置类"""
    
    def __init__(self):
        self._load_config()
    
    def _load_config(self):
        """加载配置"""
        # 默认配置
        self.file_base_path = ""
        self.api_base_url = ""
        
        # 尝试从环境变量加载
        env_file_path = os.getenv("FILE_BASE_PATH")
        if env_file_path:
            self.file_base_path = env_file_path
            
        env_api_url = os.getenv("API_BASE_URL")
        if env_api_url:
            self.api_base_url = env_api_url
        
        # 尝试从.env文件加载
        env_file = Path(".env")
        if env_file.exists():
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            
                            if key == "FILE_BASE_PATH":
                                self.file_base_path = value
                            elif key == "API_BASE_URL":
                                self.api_base_url = value
            except Exception as e:
                print(f"读取.env文件失败: {e}")
    
    def get_full_file_path(self, relative_path: str) -> str:
        """
        获取完整的文件路径
        
        Args:
            relative_path: API返回的相对路径
            
        Returns:
            str: 完整的文件路径
        """
        if not relative_path:
            return ""
        
        # 确保路径分隔符正确
        relative_path = relative_path.replace('\\', '/')
        
        # 组合完整路径
        full_path = os.path.join(self.file_base_path, relative_path)
        
        # 标准化路径
        full_path = os.path.normpath(full_path)
        
        return full_path
    
    def get_file_base_path(self) -> str:
        """获取文件基础路径"""
        return self.file_base_path
    
    def set_file_base_path(self, path: str):
        """设置文件基础路径"""
        self.file_base_path = path
    
    def get_api_base_url(self) -> str:
        """获取API基础URL"""
        return self.api_base_url
    
    def set_api_base_url(self, url: str):
        """设置API基础URL"""
        self.api_base_url = url

# 全局配置实例
config = Config() 