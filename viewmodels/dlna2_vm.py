from PySide6.QtCore import QObject, Signal, Slot, Property
from api.dlna2_api import Dlna2API
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


class Dlna2ViewModel(QObject):
    """DLNA2设备管理ViewModel，专门处理DLNA2设备相关功能"""
    
    # 信号定义
    dlnaDevicesChanged = Signal()  # DLNA设备列表变化信号
    deviceListLoadingChanged = Signal()  # 设备列表加载状态变化信号
    playStarted = Signal(str, str)  # 播放开始信号 (file_path, device_id)
    playFinished = Signal(bool, str)  # 播放完成信号 (success, message)
    controlCommandSent = Signal(str, str)  # 控制命令发送信号 (device_id, command)
    controlResultChanged = Signal(bool, str)  # 控制结果变化信号 (success, message)
    currentDeviceChanged = Signal(str)  # 当前设备变化信号
    volumeChanged = Signal(int)  # 音量变化信号
    
    def __init__(self):
        super().__init__()
        self._dlna_api = Dlna2API()
        self._dlna_devices = []  # DLNA设备列表
        self._current_device_id = ""  # 当前选中的设备ID
        self._is_loading_devices = False  # 是否正在加载设备列表
        self._current_playing_file = ""  # 当前播放的文件路径
        self._current_volume = 50  # 当前音量（默认50%）
        self._is_playing = False  # 是否正在播放
        self._error_message = ""  # 错误信息
    
    @Slot(str)
    def set_token(self, token: str):
        """设置认证 token"""
        self._dlna_api.set_token(token)
    
    @Slot()
    def refresh_dlna_devices(self):
        """刷新DLNA设备列表"""
        self._is_loading_devices = True
        self._error_message = ""
        self.deviceListLoadingChanged.emit()
        
        try:
            devices = self._dlna_api.list_dlna2()
            if devices is not None:
                self._dlna_devices = devices
                self._error_message = ""
            else:
                self._dlna_devices = []
                self._error_message = "获取DLNA设备列表失败"
        except Exception as e:
            self._dlna_devices = []
            self._error_message = f"获取DLNA设备列表异常: {str(e)}"
        
        self._is_loading_devices = False
        self.dlnaDevicesChanged.emit()
        self.deviceListLoadingChanged.emit()
    
    @Slot(str)
    def select_device(self, device_id: str):
        """选择DLNA设备"""
        if self._current_device_id != device_id:
            self._current_device_id = device_id
            self.currentDeviceChanged.emit(device_id)
    
    @Slot(str, str)
    def play_file_on_device(self, file_path: str, device_id: str = ""):
        """在指定设备上播放文件"""
        if not file_path:
            self.playFinished.emit(False, "文件路径为空")
            return
        
        # 如果没有指定设备ID，使用当前选中的设备
        if not device_id:
            device_id = self._current_device_id
        
        if not device_id:
            self.playFinished.emit(False, "请先选择DLNA设备")
            return
        
        # 检查设备是否存在
        device_exists = any(device.get("id") == device_id for device in self._dlna_devices)
        if not device_exists:
            self.playFinished.emit(False, "指定的DLNA设备不存在")
            return
        
        self._is_playing = True
        self._current_playing_file = file_path
        self.playStarted.emit(file_path, device_id)
        
        try:
            result = self._dlna_api.play_on_dlna2(file_path, device_id)
            
            if "error" not in result:
                self.playFinished.emit(True, f"开始在设备 {device_id} 上播放文件")
            else:
                error_msg = result.get("error", "播放失败")
                self.playFinished.emit(False, f"播放失败: {error_msg}")
        except Exception as e:
            self.playFinished.emit(False, f"播放异常: {str(e)}")
        
        self._is_playing = False
        self._current_playing_file = ""
    
    @Slot(str)
    def play_file_on_current_device(self, file_path: str):
        """在当前选中的设备上播放文件"""
        self.play_file_on_device(file_path, self._current_device_id)
    
    @Slot(str)
    def pause_device(self, device_id: str = ""):
        """暂停设备播放"""
        self._send_control_command(device_id, "Pause")
    
    @Slot(str)
    def unpause_device(self, device_id: str = ""):
        """继续设备播放"""
        self._send_control_command(device_id, "Unpause")
    
    @Slot(str)
    def stop_device(self, device_id: str = ""):
        """停止设备播放"""
        self._send_control_command(device_id, "Stop")
    
    @Slot(str)
    def fast_forward_device(self, device_id: str = ""):
        """快进10秒"""
        self._send_control_command(device_id, "FastForward")
    
    @Slot(str)
    def rewind_device(self, device_id: str = ""):
        """后退10秒"""
        self._send_control_command(device_id, "Rewind")
    
    @Slot(int, str)
    def set_device_volume(self, volume: int, device_id: str = ""):
        """设置设备音量"""
        if not (0 <= volume <= 100):
            self.controlResultChanged.emit(False, "音量值必须在0-100之间")
            return
        
        self._send_control_command(device_id, "SetVolume", volume)
        self._current_volume = volume
        self.volumeChanged.emit(volume)
    
    def _send_control_command(self, device_id: str, command: str, value: int = 0):
        """发送控制命令到设备"""
        # 如果没有指定设备ID，使用当前选中的设备
        if not device_id:
            device_id = self._current_device_id
        
        if not device_id:
            self.controlResultChanged.emit(False, "请先选择DLNA设备")
            return
        
        # 检查设备是否存在
        device_exists = any(device.get("id") == device_id for device in self._dlna_devices)
        if not device_exists:
            self.controlResultChanged.emit(False, "指定的DLNA设备不存在")
            return
        
        self.controlCommandSent.emit(device_id, command)
        
        try:
            result = self._dlna_api.dlna_command2(device_id, command, value)
            
            if "error" not in result:
                command_names = {
                    "Pause": "暂停",
                    "Unpause": "继续播放",
                    "Stop": "停止",
                    "FastForward": "快进",
                    "Rewind": "后退",
                    "SetVolume": "设置音量"
                }
                command_name = command_names.get(command, command)
                self.controlResultChanged.emit(True, f"{command_name}命令执行成功")
            else:
                error_msg = result.get("error", "命令执行失败")
                self.controlResultChanged.emit(False, f"命令执行失败: {error_msg}")
        except Exception as e:
            self.controlResultChanged.emit(False, f"命令执行异常: {str(e)}")
    
    @Slot(result=list)
    def get_dlna_devices(self):
        """获取DLNA设备列表"""
        return self._dlna_devices.copy()
    
    @Slot(result=int)
    def get_device_count(self):
        """获取设备数量"""
        return len(self._dlna_devices)
    
    @Slot(result=str)
    def get_current_device_id(self):
        """获取当前选中的设备ID"""
        return self._current_device_id
    
    @Slot(result=str)
    def get_current_device_name(self):
        """获取当前选中设备的名称"""
        for device in self._dlna_devices:
            if device.get("id") == self._current_device_id:
                return device.get("name", "未知设备")
        return ""
    
    @Slot(result=bool)
    def has_devices(self):
        """检查是否有可用的DLNA设备"""
        return len(self._dlna_devices) > 0
    
    @Slot(result=bool)
    def has_selected_device(self):
        """检查是否已选择设备"""
        return bool(self._current_device_id)
    
    @Slot(result=bool)
    def can_play_file(self):
        """检查是否可以播放文件"""
        return bool(self._current_device_id) and bool(self._dlna_devices)
    
    @Slot(result=bool)
    def can_control_device(self):
        """检查是否可以控制设备"""
        return bool(self._current_device_id) and bool(self._dlna_devices)
    
    @Slot(result=str)
    def get_current_playing_file(self):
        """获取当前播放的文件路径"""
        return self._current_playing_file
    
    @Slot(result=bool)
    def is_playing(self):
        """检查是否正在播放"""
        return self._is_playing
    
    @Slot(result=str)
    def get_error_message(self):
        """获取错误信息"""
        return self._error_message
    
    @Slot()
    def clear_error_message(self):
        """清空错误信息"""
        self._error_message = ""
    
    # 属性定义
    @Property(list, notify=dlnaDevicesChanged)
    def dlna_devices(self):
        """DLNA设备列表"""
        return self._dlna_devices.copy()
    
    @Property(int, notify=dlnaDevicesChanged)
    def device_count(self):
        """设备数量"""
        return len(self._dlna_devices)
    
    @Property(str, notify=currentDeviceChanged)
    def current_device_id(self):
        """当前选中的设备ID"""
        return self._current_device_id
    
    @Property(str, notify=currentDeviceChanged)
    def current_device_name(self):
        """当前选中设备的名称"""
        for device in self._dlna_devices:
            if device.get("id") == self._current_device_id:
                return device.get("name", "未知设备")
        return ""
    
    @Property(bool, notify=deviceListLoadingChanged)
    def is_loading_devices(self):
        """是否正在加载设备列表"""
        return self._is_loading_devices
    
    @Property(bool, notify=dlnaDevicesChanged)
    def has_devices_available(self):
        """是否有可用的DLNA设备"""
        return len(self._dlna_devices) > 0
    
    @Property(bool, notify=currentDeviceChanged)
    def has_device_selected(self):
        """是否已选择设备"""
        return bool(self._current_device_id)
    
    @Property(bool, notify=dlnaDevicesChanged)
    def can_play_files(self):
        """是否可以播放文件"""
        return bool(self._current_device_id) and bool(self._dlna_devices)
    
    @Property(bool, notify=dlnaDevicesChanged)
    def can_control_devices(self):
        """是否可以控制设备"""
        return bool(self._current_device_id) and bool(self._dlna_devices)
    
    @Property(str, notify=playStarted)
    def current_playing_file(self):
        """当前播放的文件路径"""
        return self._current_playing_file
    
    @Property(bool, notify=playStarted)
    def is_currently_playing(self):
        """是否正在播放"""
        return self._is_playing
    
    @Property(int, notify=volumeChanged)
    def current_volume(self):
        """当前音量"""
        return self._current_volume
    
    @Property(str, notify=dlnaDevicesChanged)
    def error_message(self):
        """错误信息"""
        return self._error_message