import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: usbNotification
    width: 300
    height: 120
    radius: 8
    color: "#FFFFFF"
    border.color: "#E0E0E0"
    border.width: 1
    
    // 简单的阴影效果（不使用QtGraphicalEffects）
    Rectangle {
        anchors.fill: parent
        anchors.margins: 2
        radius: 6
        color: "#20000000"
        z: -1
    }
    
    // 动画属性
    property bool isVisible: false
    property string deviceName: ""
    property string eventType: ""
    
    // 位置：右上角
    anchors {
        right: parent.right
        top: parent.top
        margins: 20
    }
    
    // 显示/隐藏动画
    states: [
        State {
            name: "visible"
            when: isVisible
            PropertyChanges {
                target: usbNotification
                opacity: 1.0
                y: 0
            }
        },
        State {
            name: "hidden"
            when: !isVisible
            PropertyChanges {
                target: usbNotification
                opacity: 0.0
                y: -20
            }
        }
    ]
    
    transitions: [
        Transition {
            from: "hidden"
            to: "visible"
            NumberAnimation {
                properties: "opacity,y"
                duration: 300
                easing.type: Easing.OutCubic
            }
        },
        Transition {
            from: "visible"
            to: "hidden"
            NumberAnimation {
                properties: "opacity,y"
                duration: 200
                easing.type: Easing.InCubic
            }
        }
    ]
    
    // 初始状态
    Component.onCompleted: {
        opacity: 0.0
        y: -20
    }
    
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 8
        
        // 标题栏
        RowLayout {
            Layout.fillWidth: true
            spacing: 8
            
            // USB图标
            Rectangle {
                width: 24
                height: 24
                radius: 12
                color: eventType === "insert" ? "#4CAF50" : "#F44336"
                
                Text {
                    anchors.centerIn: parent
                    text: eventType === "insert" ? "✓" : "✗"
                    color: "white"
                    font.pixelSize: 14
                    font.bold: true
                }
            }
            
            // 标题
            Text {
                text: eventType === "insert" ? "USB设备插入" : "USB设备移除"
                font.pixelSize: 16
                font.bold: true
                color: "#333333"
                Layout.fillWidth: true
            }
            
            // 关闭按钮
            Button {
                width: 20
                height: 20
                background: Rectangle {
                    color: "transparent"
                }
                
                Text {
                    anchors.centerIn: parent
                    text: "×"
                    font.pixelSize: 16
                    color: "#999999"
                }
                
                onClicked: {
                    usbNotification.hide()
                }
            }
        }
        
        // 设备名称
        Text {
            text: deviceName || "未知设备"
            font.pixelSize: 14
            color: "#666666"
            Layout.fillWidth: true
            wrapMode: Text.WordWrap
        }
        
        // 时间戳
        Text {
            text: new Date().toLocaleTimeString()
            font.pixelSize: 12
            color: "#999999"
            Layout.fillWidth: true
        }
    }
    
    // 自动隐藏定时器
    Timer {
        id: autoHideTimer
        interval: 5000 // 5秒后自动隐藏
        repeat: false
        onTriggered: {
            usbNotification.hide()
        }
    }
    
    // 显示通知
    function show(device, type) {
        deviceName = device
        eventType = type
        isVisible = true
        autoHideTimer.start()
    }
    
    // 隐藏通知
    function hide() {
        isVisible = false
        autoHideTimer.stop()
    }
} 