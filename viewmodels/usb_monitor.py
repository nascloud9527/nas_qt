from PySide6.QtCore import QObject, Signal, Slot, Property, QUrl, QTimer
from PySide6.QtWebSockets import QWebSocket
import json
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
        self._socket = QWebSocket()
        self._is_connected = False
        self._status_message = "未连接"
        self._server_url = "ws://localhost:8080/ws"
        self._usb_api = USBAPI()  # USB API实例
        
        # 添加重连定时器
        self._reconnect_timer = QTimer()
        self._reconnect_timer.timeout.connect(self.connect_to_server)
        self._reconnect_timer.setInterval(5000)  # 5秒
        
        # 连接信号
        self._socket.connected.connect(self._on_connected)
        self._socket.disconnected.connect(self._on_disconnected)
        self._socket.textMessageReceived.connect(self._on_message)
        self._socket.errorOccurred.connect(self._on_error)
        
        # 尝试连接远程服务器
        self.connect_to_server()
    
    def _handle_usb_event(self, event_type, device_id, device_info):
        """处理USB事件"""
        event_text = "插入" if event_type == "insert" else "移除"

        self.usbEventReceived.emit(event_type, device_info)
        self._update_status(f"USB设备{event_text}: {device_info}")
    
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
        """连接到USB监控服务器"""
        if not self._is_connected:
            self._socket.open(QUrl(self._server_url))
            self._update_status("正在连接...")
    
    @Slot()
    def disconnect_from_server(self):
        """断开与服务器的连接"""
        if self._is_connected:
            self._socket.close()
    
    def _on_connected(self):
        """连接成功回调"""
        self._is_connected = True
        self._update_status("已连接到 USB 后台服务")
        self.connectionStatusChanged.emit()
        print("USB监控服务连接成功")
        # 连接成功后停止重连定时器
        self._reconnect_timer.stop()
    
    def _on_disconnected(self):
        """连接断开回调"""
        self._is_connected = False
        self._update_status("连接已断开，5秒后尝试重新连接...")
        self.connectionStatusChanged.emit()
        print("USB监控服务连接断开，5秒后尝试重新连接...")
        # 启动重连定时器
        self._reconnect_timer.start()
    
    def _on_error(self, error):
        """连接错误回调"""
        self._is_connected = False
        self._update_status(f"连接错误: {error}")
        self.connectionStatusChanged.emit()
        print(f"USB监控服务连接错误: {error}")
        # 启动重连定时器
        self._reconnect_timer.start()
    
    def _on_message(self, message):
        """接收消息回调"""
        try:
            # print(f"收到WebSocket消息: {message}")
            # 尝试解析JSON消息
            data = json.loads(message)
            event_type = data.get("type", "unknown")
            device_name = data.get("device", "未知设备")
            
            # print(f"解析后的消息 - 事件类型: {event_type}, 设备名称: {device_name}")
            
            if event_type in ["insert", "remove"]:
                # print(f"触发USB事件信号: {event_type}, {device_name}")
                self._handle_usb_event(event_type, None, device_name)
            else:
                # print(f"未知USB事件类型: {event_type}")
                self._update_status(f"未知USB事件: {message}")
            
        except json.JSONDecodeError as e:
            # print(f"JSON解析错误，尝试解析纯文本消息: {e}")
            # 如果不是JSON格式，尝试解析纯文本消息
            self._parse_text_message(message)
        except Exception as e:
            # print(f"处理WebSocket消息时出错: {e}")
            self._update_status(f"消息处理错误: {str(e)}")
    
    def _parse_text_message(self, message):
        """解析纯文本格式的USB事件消息"""
        try:
            # print(f"解析纯文本消息: {message}")
            
            # 根据消息内容判断事件类型
            if "❌ 移除设备:" in message:
                # 移除设备消息
                device_name = message.split("❌ 移除设备:")[1].strip()
                # print(f"检测到设备移除事件: {device_name}")
                self._handle_usb_event("remove", None, device_name)
            elif "📦 插入设备:" in message:
                # 插入设备消息
                device_part = message.split("📦 插入设备:")[1].strip()
                # 处理可能包含容量信息的设备名称
                if "(" in device_part:
                    device_name = device_part.split("(")[0].strip()
                else:
                    device_name = device_part
                # print(f"检测到设备插入事件: {device_name}")
                self._handle_usb_event("insert", None, device_name)
            else:
                # print(f"无法识别的消息格式: {message}")
                self._update_status(f"收到消息: {message}")
                
        except Exception as e:
            # print(f"解析纯文本消息时出错: {e}")
            self._update_status(f"收到消息: {message}")
    
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
    
    # 属性定义
    @Property(bool, notify=connectionStatusChanged)
    def is_connected(self):
        return self._is_connected
    
    @Property(str, notify=statusMessageChanged)
    def status_message(self):
        return self._status_message