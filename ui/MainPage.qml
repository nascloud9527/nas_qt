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

    // 当前页面类型：0=文件列表, 1=视频, 2=图片, 3=文档, 4=音频
    property int currentPageType: 0

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
        
        function onCreateFolderFinished(success, message) {
            console.log("创建文件夹完成:", success, message)
            // 显示创建文件夹结果消息
            if (success) {
                showMessage("创建成功", message, "success")
                // 成功时关闭对话框
                if (createFolderDialogInstance) {
                    createFolderDialogInstance.close()
                    createFolderDialogInstance.destroy()
                    createFolderDialogInstance = null
                }
            } else {
                // 失败时显示错误信息，不关闭对话框
                if (createFolderDialogInstance) {
                    // 尝试解析JSON格式的错误信息
                    var errorMsg = message
                    try {
                        if (message.startsWith('{') && message.endsWith('}')) {
                            var errorObj = JSON.parse(message)
                            if (errorObj.error) {
                                errorMsg = errorObj.error
                            }
                        }
                    } catch (e) {
                        console.log("解析错误信息失败:", e)
                        // 如果解析失败，使用原始消息
                        errorMsg = message
                    }
                    createFolderDialogInstance.errorMessage = errorMsg
                } else {
                    showMessage("创建失败", message, "error")
                }
            }
        }
        
        function onShowCreateFolderDialogRequested() {
            console.log("显示创建文件夹对话框")
            showCreateFolderDialog()
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

    // 保存对话框实例的引用
    property var createFolderDialogInstance: null

    // 显示创建文件夹对话框
    function showCreateFolderDialog() {
        console.log("showCreateFolderDialog 被调用")
        
        // 直接创建对话框对象，而不是使用Loader
        var dialogComponent = Qt.createComponent("components/CreateFolderDialog.qml")
        if (dialogComponent.status === Component.Ready) {
            console.log("对话框组件创建成功")
            var dialog = dialogComponent.createObject(mainPage, {
                "folderName": "新建文件夹",
                "errorMessage": ""  // 初始化错误信息为空
            })
            
            // 保存对话框实例引用
            createFolderDialogInstance = dialog
            
            dialog.folderCreated.connect(function(folderName) {
                console.log("用户确认创建文件夹:", folderName)
                fileVM.create_folder(folderName)
                // 不在这里关闭对话框，让onCreateFolderFinished处理
            })
            
            dialog.dialogCancelled.connect(function() {
                console.log("用户取消创建文件夹")
                dialog.destroy()
                createFolderDialogInstance = null
            })
            
            console.log("尝试打开对话框")
            dialog.open()
        } else {
            console.log("对话框组件创建失败:", dialogComponent.errorString())
        }
    }

    // 切换页面类型
    function switchPageType(pageType) {
        console.log("切换到页面类型:", pageType)
        currentPageType = pageType
        
        // 根据页面类型加载不同的数据
        switch (pageType) {
            case 0: // 文件列表
                // 使用 fileVM 加载当前目录文件
                break
            case 1: // 视频
                typefilesVM.fetchTypeFiles("video", 1, 30)
                break
            case 2: // 图片
                typefilesVM.fetchTypeFiles("photo", 1, 30)
                break
            case 3: // 文档
                typefilesVM.fetchTypeFiles("document", 1, 30)
                break
            case 4: // 音频
                typefilesVM.fetchTypeFiles("audio", 1, 30)
                break
        }
    }

    // 使用背景图片组件
    BackgroundImage {
        anchors.fill: parent
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 0

        // 1. 导航区域
        Loader {
            Layout.fillWidth: true
            Layout.preferredHeight: 60
            source: "components/NavigationBar.qml"
            
            onItemChanged: {
                if (item) {
                    // 连接导航栏的页面切换信号
                    item.pageTypeChanged.connect(function(pageType) {
                        switchPageType(pageType)
                    })
                }
            }
        }

        // 分隔线
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 1
            color: themeManager.dividerColor
        }

        // 2. 工具栏（只在文件列表页面显示）
        Loader {
            Layout.fillWidth: true
            Layout.preferredHeight: 90
            source: "components/ToolBar.qml"
            visible: currentPageType === 0
        }

        // 分隔线（只在文件列表页面显示）
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 1
            color: themeManager.dividerColor
            visible: currentPageType === 0
        }

        // 3. 内容区域
        Loader {
            
            Layout.fillWidth: true
            Layout.fillHeight: true
            
            source: {
                switch (currentPageType) {
                    case 0: return "components/FileListArea.qml"
                    case 1: return "pages/VideoPage.qml"
                    case 2: return "pages/PhotoPage.qml"
                    case 3: return "pages/DocumentPage.qml"
                    case 4: return "pages/AudioPage.qml"
                    default: return "components/FileListArea.qml"
                }
            }
        }
    }
} 