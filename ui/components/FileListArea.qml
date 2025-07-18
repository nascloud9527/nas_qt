import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: fileListArea
    color: themeManager.backgroundColor

    // 引用右键菜单组件
    FileContextMenu {
        id: contextMenu
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
                    checked: fileVM.all_files_selected
                    tristate: fileVM.some_files_selected && !fileVM.all_files_selected
                    
                    onClicked: {
                        // 明确处理点击事件，而不是依赖checkedChanged
                        if (checkState === Qt.PartiallyChecked) {
                            // 当处于三态时，强制设置为选中状态
                            fileVM.select_all_files(true)
                        } else {
                            // 根据当前状态决定下一步操作
                            if (fileVM.all_files_selected) {
                                // 当前全选，点击后取消全选
                                fileVM.select_all_files(false)
                            } else {
                                // 当前未全选，点击后全选
                                fileVM.select_all_files(true)
                            }
                        }
                    }
                }

                // 文件图标占位符（对应文件列表项中的图标）
                Item {
                    Layout.preferredWidth: 24
                    Layout.preferredHeight: 24
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

            // 空数据提示
            Rectangle {
                anchors.fill: parent
                color: themeManager.backgroundColor
                visible: fileVM.file_list.length === 0

                ColumnLayout {
                    anchors.centerIn: parent
                    spacing: 16

                    // 空数据图标
                    Rectangle {
                        Layout.preferredWidth: 64
                        Layout.preferredHeight: 64
                        radius: 32
                        color: themeManager.surfaceColor
                        border.color: themeManager.dividerColor
                        border.width: 2

                        Text {
                            anchors.centerIn: parent
                            text: "📁"
                            font.pixelSize: 28
                        }
                    }

                    // 空数据文本
                    // Text {
                    //     text: "No data"
                    //     font.pixelSize: 16
                    //     font.weight: Font.Medium
                    //     color: themeManager.textSecondaryColor
                    //     horizontalAlignment: Text.AlignHCenter
                    // }

                    // 提示文本
                    Text {
                        text: "此文件夹为空"
                        font.pixelSize: 12
                        color: themeManager.textSecondaryColor
                        horizontalAlignment: Text.AlignHCenter
                    }
                }
            }

            ListView {
                id: fileListView
                anchors.fill: parent
                model: fileVM.file_list
                spacing: 1
                visible: fileVM.file_list.length > 0

                delegate: Rectangle {
                    width: fileListView.width
                    height: 50
                    color: mouseArea.containsMouse ? themeManager.hoverColor : 
                           (modelData.selected ? themeManager.primaryColor + "20" : themeManager.surfaceColor)
                    border.color: modelData.selected ? themeManager.primaryColor : "transparent"
                    border.width: modelData.selected ? 2 : 0

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
                                // 只有当复选框状态与文件选择状态不一致时才调用
                                if (checked !== modelData.selected) {
                                    fileVM.toggle_file_selection(index, checked)
                                }
                            }
                        }

                        // 文件图标
                        Text {
                            text: getFileTypeIcon(modelData.type)
                            font.pixelSize: 18
                            color: themeManager.textSecondaryColor
                            Layout.preferredWidth: 24
                            Layout.preferredHeight: 24
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
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
                        acceptedButtons: Qt.LeftButton | Qt.RightButton
                        
                        // 单击选中文件
                        onClicked: function(mouse) {
                            if (mouse.button === Qt.LeftButton) {
                                var ctrlPressed = (mouse.modifiers & Qt.ControlModifier) !== 0
                                fileVM.select_file(index, ctrlPressed)
                            } else if (mouse.button === Qt.RightButton) {
                                contextMenu.contextIndex = index
                                contextMenu.popup()
                                console.log("右键菜单触发，文件索引:", index)
                            }
                        }
                        
                        // 双击打开文件或文件夹
                        onDoubleClicked: function(mouse) {
                            if (mouse.button === Qt.LeftButton) {
                                fileVM.open_file_or_folder(index)
                            }
                        }
                    }
                }
            }
        }
    }

    // 根据文件类型返回图标文本
    function getFileTypeIcon(type) {
        switch(type) {
            case "文件夹": return "📁"
            case "文档": return "📄"
            case "图片": return "🖼️"
            case "视频": return "📹"
            case "音频": return "🎵"
            case "压缩包": return "📦"
            default: return "📌"
        }
    }
} 