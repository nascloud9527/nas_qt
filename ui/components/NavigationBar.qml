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
                height: 32
                width: 32
                padding: 4

                background: Rectangle {
                    radius: 16
                    color: "transparent"
                    border.color: themeManager.textSecondaryColor
                    border.width: 1
                }

                contentItem: Row {
                    spacing: 2
                    anchors.centerIn: parent
                    
                    // 上传箭头
                    Text {
                        text: "↑"
                        font.pixelSize: 14
                        font.weight: Font.Bold
                        color: themeManager.textPrimaryColor
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    // 下载箭头
                    Text {
                        text: "↓"
                        font.pixelSize: 14
                        font.weight: Font.Bold
                        color: themeManager.textPrimaryColor
                        verticalAlignment: Text.AlignVCenter
                    }
                }

                // 鼠标悬停提示
                ToolTip {
                    parent: transferButton
                    text: "上传、下载"
                    visible: transferButton.hovered
                }

                onClicked: {
                    console.log("点击了传输按钮，可在此处理上传下载逻辑");
                    // 这里可扩展实际上传下载相关业务代码，比如弹出对应窗口等
                }
            }

            // 全部按钮
            Button {
                id: allButton
                height: 32
                width: 32
                padding: 4

                background: Rectangle {
                    radius: 16
                    color: "transparent"
                    border.color: themeManager.textSecondaryColor
                    border.width: 1
                }

                contentItem: Grid {
                    anchors.centerIn: parent
                    columns: 2
                    rows: 2
                    spacing: 1
                    
                    // 四个小方块表示全部/网格视图
                    Rectangle {
                        width: 3
                        height: 3
                        radius: 1
                        color: themeManager.textPrimaryColor
                    }
                    Rectangle {
                        width: 3
                        height: 3
                        radius: 1
                        color: themeManager.textPrimaryColor
                    }
                    Rectangle {
                        width: 3
                        height: 3
                        radius: 1
                        color: themeManager.textPrimaryColor
                    }
                    Rectangle {
                        width: 3
                        height: 3
                        radius: 1
                        color: themeManager.textPrimaryColor
                    }
                }

                // 鼠标悬停提示
                ToolTip {
                    parent: allButton
                    text: "全部文件"
                    visible: allButton.hovered
                }

                onClicked: {
                    console.log("点击了全部按钮，可处理对应逻辑");
                    // 可扩展点击后展示全部内容等业务逻辑
                }
            }
        }

        // 原右侧占位调整，因为上面新增了功能按钮区域，这里可去掉或者按需调整
        // Item {
        //     Layout.fillWidth: true
        // }
    }
}