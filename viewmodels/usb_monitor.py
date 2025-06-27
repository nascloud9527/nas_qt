from PySide6.QtCore import QObject, Signal, Slot, Property, QTimer
import sys
import os

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
        self._is_connected = False
        self._status_message = "未连接"
        self._usb_api = USBAPI()  # USB API实例
        
        # 添加重连定时器
        self._reconnect_timer = QTimer()
        self._reconnect_timer.timeout.connect(self.connect_to_server)
        self._reconnect_timer.setInterval(5000)  # 5秒
        
        # 注册D-Bus事件回调
        self._usb_api.add_event_callback(self._on_dbus_event)
        
        # 尝试连接D-Bus服务
        self.connect_to_server()
    
    def _handle_usb_event(self, event_type, device_info):
        """处理USB事件"""
        event_text = "插入" if event_type == "mount" else "移除"
        
        # 从设备信息中提取设备名称
        device_name = device_info.get("device", "未知设备") if isinstance(device_info, dict) else str(device_info)
        
        self.usbEventReceived.emit(event_type, device_name)
        self._update_status(f"USB设备{event_text}: {device_name}")
    
    def _on_dbus_event(self, event_type, device_info):
        """D-Bus事件回调"""
        try:
            print(f"D-Bus事件: {event_type}, 设备信息: {device_info}")
            self._handle_usb_event(event_type, device_info)
        except Exception as e:
            print(f"处理D-Bus事件时出错: {e}")
            self._update_status(f"D-Bus事件处理错误: {str(e)}")
    
    def _update_status(self, message):
        """更新状态消息并发送信号"""
        self._status_message = message
        self.statusMessageChanged.emit()
    
    @Slot(str)
    def set_token(self, token: str):
        """设置认证token"""
        self._usb_api.set_token(token)
    
    @Slot()
    def connect_to_server(self):
        """连接到USB监控服务（D-Bus）"""
        try:
            if not self._is_connected:
                # 检查D-Bus服务是否可用
                if not self._usb_api.is_service_available():
                    self._is_connected = False
                    self._update_status("D-Bus服务不可用，请确保USB监控服务已启动")
                    self.connectionStatusChanged.emit()
                    print("D-Bus服务不可用，5秒后尝试重新连接...")
                    # 启动重连定时器
                    self._reconnect_timer.start()
                    return
                
                # 尝试获取设备列表来测试连接
                result = self._usb_api.get_usb_devices()
                if result["success"]:
                    self._is_connected = True
                    self._update_status("已连接到 USB D-Bus 服务")
                    self.connectionStatusChanged.emit()
                    print("USB D-Bus 服务连接成功")
                    # 连接成功后停止重连定时器
                    self._reconnect_timer.stop()
                else:
                    self._is_connected = False
                    self._update_status(f"连接失败: {result.get('error', '未知错误')}")
                    self.connectionStatusChanged.emit()
                    # 启动重连定时器
                    self._reconnect_timer.start()
        except Exception as e:
            self._is_connected = False
            self._update_status(f"连接错误: {str(e)}")
            self.connectionStatusChanged.emit()
            print(f"USB D-Bus 服务连接错误: {e}")
            # 启动重连定时器
            self._reconnect_timer.start()
    
    @Slot()
    def disconnect_from_server(self):
        """断开与服务器的连接"""
        if self._is_connected:
            try:
                self._usb_api.stop_monitoring()
                self._is_connected = False
                self._update_status("已断开连接")
                self.connectionStatusChanged.emit()
            except Exception as e:
                print(f"断开连接时出错: {e}")
    
    @Slot()
    def start_monitoring(self):
        """开始监听USB设备事件"""
        if not self._usb_api.is_service_available():
            self._update_status("D-Bus服务不可用，无法开始监听")
            return
            
        try:
            success = self._usb_api.start_monitoring()
            if success:
                self._update_status("开始监听USB设备事件")
            else:
                self._update_status("启动监听失败")
        except Exception as e:
            self._update_status(f"启动监听失败: {str(e)}")
    
    @Slot()
    def stop_monitoring(self):
        """停止监听USB设备事件"""
        try:
            success = self._usb_api.stop_monitoring()
            if success:
                self._update_status("停止监听USB设备事件")
            else:
                self._update_status("停止监听失败")
        except Exception as e:
            self._update_status(f"停止监听失败: {str(e)}")
    
    @Slot()
    def check_service_status(self):
        """检查D-Bus服务状态"""
        is_available = self._usb_api.is_service_available()
        if is_available:
            self._update_status("D-Bus服务可用")
        else:
            self._update_status("D-Bus服务不可用")
        return is_available
    
    @Slot()
    def reconnect(self):
        """重新连接"""
        self.disconnect_from_server()
        self.connect_to_server()
    
    @Slot()
    def get_usb_devices(self):
        """获取USB设备列表"""
        try:
            result = self._usb_api.get_usb_devices()
            if result["success"]:
                self._update_status(f"获取到 {len(result['data'])} 个USB设备")
                return result["data"]
            else:
                self._update_status(f"获取USB设备失败: {result.get('error', '未知错误')}")
                return []
        except Exception as e:
            self._update_status(f"获取USB设备时出错: {str(e)}")
            return []
    
    @Slot()
    def get_usb_info(self):
        """获取USB设备信息"""
        try:
            result = self._usb_api.get_usb_info()
            if result["success"]:
                self._update_status("获取USB设备信息成功")
                return result["data"]
            else:
                self._update_status(f"获取USB设备信息失败: {result.get('error', '未知错误')}")
                return {}
        except Exception as e:
            self._update_status(f"获取USB设备信息时出错: {str(e)}")
            return {}
    
    # 属性定义
    @Property(bool, notify=connectionStatusChanged)
    def is_connected(self):
        return self._is_connected
    
    @Property(str, notify=statusMessageChanged)
    def status_message(self):
        return self._status_message