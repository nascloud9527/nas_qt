import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: toolBar
    color: themeManager.surfaceColor

    RowLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 12

        // 上传文件按钮
        Button {
            text: "上传文件"
            Layout.preferredWidth: 100
            Layout.preferredHeight: 36
            
            background: Rectangle {
                radius: 18
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
                console.log("点击上传文件")
            }
        }

        // 新建文件按钮
        Button {
            text: "新建文件"
            Layout.preferredWidth: 100
            Layout.preferredHeight: 36
            
            background: Rectangle {
                radius: 18
                color: parent.pressed ? themeManager.hoverColor : themeManager.backgroundColor
                border.color: themeManager.dividerColor
                border.width: 1
            }
            
            contentItem: Text {
                text: parent.text
                font.pixelSize: 12
                font.weight: Font.Medium
                color: themeManager.textPrimaryColor
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            
            onClicked: {
                console.log("点击新建文件")
            }
        }

        // 右侧占位
        Item {
            Layout.fillWidth: true
        }
    }
} 