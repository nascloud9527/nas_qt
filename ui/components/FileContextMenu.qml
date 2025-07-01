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
            // TODO: 实现复制功能
            console.log("复制文件:", fileContextMenu.contextIndex)
        }
    }

    MenuItem {
        text: "移动"
        onTriggered: {
            // TODO: 实现移动功能
            console.log("移动文件:", fileContextMenu.contextIndex)
        }
    }
    
    MenuItem {
        text: "删除"
        onTriggered: {
            // TODO: 实现删除功能
            console.log("删除文件:", fileContextMenu.contextIndex)
        }
    }

    MenuItem {
        text: "投屏"
        onTriggered: {
            // TODO: 实现投屏功能
            console.log("投屏文件:", fileContextMenu.contextIndex)
        }
    }
    
    // MenuSeparator {}
    
    // MenuItem {
    //     text: "重命名"
    //     onTriggered: {
    //         // TODO: 实现重命名功能
    //         console.log("重命名文件:", fileContextMenu.contextIndex)
    //     }
    // }
    
    // MenuItem {
    //     text: "属性"
    //     onTriggered: {
    //         // TODO: 实现属性查看功能
    //         console.log("查看文件属性:", fileContextMenu.contextIndex)
    //     }
    // }
} 