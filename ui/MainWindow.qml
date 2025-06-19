import QtQuick 6.5
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: "NAS 文件管理系统"
    color: "#FAFAFA"
    
    // Material Design 窗口属性
    minimumWidth: 800
    minimumHeight: 600
    
    // 设置窗口图标（如果有的话）
    // icon: "qrc:/icons/app_icon.png"

    // 页面加载器，支持页面切换
    Loader {
        id: mainPageLoader
        anchors.fill: parent
        source: "Login.qml"
        
        // 监听登录成功信号
        onItemChanged: {
            if (item && item.loginSuccess) {
                item.loginSuccess.connect(function() {
                    mainPageLoader.source = "MainPage.qml"
                })
            }
        }
    }
} 