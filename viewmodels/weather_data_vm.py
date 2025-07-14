#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import requests
import time
from tq_qpi.core import GaodeWeather
from tq_qpi.ip_utils import get_public_ip

class WeatherDataVM:
    def __init__(self, gaode_api_key):
        self.weather_service = GaodeWeather(gaode_api_key)
        self._timeout = 10  # 设置超时时间为10秒

    def create_weather_data(self):
        print("=== 获取当前位置 ===")
        
        # 设置默认数据
        default_data = {
            "weather": "未知",
            "city": "",
            "date": "",
            "time": "",
            "tempRange": ""
        }
        
        try:
            # 获取公网IP，设置超时
            public_ip = self._get_public_ip_with_timeout()
            print(f"本机公网IP: {public_ip or '获取失败'}")
            
            if not public_ip:
                print("无法获取公网IP，使用默认数据")
                return self._get_default_weather_data()

            # 获取位置信息，设置超时
            location = self._get_location_with_timeout(public_ip)
            if "error" in location:
                print(f"定位失败: {location['error']}")
                return self._get_default_weather_data()

            # 获取详细位置信息
            city_name = self._get_city_name(location)
            print(f"定位结果: {city_name}")

            # 获取天气信息，设置超时
            weather_info = self._get_weather_with_timeout(location["adcode"])
            weather_text = weather_info.get("weather", "未知")
            temp_range = weather_info.get("tempRange", "")

            # 生成当前时间信息
            now = datetime.now()
            week_cn = ["一", "二", "三", "四", "五", "六", "天"]
            weekday_cn = week_cn[now.weekday()] if now.weekday() < 7 else "天"

            date_str = now.strftime(f"%m.%d 星期{weekday_cn}")
            time_str = now.strftime("%H:%M")

            weather_data = {
                "weather": weather_text,
                "city": city_name,
                "date": date_str,
                "time": time_str,
                "tempRange": temp_range
            }

            return weather_data
            
        except Exception as e:
            print(f"天气数据获取异常: {str(e)}")
            return self._get_default_weather_data()

    def _get_public_ip_with_timeout(self):
        """带超时的公网IP获取"""
        try:
            # 设置请求超时
            response = requests.get("https://httpbin.org/ip", timeout=self._timeout)
            if response.status_code == 200:
                return response.json().get("origin", "").split(",")[0]
        except Exception as e:
            print(f"获取公网IP失败: {str(e)}")
        
        # 如果网络请求失败，尝试使用原有的get_public_ip方法
        try:
            return get_public_ip()
        except Exception as e:
            print(f"备用IP获取方法也失败: {str(e)}")
            return None

    def _get_location_with_timeout(self, public_ip):
        """带超时的位置获取"""
        try:
            return self.weather_service.get_location_by_ip(public_ip)
        except Exception as e:
            print(f"获取位置信息失败: {str(e)}")
            return {"error": "网络请求超时"}

    def _get_city_name(self, location):
        """获取城市名称"""
        try:
            if "rectangle" in location:
                center_lnglat = location["rectangle"].split(";")[0]
                detail_location = self.weather_service.get_regeo(center_lnglat)
                if "error" not in detail_location:
                    district = detail_location.get("addressComponent", {}).get("district", "")
                    township = detail_location.get("addressComponent", {}).get("township", "")
                else:
                    district = ""
                    township = ""
            else:
                detail_location = {}
                district = ""
                township = ""

            return f"{location.get('city', '')}{district}{township}"
        except Exception as e:
            print(f"获取城市名称失败: {str(e)}")
            return location.get('city', '')

    def _get_weather_with_timeout(self, adcode):
        """带超时的天气获取"""
        try:
            realtime_weather = self.weather_service.get_weather(adcode)
            if realtime_weather["status"] == "success":
                weather = realtime_weather["data"]
                weather_text = weather.get("weather", "")
                temp = weather.get("temperature", "")
                temp_range = f"{temp}°C"
                return {
                    "weather": weather_text,
                    "tempRange": temp_range
                }
        except Exception as e:
            print(f"获取天气信息失败: {str(e)}")
        
        return {
            "weather": "未知",
            "tempRange": ""
        }

    def _get_default_weather_data(self):
        """获取默认天气数据"""
        now = datetime.now()
        week_cn = ["一", "二", "三", "四", "五", "六", "天"]
        weekday_cn = week_cn[now.weekday()] if now.weekday() < 7 else "天"

        date_str = now.strftime(f"%m.%d 星期{weekday_cn}")
        time_str = now.strftime("%H:%M")

        return {
            "weather": "未知",
            "city": "",
            "date": date_str,
            "time": time_str,
            "tempRange": ""
        }
