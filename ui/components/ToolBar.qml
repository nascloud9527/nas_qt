import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: toolBar
    color: themeManager.surfaceColor

    // 添加调试信息
    Component.onCompleted: {
        console.log("ToolBar 加载完成")
        if (fileVM) {
            console.log("fileVM 在 ToolBar 中可用")
            console.log("当前目录:", fileVM.current_directory)
        } else {
            console.log("fileVM 在 ToolBar 中不可用")
        }
        if (themeManager) {
            console.log("themeManager 在 ToolBar 中可用")
        } else {
            console.log("themeManager 在 ToolBar 中不可用")
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 12
        spacing: 8

        // 路径显示栏
        RowLayout {
            Layout.fillWidth: true
            Layout.preferredHeight: 32
            spacing: 8

            // 返回上一级按钮
            Button {
                id: backButton
                Layout.preferredWidth: 32
                Layout.preferredHeight: 32
                enabled: fileVM && !fileVM.is_at_home
                
                background: Rectangle {
                    radius: 16
                    color: parent.enabled ? 
                           (parent.pressed ? themeManager.hoverColor : themeManager.backgroundColor) :
                           themeManager.disabledColor
                    border.color: parent.enabled ? themeManager.dividerColor : themeManager.disabledColor
                    border.width: 1
                }
                
                contentItem: Text {
                    text: "←"
                    font.pixelSize: 16
                    font.weight: Font.Bold
                    color: parent.enabled ? themeManager.textPrimaryColor : themeManager.textDisabledColor
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                
                onClicked: {
                    console.log("返回按钮被点击")
                    if (fileVM && fileVM.current_directory !== "") {
                        console.log("执行返回上一级，当前目录:", fileVM.current_directory)
                        fileVM.go_to_parent_directory()
                    } else {
                        console.log("无法返回，当前目录:", fileVM ? fileVM.current_directory : "fileVM不可用")
                    }
                }
            }

            // 当前路径显示
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 32
                radius: 16
                color: themeManager.backgroundColor
                border.color: themeManager.dividerColor
                border.width: 1

                Text {
                    anchors.fill: parent
                    anchors.margins: 8
                    text: fileVM ? (fileVM.current_directory || "主页") : "加载中..."
                    font.pixelSize: 12
                    color: themeManager.textPrimaryColor
                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideLeft
                }
            }
        }

        // 按钮栏
        RowLayout {
            Layout.fillWidth: true
            Layout.preferredHeight: 36
            spacing: 12

            // 上传文件按钮
            Button {
                id: uploadButton
                text: fileVM && fileVM.is_uploading ? "上传中..." : "上传文件"
                Layout.preferredWidth: 100
                Layout.preferredHeight: 36
                enabled: fileVM && !fileVM.is_uploading
                
                background: Rectangle {
                    radius: 18
                    color: parent.enabled ? 
                           (parent.pressed ? themeManager.primaryDarkColor : themeManager.primaryColor) :
                           themeManager.disabledColor
                    border.color: parent.enabled ? "#40000000" : themeManager.disabledColor
                    border.width: 1
                }
                
                contentItem: Text {
                    text: parent.text
                    font.pixelSize: 12
                    font.weight: Font.Medium
                    color: parent.enabled ? "white" : themeManager.textDisabledColor
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                
                onClicked: {
                    console.log("点击上传文件")
                    if (fileVM) {
                        fileVM.select_file_for_upload()
                    } else {
                        console.log("fileVM不可用")
                    }
                }
            }

            // 下载文件按钮
            Button {
                id: downloadButton
                text: downloadVM && downloadVM.is_downloading ? "下载中..." : "下载文件"
                Layout.preferredWidth: 100
                Layout.preferredHeight: 36
                enabled: fileVM && downloadVM && !downloadVM.is_downloading
                
                background: Rectangle {
                    radius: 18
                    color: parent.enabled ? 
                           (parent.pressed ? themeManager.primaryDarkColor : themeManager.primaryColor) :
                           themeManager.disabledColor
                    border.color: parent.enabled ? "#40000000" : themeManager.disabledColor
                    border.width: 1
                }
                
                contentItem: Text {
                    text: parent.text
                    font.pixelSize: 12
                    font.weight: Font.Medium
                    color: parent.enabled ? "white" : themeManager.textDisabledColor
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                
                onClicked: {
                    console.log("点击下载文件")
                    if (fileVM && downloadVM) {
                        // 获取当前选中的文件列表进行下载
                        var selectedFiles = fileVM.get_selected_files()    
                        console.log("获取到的文件列表:", JSON.stringify(selectedFiles))  // 新增日志输出                  
                        if (selectedFiles && selectedFiles.length > 0) {
                            downloadVM.download_multiple_files(selectedFiles)
                        } else {
                            console.log("没有选中文件")
                        }
                    } else {
                        console.log("fileVM或downloadVM不可用")
                    }
                }
            }

            // 新建文件夹按钮
            Button {
                id: createFolderButton
                text: fileVM && fileVM.is_creating_folder ? "创建中..." : "新建文件夹"
                Layout.preferredWidth: 100
                Layout.preferredHeight: 36
                enabled: fileVM && !fileVM.is_creating_folder
                
                background: Rectangle {
                    radius: 18
                    color: parent.enabled ? 
                           (parent.pressed ? themeManager.hoverColor : themeManager.backgroundColor) :
                           themeManager.disabledColor
                    border.color: parent.enabled ? themeManager.dividerColor : themeManager.disabledColor
                    border.width: 1
                }
                
                contentItem: Text {
                    text: parent.text
                    font.pixelSize: 12
                    font.weight: Font.Medium
                    color: parent.enabled ? themeManager.textPrimaryColor : themeManager.textDisabledColor
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                
                onClicked: {
                    console.log("点击新建文件夹")
                    if (fileVM) {
                        fileVM.show_create_folder_dialog()
                    } else {
                        console.log("fileVM不可用")
                    }
                }
            }

            // 右侧占位
            Item {
                Layout.fillWidth: true
            }
        }
    }
} 