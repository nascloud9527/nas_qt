from PySide6.QtCore import QObject, Property, Signal, Slot, QThread, QThreadPool, QRunnable
from datetime import datetime
from viewmodels.weather_data_vm import WeatherDataVM

class WeatherWorker(QRunnable):
    """天气数据获取工作线程"""
    
    def __init__(self, weather_data_vm, callback):
        super().__init__()
        self.weather_data_vm = weather_data_vm
        self.callback = callback
    
    def run(self):
        """在工作线程中执行天气数据获取"""
        try:
            weather_data = self.weather_data_vm.create_weather_data()
            # 通过回调函数将结果传回主线程
            self.callback.emit(weather_data)
        except Exception as e:
            print(f"天气数据获取失败: {str(e)}")
            # 发送错误数据
            error_data = {
                "weather": "未知",
                "city": "获取失败",
                "date": "",
                "time": "",
                "tempRange": ""
            }
            self.callback.emit(error_data)

class WeatherViewModel(QObject):
    # 定义属性变化信号（如果以后想动态更新界面）
    weatherChanged = Signal()
    cityChanged = Signal()
    dateChanged = Signal()
    timeChanged = Signal()
    tempRangeChanged = Signal()
    weatherDataLoaded = Signal()  # 新增：天气数据加载完成信号
    weatherDataReceived = Signal(dict)  # 新增：接收天气数据的信号

    def __init__(self, weather_data=None):
        super().__init__()
        
        # 初始化天气数据服务
        self._weather_data_vm = None
        self._is_loading = False
        self._is_loaded = False
        
        # 连接信号
        self.weatherDataReceived.connect(self._on_weather_data_received)
        
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
        """异步加载天气数据"""
        if not self._weather_data_vm:
            print("天气服务未初始化")
            return
        
        if self._is_loading:
            print("天气数据正在加载中，跳过重复请求")
            return
        
        print("开始异步获取天气数据...")
        self._is_loading = True
        
        # 创建工作线程
        worker = WeatherWorker(self._weather_data_vm, self.weatherDataReceived)
        
        # 获取线程池并启动工作线程
        thread_pool = QThreadPool.globalInstance()
        thread_pool.start(worker)

    @Slot(dict)
    def _on_weather_data_received(self, weather_data):
        """接收天气数据并更新UI"""
        print("接收到天气数据，更新UI...")
        
        # 更新天气数据
        self._weather = weather_data.get("weather", "")
        self._city = weather_data.get("city", "")
        self._date = weather_data.get("date", "")
        self._time = weather_data.get("time", "")
        self._tempRange = weather_data.get("tempRange", "")
        
        self._is_loading = False
        self._is_loaded = True
        
        # 发送信号通知数据更新
        self.weatherChanged.emit()
        self.cityChanged.emit()
        self.dateChanged.emit()
        self.timeChanged.emit()
        self.tempRangeChanged.emit()
        self.weatherDataLoaded.emit()
        
        print(f"天气数据更新完成: {self._city} {self._weather} {self._tempRange}")

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
    
    def get_is_loading(self):
        return self._is_loading

    weather = Property(str, fget=get_weather, notify=weatherChanged)
    city = Property(str, fget=get_city, notify=cityChanged)
    date = Property(str, fget=get_date, notify=dateChanged)
    time = Property(str, fget=get_time, notify=timeChanged)
    tempRange = Property(str, fget=get_tempRange, notify=tempRangeChanged)
    isLoaded = Property(bool, fget=get_is_loaded, notify=weatherDataLoaded)
    isLoading = Property(bool, fget=get_is_loading, notify=weatherDataLoaded)

    
