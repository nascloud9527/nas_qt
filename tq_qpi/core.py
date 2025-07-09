#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高德地图API核心功能模块
"""

import requests

class GaodeWeather:
    def __init__(self, api_key):
        self.api_key = api_key
        self.ip_url = "https://restapi.amap.com/v3/ip"
        self.weather_url = "https://restapi.amap.com/v3/weather/weatherInfo"
    
    def get_location_by_ip(self, ip=None):
        """通过IP获取地理位置信息"""
        params = {
            "key": self.api_key,
            "ip": ip or ""
        }
        
        try:
            response = requests.get(self.ip_url, params=params, timeout=5)
            data = response.json()
            
            if data.get("status") == "1":
                return {
                    "ip": ip,
                    "province": data.get("province", ""),
                    "city": data.get("city", ""),
                    "adcode": data.get("adcode", ""),
                    "rectangle": data.get("rectangle", "")
                }
            return {"error": data.get("info", "未知错误")}
        except Exception as e:
            return {"error": f"API请求失败: {str(e)}"}

    def get_weather(self, adcode, extensions="base"):
        """通过adcode获取天气信息"""
        params = {
            "key": self.api_key,
            "city": adcode,
            "extensions": extensions
        }
        
        try:
            response = requests.get(self.weather_url, params=params, timeout=5)
            data = response.json()
            
            if data.get("status") == "1":
                weather_data = data.get("lives", [{}])[0] if extensions == "base" else data.get("forecasts", [{}])[0]
                return {"status": "success", "data": weather_data}
            return {"status": "error", "message": data.get("info", "未知错误")}
        except Exception as e:
            return {"status": "error", "message": f"API请求失败: {str(e)}"}
        
    def get_regeo(self, location):
        """逆地理编码（坐标->详细地址）"""
        url = "https://restapi.amap.com/v3/geocode/regeo"
        params = {
            "key": self.api_key,
            "location": location,
            "extensions": "base"
        }
        try:
            response = requests.get(url, params=params, timeout=5)
            data = response.json()
            if data.get("status") == "1":
                return data.get("regeocode", {})
            return {"error": data.get("info", "逆地理编码失败")}
        except Exception as e:
            return {"error": f"API请求失败: {str(e)}"}    