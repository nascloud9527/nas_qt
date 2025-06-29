import requests
from config import config

class TypeFilesAPI:
    def __init__(self, token: str = ""):
        self.token = token
        self.headers = {
            "Content-Type": "application/json"
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def set_token(self, token: str):
        self.token = token
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
        elif "Authorization" in self.headers:
            # 如果 token 为空，则移除 Authorization 头
            del self.headers["Authorization"]

    def get_type_files(self, file_type: str, page: int = 1, pagesize: int = 30) -> dict:
        url = f"{config.get_api_base_url()}/api/file/typefiles"
        params = {
            "type": file_type,
            "page": page,
            "pagesize": pagesize
        }
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
