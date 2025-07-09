#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IP地址相关工具函数
"""

import requests

def get_public_ip():
    """获取本机公网IP地址"""
    services = [
        {"url": "https://api.ipify.org?format=json", "field": "ip"},
        {"url": "https://httpbin.org/ip", "field": "origin"},
        {"url": "https://ipinfo.io/json", "field": "ip"}
    ]
    
    for service in services:
        try:
            response = requests.get(service["url"], timeout=3)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data.get(service["field"]), str):
                    return data[service["field"]].split(",")[0].strip()
        except:
            continue
    return None