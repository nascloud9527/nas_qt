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
        self.ffmpeg_path = ""           # 新增默认值
        
        # 尝试从环境变量加载
        env_file_path = os.getenv("FILE_BASE_PATH")
        if env_file_path:
            self.file_base_path = env_file_path
            
        env_api_url = os.getenv("API_BASE_URL")
        if env_api_url:
            self.api_base_url = env_api_url

        env_ffmpeg_path = os.getenv("FFMPEG_PATH")
        if env_ffmpeg_path:
            self.ffmpeg_path = env_ffmpeg_path
        
        # 尝试从 .env 文件加载
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
                            elif key == "FFMPEG_PATH":        
                                self.ffmpeg_path = value
            except Exception as e:
                print(f"读取.env文件失败: {e}")
    
    def get_full_file_path(self, relative_path: str) -> str:
        """
        获取完整的文件路径
        """
        if not relative_path:
            return ""
        
        relative_path = relative_path.replace('\\', '/')
        full_path = os.path.join(self.file_base_path, relative_path)
        return os.path.normpath(full_path)
    
    def get_file_base_path(self) -> str:
        return self.file_base_path
    
    def set_file_base_path(self, path: str):
        self.file_base_path = path
    
    def get_api_base_url(self) -> str:
        return self.api_base_url
    
    def set_api_base_url(self, url: str):
        self.api_base_url = url
    
    def get_ffmpeg_path(self) -> str:
        """获取 ffmpeg 路径"""
        return self.ffmpeg_path
    
    def set_ffmpeg_path(self, path: str):
        """设置 ffmpeg 路径"""
        self.ffmpeg_path = path

# 全局配置实例
config = Config()
