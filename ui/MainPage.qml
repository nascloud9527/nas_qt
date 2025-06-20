import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    id: mainPage
    anchors.fill: parent

    // 添加调试信息
    Component.onCompleted: {
        console.log("MainPage 加载完成")
        if (fileVM) {
            console.log("fileVM 在 MainPage 中可用")
            console.log("当前目录:", fileVM.current_directory)
        } else {
            console.log("fileVM 在 MainPage 中不可用")
        }
        if (themeManager) {
            console.log("themeManager 在 MainPage 中可用")
        } else {
            console.log("themeManager 在 MainPage 中不可用")
        }
    }

    // 处理文件打开信号
    Connections {
        target: fileVM
        
        function onFileOpened(filePath) {
            console.log("文件打开:", filePath)
            // TODO: 实现文件打开逻辑，比如调用系统默认程序打开文件
            // 这里可以添加文件类型判断和相应的处理逻辑
        }
        
        function onDirectoryChanged(newDirectory) {
            console.log("目录改变:", newDirectory)
            // 目录改变时的处理逻辑
        }
        
        function onContextMenuRequested(x, y, index) {
            console.log("右键菜单请求:", x, y, index)
            // 右键菜单的处理逻辑
        }
        
        function onUploadFinished(success, message) {
            console.log("上传完成:", success, message)
            // 显示上传结果消息
            if (success) {
                showMessage("上传成功", message, "success")
            } else {
                showMessage("上传失败", message, "error")
            }
        }
    }

    // 消息提示组件
    function showMessage(title, message, type) {
        // 创建消息提示
        var messageComponent = Qt.createComponent("components/MessageDialog.qml")
        if (messageComponent.status === Component.Ready) {
            var messageDialog = messageComponent.createObject(mainPage, {
                "title": title,
                "message": message,
                "type": type
            })
            messageDialog.open()
        }
    }

    Rectangle {
        anchors.fill: parent
        color: themeManager.backgroundColor

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            // 1. 导航区域
            Loader {
                Layout.fillWidth: true
                Layout.preferredHeight: 60
                source: "components/NavigationBar.qml"
            }

            // 分隔线
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 1
                color: themeManager.dividerColor
            }

            // 2. 工具栏
            Loader {
                Layout.fillWidth: true
                Layout.preferredHeight: 90
                source: "components/ToolBar.qml"
            }

            // 分隔线
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 1
                color: themeManager.dividerColor
            }

            // 3. 文件列表区
            Loader {
                Layout.fillWidth: true
                Layout.fillHeight: true
                source: "components/FileListArea.qml"
            }
        }

        // 主题切换按钮（右上角）
        Button {
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.margins: 16
            width: 40
            height: 40
            
            background: Rectangle {
                radius: 20
                color: themeManager.surfaceColor
                border.color: themeManager.dividerColor
                border.width: 1
            }
            
            contentItem: Text {
                text: themeManager.isDarkTheme ? "☀️" : "🌙"
                font.pixelSize: 16
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            
            onClicked: {
                themeManager.toggleTheme()
            }
        }
    }
} 