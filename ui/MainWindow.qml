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
                    // 设置 token 和用户名
                    fileVM.set_token(loginVM.get_token())
                    fileVM.set_username(loginVM.get_username())
                    
                    // 加载文件列表（使用用户名作为目录）
                    fileVM.load_file_list("")
                    
                    // 切换到主页面
                    mainPageLoader.source = "MainPage.qml"
                })
            }
        }
    }
    
    // USB通知组件
    USBNotification {
        id: usbNotification
        z: 1000 // 确保在最顶层显示
    }
    
    // 确保对象在页面切换时保持可用
    Component.onCompleted: {
        // 确保fileVM和themeManager在全局上下文中可用
        if (fileVM) {
            console.log("fileVM 已注册")
        }
        if (themeManager) {
            console.log("themeManager 已注册")
        }
        if (usbMonitor) {
            console.log("usbMonitor 已注册")
            
            // 连接USB事件信号
            usbMonitor.usbEventReceived.connect(function(eventType, deviceName) {
                console.log("USB事件:", eventType, deviceName)
                usbNotification.show(deviceName, eventType)
            })
        }
    }
} 