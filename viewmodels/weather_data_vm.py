#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from tq_qpi.core import GaodeWeather
from tq_qpi.ip_utils import get_public_ip
from viewmodels.weather_vm import WeatherViewModel

class WeatherDataVM:
    def __init__(self, gaode_api_key):
        self.weather_service = GaodeWeather(gaode_api_key)

    def create_weather_vm(self):
        print("=== 获取当前位置 ===")
        public_ip = get_public_ip()
        print(f"本机公网IP: {public_ip or '获取失败'}")

        location = self.weather_service.get_location_by_ip(public_ip)
        if "error" in location:
            print(f"定位失败: {location['error']}")
            # 返回一个空VM，避免程序崩溃
            return WeatherViewModel({
                "weather": "未知",
                "city": "",
                "date": "",
                "time": "",
                "tempRange": ""
            })

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

        city_name = f"{location.get('city', '')}{district}{township}"
        print(f"定位结果: {city_name}")

        realtime_weather = self.weather_service.get_weather(location["adcode"])
        if realtime_weather["status"] == "success":
            weather = realtime_weather["data"]
            weather_text = weather.get("weather", "")
            temp = weather.get("temperature", "")
            temp_range = f"{temp}°C"
        else:
            weather_text = "未知"
            temp_range = ""

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

        return WeatherViewModel(weather_data)
