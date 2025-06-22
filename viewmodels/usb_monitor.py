from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl, QThread, QTimer
from PySide6.QtWebSockets import QWebSocket
from PySide6.QtWidgets import QMessageBox
import json
import subprocess
import platform
import os
import re
import sys

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from api.usb_api import USBAPI
from config import config

class USBMonitor(QObject):
    # 信号定义
    connectionStatusChanged = Signal()
    usbEventReceived = Signal(str, str)  # (event_type, device_name)
    statusMessageChanged = Signal()
    
    def __init__(self):
        super().__init__()
        self._socket = QWebSocket()
        self._is_connected = False
        self._status_message = "未连接"
        self._server_url = "ws://127.0.0.1:8080/ws"
        self._monitor_thread = None
        self._monitor_timer = QTimer()
        self._monitor_timer.timeout.connect(self._check_usb_devices)
        self._previous_devices = set()
        self._device_cache = {}  # 缓存设备信息
        self._usb_api = USBAPI()  # USB API实例
        
        # 连接信号
        self._socket.connected.connect(self._on_connected)
        self._socket.disconnected.connect(self._on_disconnected)
        self._socket.textMessageReceived.connect(self._on_message)
        self._socket.errorOccurred.connect(self._on_error)
        
        # 启动本地USB监控
        self._start_local_monitoring()
        
        # 尝试连接远程服务器
        self.connect_to_server()
    
    def _start_local_monitoring(self):
        """启动本地USB设备监控"""
        self._monitor_timer.start(1000)  # 每1秒检查一次
        self._status_message = "正在监控USB设备..."
        self.statusMessageChanged.emit()
        print("启动本地USB设备监控")
    
    def _check_usb_devices(self):
        """检查USB设备变化"""
        try:
            current_devices = self._get_usb_devices()
            
            # 检测新插入的设备
            new_devices = current_devices - self._previous_devices
            for device in new_devices:
                device_info = self._get_device_info(device)
                print(f"🔌 检测到USB设备插入: {device_info}")
                self.usbEventReceived.emit("insert", device_info)
                self._status_message = f"USB设备插入: {device_info}"
                self.statusMessageChanged.emit()
            
            # 检测移除的设备
            removed_devices = self._previous_devices - current_devices
            for device in removed_devices:
                device_info = self._device_cache.get(device, device)
                print(f"🔌❌ 检测到USB设备移除: {device_info}")
                self.usbEventReceived.emit("remove", device_info)
                self._status_message = f"USB设备移除: {device_info}"
                self.statusMessageChanged.emit()
            
            self._previous_devices = current_devices
            
        except Exception as e:
            print(f"检查USB设备时出错: {e}")
    
    def _get_usb_devices(self):
        """获取当前USB设备列表"""
        devices = set()
        
        try:
            # 检查是否有认证token
            if not self._usb_api.token:
                # 没有token时不输出错误日志，静默处理
                return devices
            
            # 使用API接口获取USB设备列表
            result = self._usb_api.get_usb_devices()
            
            if result["success"] and result["data"]:
                usb_devices = result["data"].get("data", [])
                
                for device_info in usb_devices:
                    # 使用设备路径作为唯一标识符
                    device_path = device_info.get("device", "")
                    if device_path:
                        devices.add(device_path)
                        
                        # 缓存设备信息
                        device_name = device_info.get("label", device_info.get("device", ""))
                        self._device_cache[device_path] = device_name
                        
                        # 只在首次发现设备时输出日志
                        if device_path not in self._previous_devices:
                            print(f"发现USB设备: {device_path} - {device_name}")
            else:
                # 只在状态码不是401时输出错误日志（避免未认证时的重复日志）
                if result.get("status_code") != 401:
                    print(f"API获取USB设备失败: {result.get('error', '未知错误')}")
                
        except Exception as e:
            print(f"获取USB设备列表失败: {e}")
        
        return devices 
    def _get_device_info(self, device_id):
        """获取设备详细信息"""
        if device_id in self._device_cache:
            return self._device_cache[device_id]
        return device_id
    
    @Slot(str)
    def set_token(self, token: str):
        """设置认证token"""
        self._usb_api.set_token(token)
    
    @Slot()
    def connect_to_server(self):
        """连接到USB监控服务器"""
        if not self._is_connected:
            self._socket.open(QUrl(self._server_url))
            self._status_message = "正在连接..."
            self.statusMessageChanged.emit()
    
    @Slot()
    def disconnect_from_server(self):
        """断开与服务器的连接"""
        if self._is_connected:
            self._socket.close()
    
    def _on_connected(self):
        """连接成功回调"""
        self._is_connected = True
        self._status_message = "已连接到 USB 后台服务"
        self.connectionStatusChanged.emit()
        self.statusMessageChanged.emit()
        print("USB监控服务连接成功")
    
    def _on_disconnected(self):
        """连接断开回调"""
        self._is_connected = False
        self._status_message = "连接已断开"
        self.connectionStatusChanged.emit()
        self.statusMessageChanged.emit()
        print("USB监控服务连接断开")
    
    def _on_error(self, error):
        """连接错误回调"""
        self._is_connected = False
        self._status_message = f"连接错误: {error}"
        self.connectionStatusChanged.emit()
        self.statusMessageChanged.emit()
        print(f"USB监控服务连接错误: {error}")
    
    def _on_message(self, message):
        """接收消息回调"""
        try:
            # 尝试解析JSON消息
            data = json.loads(message)
            event_type = data.get("type", "unknown")
            device_name = data.get("device", "未知设备")
            
            # 发出USB事件信号
            self.usbEventReceived.emit(event_type, device_name)
            
            # 更新状态消息
            if event_type == "insert":
                self._status_message = f"USB设备插入: {device_name}"
            elif event_type == "remove":
                self._status_message = f"USB设备移除: {device_name}"
            else:
                self._status_message = f"USB事件: {message}"
            
            self.statusMessageChanged.emit()
            
        except json.JSONDecodeError:
            # 如果不是JSON格式，直接显示消息
            self._status_message = f"收到消息: {message}"
            self.statusMessageChanged.emit()
    
    @Slot(str)
    def set_server_url(self, url):
        """设置服务器URL"""
        if self._server_url != url:
            self._server_url = url
            if self._is_connected:
                self.disconnect_from_server()
                self.connect_to_server()
    
    @Slot()
    def reconnect(self):
        """重新连接"""
        self.disconnect_from_server()
        self.connect_to_server()
    
    @Slot()
    def refresh_devices(self):
        """手动刷新设备列表"""
        self._check_usb_devices()
    
    # 属性定义
    @Property(bool, notify=connectionStatusChanged)
    def is_connected(self):
        return self._is_connected
    
    @Property(str, notify=statusMessageChanged)
    def status_message(self):
        return self._status_message