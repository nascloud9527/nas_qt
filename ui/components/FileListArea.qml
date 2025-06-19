import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: fileListArea
    color: backgroundColor

    property color backgroundColor: "#FAFAFA"
    property color surfaceColor: "#FFFFFF"
    property color textPrimaryColor: "#212121"
    property color textSecondaryColor: "#757575"
    property color dividerColor: "#BDBDBD"

    // 演示文件数据
    property var fileList: [
        { name: "工作文档.docx", type: "文档", size: "2.5 MB", date: "2024-01-15" },
        { name: "项目计划.pdf", type: "文档", size: "1.8 MB", date: "2024-01-14" },
        { name: "会议照片.jpg", type: "图片", size: "3.2 MB", date: "2024-01-13" },
        { name: "演示视频.mp4", type: "视频", size: "15.6 MB", date: "2024-01-12" },
        { name: "数据表格.xlsx", type: "文档", size: "856 KB", date: "2024-01-11" },
        { name: "风景图片.png", type: "图片", size: "4.1 MB", date: "2024-01-10" },
        { name: "音乐文件.mp3", type: "音频", size: "8.3 MB", date: "2024-01-09" },
        { name: "备份文件.zip", type: "压缩包", size: "25.7 MB", date: "2024-01-08" }
    ]

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        // 文件列表标题栏
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 40
            color: surfaceColor

            RowLayout {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 16

                Text {
                    text: "文件名"
                    font.pixelSize: 12
                    font.weight: Font.Medium
                    color: textSecondaryColor
                    Layout.preferredWidth: 200
                }

                Text {
                    text: "类型"
                    font.pixelSize: 12
                    font.weight: Font.Medium
                    color: textSecondaryColor
                    Layout.preferredWidth: 80
                }

                Text {
                    text: "大小"
                    font.pixelSize: 12
                    font.weight: Font.Medium
                    color: textSecondaryColor
                    Layout.preferredWidth: 80
                }

                Text {
                    text: "修改日期"
                    font.pixelSize: 12
                    font.weight: Font.Medium
                    color: textSecondaryColor
                    Layout.preferredWidth: 100
                }

                Item {
                    Layout.fillWidth: true
                }
            }
        }

        // 分隔线
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 1
            color: dividerColor
        }

        // 文件列表
        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true

            ListView {
                id: fileListView
                anchors.fill: parent
                model: fileList
                spacing: 1

                delegate: Rectangle {
                    width: fileListView.width
                    height: 50
                    color: mouseArea.containsMouse ? "#F0F0F0" : surfaceColor

                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 16
                        spacing: 16

                        // 文件图标（简化版）
                        Rectangle {
                            Layout.preferredWidth: 24
                            Layout.preferredHeight: 24
                            radius: 4
                            color: getFileTypeColor(modelData.type)
                        }

                        // 文件名
                        Text {
                            text: modelData.name
                            font.pixelSize: 14
                            color: textPrimaryColor
                            Layout.preferredWidth: 200
                            elide: Text.ElideRight
                        }

                        // 文件类型
                        Text {
                            text: modelData.type
                            font.pixelSize: 12
                            color: textSecondaryColor
                            Layout.preferredWidth: 80
                        }

                        // 文件大小
                        Text {
                            text: modelData.size
                            font.pixelSize: 12
                            color: textSecondaryColor
                            Layout.preferredWidth: 80
                        }

                        // 修改日期
                        Text {
                            text: modelData.date
                            font.pixelSize: 12
                            color: textSecondaryColor
                            Layout.preferredWidth: 100
                        }

                        Item {
                            Layout.fillWidth: true
                        }
                    }

                    MouseArea {
                        id: mouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: {
                            console.log("点击文件:", modelData.name)
                        }
                    }
                }
            }
        }
    }

    // 根据文件类型返回颜色
    function getFileTypeColor(type) {
        switch(type) {
            case "文档": return "#2196F3"
            case "图片": return "#4CAF50"
            case "视频": return "#FF5722"
            case "音频": return "#9C27B0"
            case "压缩包": return "#FF9800"
            default: return "#757575"
        }
    }
} 