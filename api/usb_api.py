import dbus
import dbus.mainloop.glib
from gi.repository import GLib
from typing import Optional, Dict, List
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import config

class USBAPI:
    def __init__(self):
        # 初始化D-Bus主循环
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        
        # 连接到系统总线
        self.bus = dbus.SystemBus()
        
        # 初始化服务状态
        self._service_available = False
        self.usb_proxy = None
        self.usb_interface = None
        
        # 存储设备信息和事件回调
        self.devices = {}
        self.event_callbacks = []
        
        # 启动主循环
        self.mainloop = GLib.MainLoop()
        self._is_running = False
        
        # 尝试连接D-Bus服务
        self._try_connect_service()
        
    def _try_connect_service(self):
        """尝试连接D-Bus服务"""
        try:
            # 检查服务是否可用
            if self.bus.name_has_owner("org.example.USBDeviceMonitor"):
                # 获取D-Bus服务代理
                self.usb_proxy = self.bus.get_object(
                    "org.example.USBDeviceMonitor", 
                    "/org/example/USBDeviceMonitor"
                )
                
                # 获取接口
                self.usb_interface = dbus.Interface(
                    self.usb_proxy, 
                    dbus_interface="org.example.USBDeviceMonitor"
                )
                
                # 注册信号回调
                self.bus.add_signal_receiver(
                    self._device_event_handler,
                    signal_name="SendMessage",
                    dbus_interface="org.example.USBDeviceMonitor"
                )
                
                self._service_available = True
                print("D-Bus服务连接成功")
            else:
                self._service_available = False
                print("D-Bus服务不可用: org.example.USBDeviceMonitor")
                
        except Exception as e:
            self._service_available = False
            print(f"D-Bus服务连接失败: {e}")
    
    def is_service_available(self) -> bool:
        """检查D-Bus服务是否可用"""
        return self._service_available
    
    def start_monitoring(self):
        """开始监听USB设备事件"""
        if not self._service_available:
            print("D-Bus服务不可用，无法开始监听")
            return False
            
        if not self._is_running:
            self._is_running = True
            try:
                self.mainloop.run()
                return True
            except Exception as e:
                print(f"启动监听失败: {e}")
                self._is_running = False
                return False
        return True
    
    def stop_monitoring(self):
        """停止监听USB设备事件"""
        if self._is_running:
            self._is_running = False
            try:
                self.mainloop.quit()
                return True
            except Exception as e:
                print(f"停止监听失败: {e}")
                return False
        return True
    
    def add_event_callback(self, callback):
        """添加设备事件回调函数"""
        self.event_callbacks.append(callback)
    
    def _device_event_handler(self, message):
        print(f"[DBus信号] 收到消息: {message}")
        
        event_type = None
        device_info = {}

        if message.startswith("📦 插入设备:"):
            event_type = "mount"
            content = message.replace("📦 插入设备:", "").strip()
            device_info["device"] = content
        elif message.startswith("❌ 移除设备:"):
            event_type = "unmount"
            content = message.replace("❌ 移除设备:", "").strip()
            device_info["device"] = content
        else:
            print(f"[DBus信号] 无法解析消息: {message}")
            return

        # 更新内部设备字典
        if event_type == "mount":
            self.devices[device_info["device"]] = device_info
        elif event_type == "unmount":
            if device_info["device"] in self.devices:
                del self.devices[device_info["device"]]

        # 调用所有注册的回调
        for callback in self.event_callbacks:
            callback(event_type, device_info)

    def get_usb_devices(self) -> Dict:
        """
        获取已挂载的USB设备列表
        
        Returns:
            Dict: 包含USB设备列表的响应数据
        """
        if not self._service_available:
            return {
                "success": False,
                "status_code": 503,
                "data": None,
                "error": "D-Bus服务不可用"
            }
            
        try:
            # 调用D-Bus方法获取设备列表
            devices = self.usb_interface.GetMountedDevices()
            return {
                "success": True,
                "status_code": 200,
                "data": list(devices),
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "status_code": 500,
                "data": None,
                "error": str(e)
            }
    
    def get_usb_info(self) -> Dict:
        """
        获取USB挂载信息
        
        Returns:
            Dict: 包含USB挂载信息的响应数据
        """
        if not self._service_available:
            return {
                "success": False,
                "status_code": 503,
                "data": None,
                "error": "D-Bus服务不可用"
            }
            
        try:
            # 调用D-Bus方法获取设备信息
            info = self.usb_interface.GetDeviceInfo()
            return {
                "success": True,
                "status_code": 200,
                "data": dict(info),
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "status_code": 500,
                "data": None,
                "error": str(e)
            }
    
    def set_token(self, token: str):
        """设置认证token（如果需要的话）"""
        # 这里可以根据需要实现token设置逻辑
        pass