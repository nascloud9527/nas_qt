import QtQuick 6.5
import QtQuick.Controls 2.15

Menu {
    id: fileContextMenu
    property int contextIndex: -1
    
    MenuItem {
        text: "打开"
        onTriggered: {
            if (fileContextMenu.contextIndex >= 0) {
                fileVM.open_file_or_folder(fileContextMenu.contextIndex)
            }
        }
    }
    
    MenuItem {
        text: "复制"
        onTriggered: {
            if (fileContextMenu.contextIndex >= 0) {
                // 获取当前文件信息
                var currentFile = fileVM.file_list[fileContextMenu.contextIndex]
                if (currentFile && currentFile.relPath) {
                    // 设置选中的文件
                    copyVM.set_selected_files([currentFile])
                    // 执行复制操作（会自动选择目标目录）
                    copyVM.copy_selected_files()
                }
            }
        }
    }

    MenuItem {
        text: "移动"
        onTriggered: {
            if (fileContextMenu.contextIndex >= 0) {
                // 获取当前文件信息
                var currentFile = fileVM.file_list[fileContextMenu.contextIndex]
                if (currentFile && currentFile.relPath) {
                    // 设置选中的文件
                    copyVM.set_selected_files([currentFile])
                    // 执行移动操作（会自动选择目标目录）
                    copyVM.move_selected_files()
                }
            }
        }
    }
    
    MenuItem {
        text: "删除"
        onTriggered: {
            if (fileContextMenu.contextIndex >= 0) {
                // 获取当前文件信息
                var currentFile = fileVM.file_list[fileContextMenu.contextIndex]
                if (currentFile && currentFile.relPath) {
                    // 设置选中的文件
                    deleteVM.set_selected_files([currentFile])
                    // 执行删除操作（会显示确认对话框）
                    deleteVM.delete_selected_files()
                }
            }
        }
    }

    MenuItem {
        text: "投屏"
        onTriggered: {
            // TODO: 实现投屏功能
            console.log("投屏文件:", fileContextMenu.contextIndex)
        }
    }
    
} 