import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "components"

Item  {
    id: mainPage
    anchors.fill: parent

    // 背景
    // Background { }
    // 使用背景图片组件
    BackgroundImage {
        anchors.fill: parent
    }

    // 时间天气
    TimeWeatherCard { }

    // 右上角按钮
    TopRightButtons { }
    
    // 页面加载器
    Loader {
        id: pageLoader
        anchors.fill: parent
        // 默认不加载任何页面，显示主菜单
        
        // 将pageLoader传递给加载的页面
        property var pageLoaderRef: pageLoader
        
        // 监听加载的页面的返回信号
        onItemChanged: {
            if (item && item.goBack) {
                item.goBack.connect(function() {
                    pageLoader.source = ""
                    // 显示底部菜单
                    mainMenu.visible = true
                })
            }
        }
        
        // 监听source变化
        onSourceChanged: {
            if (source && source !== "") {
                // 有页面加载时，隐藏底部菜单
                mainMenu.visible = false
            } else {
                // 没有页面加载时，显示底部菜单
                mainMenu.visible = true
            }
        }
    }


    // 处理复制和移动操作信号
    Connections {
        target: copyVM
        
        function onCopyFinished(success, message) {
            console.log("复制操作完成:", success, message)
            // 显示复制结果消息
            if (success) {
                showMessage("复制成功", message, "success")
                // 刷新文件列表
                fileVM.refresh_file_list()
            } else {
                showMessage("复制失败", message, "error")
            }
        }
        
        function onCopyStarted(operationType) {
            console.log("复制操作开始:", operationType)
            // 可以在这里显示进度条或其他UI反馈
        }
        
        function onCopyProgressChanged(progress) {
            console.log("复制进度:", progress)
            // 可以在这里更新进度条
        }
        
        function onDirectoryTreeChanged(directoryTree) {
            // console.log("目录树数据更新:", directoryTree)
            // 显示目录选择对话框
            showDirectorySelectDialog(directoryTree)
        }
        
        function onDirectoryTreeRequested() {
            // console.log("请求目录树数据")
            // 可以在这里显示加载状态
        }
    }

    // 处理删除操作信号
    Connections {
        target: deleteVM
        
        function onDeleteFinished(success, message) {
            console.log("删除操作完成:", success, message)
            // 显示删除结果消息
            if (success) {
                showMessage("删除成功", message, "success")
                // 刷新文件列表
                fileVM.refresh_file_list()
            } else {
                showMessage("删除失败", message, "error")
            }
        }
        
        function onDeleteStarted(operationInfo) {
            console.log("删除操作开始:", operationInfo)
            // 可以在这里显示进度条或其他UI反馈
        }
        
        function onDeleteProgressChanged(progress) {
            console.log("删除进度:", progress)
            // 可以在这里更新进度条
        }
        
        function onConfirmationRequested(filesToDelete) {
            console.log("请求删除确认:", filesToDelete)
            showDeleteConfirmDialog(filesToDelete)
        }
    }

    property var deleteConfirmDialogInstance: null
    property var directorySelectDialogInstance: null
    property string currentOperation: "" // "copy" 或 "move"

    // 显示删除确认对话框
    function showDeleteConfirmDialog(filesToDelete) {
        console.log("showDeleteConfirmDialog 被调用")
        
        // 创建删除确认对话框
        var dialogComponent = Qt.createComponent("components/DeleteConfirmDialog.qml")
        if (dialogComponent.status === Component.Ready) {
            console.log("删除确认对话框组件创建成功")
            var dialog = dialogComponent.createObject(mainPage, {
                "filesToDelete": filesToDelete,
                "title": "确认删除",
                "message": "确定要删除选中的文件吗？此操作不可撤销。"
            })
            
            // 保存对话框实例引用
            deleteConfirmDialogInstance = dialog
            
            dialog.deleteConfirmed.connect(function() {
                console.log("用户确认删除")
                deleteVM.confirm_delete()
                dialog.destroy()
                deleteConfirmDialogInstance = null
            })
            
            dialog.deleteCancelled.connect(function() {
                console.log("用户取消删除")
                deleteVM.cancel_delete()
                dialog.destroy()
                deleteConfirmDialogInstance = null
            })
            
            console.log("尝试打开删除确认对话框")
            dialog.open()
        } else {
            console.log("删除确认对话框组件创建失败:", dialogComponent.errorString())
        }
    }
    
    // 显示目录选择对话框
    function showDirectorySelectDialog(directoryTree) {
        console.log("showDirectorySelectDialog 被调用")
        
        // 获取当前操作类型
        currentOperation = copyVM.get_current_operation_type()
        console.log("当前操作类型:", currentOperation)
        
        // 创建目录选择对话框
        var dialogComponent = Qt.createComponent("components/DirectorySelectDialog.qml")
        if (dialogComponent.status === Component.Ready) {
            console.log("目录选择对话框组件创建成功")
            var dialog = dialogComponent.createObject(mainPage, {
                "directoryTree": directoryTree,
                "dialogTitle": "选择目标目录"
            })
            
            // 保存对话框实例引用
            directorySelectDialogInstance = dialog
            
            dialog.directorySelected.connect(function(selectedDirectory) {
                console.log("用户选择目录:", selectedDirectory)
                // 根据当前操作类型执行相应的操作
                if (currentOperation === "copy") {
                    copyVM.copy_files_with_directory(selectedDirectory)
                } else if (currentOperation === "move") {
                    copyVM.move_files_with_directory(selectedDirectory)
                }
                dialog.destroy()
                directorySelectDialogInstance = null
                currentOperation = ""
            })
            
            dialog.dialogCancelled.connect(function() {
                console.log("用户取消选择目录")
                dialog.destroy()
                directorySelectDialogInstance = null
                currentOperation = ""
            })
            
            console.log("尝试打开目录选择对话框")
            dialog.open()
        } else {
            console.log("目录选择对话框组件创建失败:", dialogComponent.errorString())
        }
    }
    
    // 底部菜单
    MainMenu_tv { 
        id: mainMenu
        onPageSelected: function(pagePath) {
            console.log("切换到页面:", pagePath)
            pageLoader.source = pagePath
        }
    }
}
