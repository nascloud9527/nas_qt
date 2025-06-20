import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Dialog {
    id: messageDialog
    modal: true
    anchors.centerIn: parent
    width: 300
    height: 150
    
    property string title: "消息"
    property string message: ""
    property string type: "info" // success, error, info
    
    background: Rectangle {
        radius: 8
        color: themeManager.surfaceColor
        border.color: themeManager.dividerColor
        border.width: 1
    }
    
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 12
        
        // 标题和图标
        RowLayout {
            Layout.fillWidth: true
            spacing: 8
            
            Text {
                text: type === "success" ? "✅" : type === "error" ? "❌" : "ℹ️"
                font.pixelSize: 20
            }
            
            Text {
                text: title
                font.pixelSize: 16
                font.weight: Font.Bold
                color: themeManager.textPrimaryColor
                Layout.fillWidth: true
            }
        }
        
        // 消息内容
        Text {
            text: message
            font.pixelSize: 14
            color: themeManager.textSecondaryColor
            wrapMode: Text.WordWrap
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
        
        // 确定按钮
        Button {
            text: "确定"
            Layout.alignment: Qt.AlignRight
            Layout.preferredWidth: 80
            Layout.preferredHeight: 32
            
            background: Rectangle {
                radius: 16
                color: parent.pressed ? themeManager.primaryDarkColor : themeManager.primaryColor
                border.color: "#40000000"
                border.width: 1
            }
            
            contentItem: Text {
                text: parent.text
                font.pixelSize: 12
                font.weight: Font.Medium
                color: "white"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            
            onClicked: {
                messageDialog.close()
            }
        }
    }
    
    // 3秒后自动关闭
    Timer {
        interval: 3000
        running: messageDialog.visible
        onTriggered: {
            messageDialog.close()
        }
    }
} 