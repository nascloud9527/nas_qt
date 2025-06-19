import requests

class LoginAPI:
    BASE_URL = "http://192.168.1.102:8080"

    @staticmethod
    def login(username, password):
        url = f"{LoginAPI.BASE_URL}/api/login"
        resp = requests.post(url, json={"username": username, "password": password})
        return resp.json(), resp.status_code 