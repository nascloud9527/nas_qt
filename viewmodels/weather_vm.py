from PySide6.QtCore import QObject, Property, Signal, Slot
from datetime import datetime
from viewmodels.weather_data_vm import WeatherDataVM

class WeatherViewModel(QObject):
    # 定义属性变化信号（如果以后想动态更新界面）
    weatherChanged = Signal()
    cityChanged = Signal()
    dateChanged = Signal()
    timeChanged = Signal()
    tempRangeChanged = Signal()
    weatherDataLoaded = Signal()  # 新增：天气数据加载完成信号

    def __init__(self, weather_data=None):
        super().__init__()
        
        # 初始化天气数据服务
        self._weather_data_vm = None
        self._is_loaded = False
        
        # 从 dict 拿数据
        if weather_data:
            self._weather = weather_data.get("weather", "")
            self._city = weather_data.get("city", "")
            self._date = weather_data.get("date", "")
            self._time = weather_data.get("time", "")
            self._tempRange = weather_data.get("tempRange", "")
        else:
            # 默认值
            self._weather = "未知"
            self._city = ""
            self._date = ""
            self._time = ""
            self._tempRange = ""

    @Slot(str)
    def initialize_weather_service(self, api_key: str):
        """初始化天气服务"""
        self._weather_data_vm = WeatherDataVM(api_key)
        print("天气服务已初始化")

    @Slot()
    def load_weather_data(self):
        """加载天气数据"""
        if not self._weather_data_vm:
            print("天气服务未初始化")
            return
        
        print("开始获取天气数据...")
        try:
            weather_data = self._weather_data_vm.create_weather_data()
            
            # 更新天气数据
            self._weather = weather_data.get("weather", "")
            self._city = weather_data.get("city", "")
            self._date = weather_data.get("date", "")
            self._time = weather_data.get("time", "")
            self._tempRange = weather_data.get("tempRange", "")
            
            self._is_loaded = True
            
            # 发送信号通知数据更新
            self.weatherChanged.emit()
            self.cityChanged.emit()
            self.dateChanged.emit()
            self.timeChanged.emit()
            self.tempRangeChanged.emit()
            self.weatherDataLoaded.emit()
            
            print(f"天气数据加载完成: {self._city} {self._weather} {self._tempRange}")
            
        except Exception as e:
            print(f"获取天气数据失败: {str(e)}")
            # 设置默认值
            self._weather = "未知"
            self._city = "获取失败"
            self._tempRange = ""
            self.weatherChanged.emit()
            self.cityChanged.emit()
            self.tempRangeChanged.emit()

    def get_weather(self):
        return self._weather

    def get_city(self):
        return self._city

    def get_date(self):
        return self._date

    def get_time(self):
        return self._time

    def get_tempRange(self):
        return self._tempRange

    def get_is_loaded(self):
        return self._is_loaded

    weather = Property(str, fget=get_weather, notify=weatherChanged)
    city = Property(str, fget=get_city, notify=cityChanged)
    date = Property(str, fget=get_date, notify=dateChanged)
    time = Property(str, fget=get_time, notify=timeChanged)
    tempRange = Property(str, fget=get_tempRange, notify=tempRangeChanged)
    isLoaded = Property(bool, fget=get_is_loaded, notify=weatherDataLoaded)

    
