import QtQuick 6.5
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 400
    height: 300
    title: "NAS 文件管理系统"
    color: "#FAFAFA"
    
    // Material Design 窗口属性
    minimumWidth: 400
    minimumHeight: 300
    
    // 设置窗口图标（如果有的话）
    // icon: "qrc:/icons/app_icon.png"

    Loader {
        anchors.fill: parent
        source: "Login.qml"  // 确保路径正确
    }
} 