import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: fileListArea
    color: themeManager.backgroundColor

    // 右键菜单
    Menu {
        id: contextMenu
        property int contextIndex: -1
        
        MenuItem {
            text: "打开"
            onTriggered: {
                if (contextMenu.contextIndex >= 0) {
                    fileVM.open_file_or_folder(contextMenu.contextIndex)
                }
            }
        }
        
        MenuItem {
            text: "复制"
            onTriggered: {
                // TODO: 实现复制功能
                console.log("复制文件:", contextMenu.contextIndex)
            }
        }
        
        MenuItem {
            text: "删除"
            onTriggered: {
                // TODO: 实现删除功能
                console.log("删除文件:", contextMenu.contextIndex)
            }
        }
        
        MenuSeparator {}
        
        MenuItem {
            text: "重命名"
            onTriggered: {
                // TODO: 实现重命名功能
                console.log("重命名文件:", contextMenu.contextIndex)
            }
        }
        
        MenuItem {
            text: "属性"
            onTriggered: {
                // TODO: 实现属性查看功能
                console.log("查看文件属性:", contextMenu.contextIndex)
            }
        }
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        // 文件列表标题栏
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 40
            color: themeManager.surfaceColor

            RowLayout {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 16

                // 全选复选框
                CheckBox {
                    id: selectAllCheckBox
                    Layout.preferredWidth: 24
                    Layout.preferredHeight: 24
                    
                    onCheckedChanged: {
                        // 全选/取消全选
                        fileVM.select_all_files(checked)
                    }
                }

                Text {
                    text: "文件名"
                    font.pixelSize: 12
                    font.weight: Font.Medium
                    color: themeManager.textSecondaryColor
                    Layout.preferredWidth: 200
                }

                Text {
                    text: "类型"
                    font.pixelSize: 12
                    font.weight: Font.Medium
                    color: themeManager.textSecondaryColor
                    Layout.preferredWidth: 80
                }

                Text {
                    text: "大小"
                    font.pixelSize: 12
                    font.weight: Font.Medium
                    color: themeManager.textSecondaryColor
                    Layout.preferredWidth: 80
                }

                Text {
                    text: "修改日期"
                    font.pixelSize: 12
                    font.weight: Font.Medium
                    color: themeManager.textSecondaryColor
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
            color: themeManager.dividerColor
        }

        // 加载状态或错误信息
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 40
            color: themeManager.surfaceColor
            visible: fileVM.is_loading || fileVM.error_message !== ""

            RowLayout {
                anchors.fill: parent
                anchors.margins: 16

                BusyIndicator {
                    Layout.preferredWidth: 20
                    Layout.preferredHeight: 20
                    visible: fileVM.is_loading
                }

                Text {
                    text: fileVM.is_loading ? "正在加载文件列表..." : fileVM.error_message
                    font.pixelSize: 12
                    color: fileVM.is_loading ? themeManager.textSecondaryColor : themeManager.errorColor
                    Layout.fillWidth: true
                }
            }
        }

        // 文件列表
        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            visible: !fileVM.is_loading && fileVM.error_message === ""

            ListView {
                id: fileListView
                anchors.fill: parent
                model: fileVM.file_list
                spacing: 1

                delegate: Rectangle {
                    width: fileListView.width
                    height: 50
                    color: mouseArea.containsMouse ? themeManager.hoverColor : themeManager.surfaceColor

                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 16
                        spacing: 16

                        // 文件选择复选框
                        CheckBox {
                            Layout.preferredWidth: 24
                            Layout.preferredHeight: 24
                            checked: modelData.selected
                            
                            onCheckedChanged: {
                                fileVM.toggle_file_selection(index, checked)
                            }
                        }

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
                            color: themeManager.textPrimaryColor
                            Layout.preferredWidth: 200
                            elide: Text.ElideRight
                        }

                        // 文件类型
                        Text {
                            text: modelData.type
                            font.pixelSize: 12
                            color: themeManager.textSecondaryColor
                            Layout.preferredWidth: 80
                        }

                        // 文件大小
                        Text {
                            text: modelData.size
                            font.pixelSize: 12
                            color: themeManager.textSecondaryColor
                            Layout.preferredWidth: 80
                        }

                        // 修改日期
                        Text {
                            text: modelData.updatedAt
                            font.pixelSize: 12
                            color: themeManager.textSecondaryColor
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
                        
                        // 单击选中文件
                        onClicked: {
                            if (mouse.button === Qt.LeftButton) {
                                fileVM.select_file(index)
                            }
                        }
                        
                        // 双击打开文件或文件夹
                        onDoubleClicked: {
                            if (mouse.button === Qt.LeftButton) {
                                fileVM.open_file_or_folder(index)
                            }
                        }
                        
                        // 右键菜单
                        onPressAndHold: {
                            if (mouse.button === Qt.RightButton) {
                                contextMenu.contextIndex = index
                                contextMenu.popup()
                            }
                        }
                        
                        // 右键点击（兼容桌面平台）
                        onReleased: {
                            if (mouse.button === Qt.RightButton) {
                                contextMenu.contextIndex = index
                                contextMenu.popup()
                            }
                        }
                    }
                }
            }
        }
    }

    // 根据文件类型返回颜色
    function getFileTypeColor(type) {
        switch(type) {
            case "文件夹": return themeManager.primaryColor
            case "文档": return themeManager.primaryColor
            case "图片": return themeManager.successColor
            case "视频": return themeManager.warningColor
            case "音频": return themeManager.accentColor
            case "压缩包": return "#FF9800"
            default: return themeManager.textSecondaryColor
        }
    }
} 