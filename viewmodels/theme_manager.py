from PySide6.QtCore import QObject, Signal, Property, Slot

class ThemeManager(QObject):
    themeChanged = Signal()
    
    def __init__(self):
        super().__init__()
        self._isDarkTheme = False
        
        # 浅色主题颜色
        self._lightTheme = {
            "backgroundColor": "#FAFAFA",
            "surfaceColor": "#FFFFFF",
            "primaryColor": "#2196F3",
            "primaryDarkColor": "#1976D2",
            "accentColor": "#FF4081",
            "textPrimaryColor": "#212121",
            "textSecondaryColor": "#757575",
            "dividerColor": "#BDBDBD",
            "hoverColor": "#F0F0F0",
            "errorColor": "#F44336",
            "successColor": "#4CAF50",
            "warningColor": "#FF9800"
        }
        
        # 深色主题颜色
        self._darkTheme = {
            "backgroundColor": "#121212",
            "surfaceColor": "#1E1E1E",
            "primaryColor": "#BB86FC",
            "primaryDarkColor": "#9B6BDF",
            "accentColor": "#03DAC6",
            "textPrimaryColor": "#FFFFFF",
            "textSecondaryColor": "#B3B3B3",
            "dividerColor": "#424242",
            "hoverColor": "#2D2D2D",
            "errorColor": "#CF6679",
            "successColor": "#4CAF50",
            "warningColor": "#FFB74D"
        }
    
    def getColor(self, colorName):
        """获取当前主题下的颜色"""
        theme = self._darkTheme if self._isDarkTheme else self._lightTheme
        return theme.get(colorName, "#000000")
    
    @Slot()
    def toggleTheme(self):
        """切换主题"""
        self._isDarkTheme = not self._isDarkTheme
        self.themeChanged.emit()
    
    @Property(bool, notify=themeChanged)
    def isDarkTheme(self):
        return self._isDarkTheme
    
    @Property(str, notify=themeChanged)
    def backgroundColor(self):
        return self.getColor("backgroundColor")
    
    @Property(str, notify=themeChanged)
    def surfaceColor(self):
        return self.getColor("surfaceColor")
    
    @Property(str, notify=themeChanged)
    def primaryColor(self):
        return self.getColor("primaryColor")
    
    @Property(str, notify=themeChanged)
    def primaryDarkColor(self):
        return self.getColor("primaryDarkColor")
    
    @Property(str, notify=themeChanged)
    def accentColor(self):
        return self.getColor("accentColor")
    
    @Property(str, notify=themeChanged)
    def textPrimaryColor(self):
        return self.getColor("textPrimaryColor")
    
    @Property(str, notify=themeChanged)
    def textSecondaryColor(self):
        return self.getColor("textSecondaryColor")
    
    @Property(str, notify=themeChanged)
    def dividerColor(self):
        return self.getColor("dividerColor")
    
    @Property(str, notify=themeChanged)
    def hoverColor(self):
        return self.getColor("hoverColor")
    
    @Property(str, notify=themeChanged)
    def errorColor(self):
        return self.getColor("errorColor")
    
    @Property(str, notify=themeChanged)
    def successColor(self):
        return self.getColor("successColor")
    
    @Property(str, notify=themeChanged)
    def warningColor(self):
        return self.getColor("warningColor") 