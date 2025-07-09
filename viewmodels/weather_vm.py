from PySide6.QtCore import QObject, Property, Signal
from datetime import datetime

class WeatherViewModel(QObject):
    # 定义属性变化信号（如果以后想动态更新界面）
    weatherChanged = Signal()
    cityChanged = Signal()
    dateChanged = Signal()
    timeChanged = Signal()
    tempRangeChanged = Signal()

    def __init__(self, weather_data):
        super().__init__()

        # 从 dict 拿数据
        self._weather = weather_data.get("weather", "")
        self._city = weather_data.get("city", "")
        self._date = weather_data.get("date", "")
        self._time = weather_data.get("time", "")
        self._tempRange = weather_data.get("tempRange", "")

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

    weather = Property(str, fget=get_weather, notify=weatherChanged)
    city = Property(str, fget=get_city, notify=cityChanged)
    date = Property(str, fget=get_date, notify=dateChanged)
    time = Property(str, fget=get_time, notify=timeChanged)
    tempRange = Property(str, fget=get_tempRange, notify=tempRangeChanged)

    
