import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: navigationBar
    color: surfaceColor

    property color primaryColor: "#2196F3"
    property color textPrimaryColor: "#212121"
    property color textSecondaryColor: "#757575"
    property color surfaceColor: "#FFFFFF"
    property int currentIndex: 0

    RowLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 24

        // 系统标题
        Text {
            text: "NAS 文件管理系统"
            font.pixelSize: 18
            font.weight: Font.Medium
            color: textPrimaryColor
            Layout.preferredWidth: 200
        }

        // 功能导航按钮
        Row {
            spacing: 8

            Repeater {
                model: ["全部", "最近", "视频", "图片", "文档"]
                
                Button {
                    text: modelData
                    height: 32
                    padding: 8
                    
                    background: Rectangle {
                        radius: 16
                        color: navigationBar.currentIndex === index ? primaryColor : "transparent"
                        border.color: navigationBar.currentIndex === index ? primaryColor : "transparent"
                        border.width: 1
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font.pixelSize: 12
                        font.weight: Font.Medium
                        color: navigationBar.currentIndex === index ? "white" : textSecondaryColor
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        navigationBar.currentIndex = index
                        console.log("切换到:", modelData)
                    }
                }
            }
        }

        // 右侧占位
        Item {
            Layout.fillWidth: true
        }
    }
} 