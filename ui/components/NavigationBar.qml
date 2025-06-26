import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: navigationBar
    color: themeManager.surfaceColor

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
            color: themeManager.textPrimaryColor
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
                        color: navigationBar.currentIndex === index ? themeManager.primaryColor : "transparent"
                        border.color: navigationBar.currentIndex === index ? themeManager.primaryColor : "transparent"
                        border.width: 1
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font.pixelSize: 12
                        font.weight: Font.Medium
                        color: navigationBar.currentIndex === index ? "white" : themeManager.textSecondaryColor
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

       // 新增功能按钮区域（传输 + 全部）
        Row {
            spacing: 8
            Layout.alignment: Qt.AlignRight  // 让按钮靠右侧

            // 传输按钮，带悬停提示
            Button {
                id: transferButton
                height: 36
                width: 65 // 增加宽度以容纳文本
                padding: 8

                // 按钮背景样式
                background: Rectangle {
                    radius: 18  // 圆角
                    color: transferButton.hovered ? themeManager.primaryColor : "transparent"
                    border.color: transferButton.hovered ? themeManager.primaryColor : themeManager.textSecondaryColor
                    border.width: 1
                    
                    // 添加悬停效果
                    Behavior on color {
                        ColorAnimation { duration: 200 }
                    }
                }

                // 按钮内容
                contentItem: Row {
                    anchors.centerIn: parent
                    spacing: 4
                    
                    // 图标容器
                    Rectangle {
                        width: 20
                        height: 20
                        radius: 10
                        color: transferButton.hovered ? "white" : themeManager.primaryColor + "20"  // 半透明背景
                        
                        Row {
                            anchors.centerIn: parent
                            spacing: 1
                            
                            // 上传箭头
                            Text {
                                text: "↑"
                                font.pixelSize: 10
                                font.weight: Font.Bold
                                color: transferButton.hovered ? themeManager.primaryColor : themeManager.textPrimaryColor
                                verticalAlignment: Text.AlignVCenter
                            }
                            
                            // 下载箭头
                            Text {
                                text: "↓"
                                font.pixelSize: 10
                                font.weight: Font.Bold
                                color: transferButton.hovered ? themeManager.primaryColor : themeManager.textPrimaryColor
                                verticalAlignment: Text.AlignVCenter
                            }
                        }
                    }
                    
                    // 文本标签
                    Text {
                        text: "传输"
                        font.pixelSize: 12
                        font.weight: Font.Medium
                        color: transferButton.hovered ? "white" : themeManager.textPrimaryColor
                        verticalAlignment: Text.AlignVCenter
                    }
                }

                // 鼠标悬停提示
                ToolTip {
                    parent: transferButton
                    text: "上传/下载文件"
                    visible: transferButton.hovered
                }

                onClicked: {
                    console.log("点击了传输按钮，可在此处理上传下载逻辑");
                    // 这里可扩展实际上传下载相关业务代码，比如弹出对应窗口等
                }
            }

        }

        // 原右侧占位调整，因为上面新增了功能按钮区域，这里可去掉或者按需调整
        // Item {
        //     Layout.fillWidth: true
        // }
    }
}