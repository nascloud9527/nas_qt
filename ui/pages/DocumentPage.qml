import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: documentPage
    color: themeManager.backgroundColor
    
    // 使用背景图片组件
    BackgroundImage {
        anchors.fill: parent
    }
        // 右键菜单组件
    Menu {
        id: videoContextMenu
        property int contextIndex: -1
        
        MenuItem {
            text: "打开"
            onTriggered: {
                if (videoContextMenu.contextIndex >= 0) {
                    var currentFile = fileVM.file_list[videoContextMenu.contextIndex]
                    if (currentFile && currentFile.relPath) {
                        var relPath = currentFile.relPath
                        var username = loginVM.get_username()
                        var newRelPath
                        // 拼接新的路径
                        if (username !== "admin") {
                            newRelPath = username + "/" + relPath
                        }else{
                            newRelPath = relPath
                        }
                        console.log("newRelPath:", newRelPath)
                        fileVM.open_file_with_system(newRelPath)
                    }
                }
            }
        }
        
        MenuItem {
            text: "复制"
            onTriggered: {
                if (videoContextMenu.contextIndex >= 0) {
                    var currentFile = fileVM.file_list[videoContextMenu.contextIndex]
                    if (currentFile && currentFile.relPath) {

                        var relPath = currentFile.relPath
                        var username = loginVM.get_username()
                        var newRelPath
                        // console.log("relPath:", relPath)
                        // console.log("get_username:", loginVM.get_username())
                        // 拼接新的路径
                        if (username !== "admin") {
                            newRelPath = username + "/" + relPath
                        }else{
                            newRelPath = relPath
                        }
                        // console.log("新的 relPath:", newRelPath)
                        // 创建新的文件对象，使用处理后的路径
                        var processedFile = {
                            "relPath": newRelPath,
                            "name": currentFile.name,
                            "isDir": currentFile.isDir
                        }

                        copyVM.set_selected_files([processedFile])
                        copyVM.copy_selected_files()
                    }
                }
            }
        }

        MenuItem {
            text: "移动"
            onTriggered: {
                if (videoContextMenu.contextIndex >= 0) {
                    var currentFile = fileVM.file_list[videoContextMenu.contextIndex]
                    if (currentFile && currentFile.relPath) {
                        // 获取当前文件的相对路径
                        var relPath = currentFile.relPath
                        var username = loginVM.get_username()
                        var newRelPath
 
                        // 拼接新的路径
                        if (username !== "admin") {
                            newRelPath = username + "/" + relPath
                        }else{
                            newRelPath = relPath
                        }

                        // 创建新的文件对象，使用处理后的路径
                        var processedFile = {
                            "relPath": newRelPath,
                            "name": currentFile.name,
                            "isDir": currentFile.isDir
                        }
                        copyVM.set_selected_files([processedFile])
                        copyVM.move_selected_files()
                    }
                }
            }
        }
        
        MenuItem {
            text: "删除"
            onTriggered: {
                if (videoContextMenu.contextIndex >= 0) {
                    var currentFile = fileVM.file_list[videoContextMenu.contextIndex]
                    if (currentFile && currentFile.relPath) {

                        console.log("currentFile.relPath:", currentFile.relPath)
                        // 获取当前文件的相对路径
                        var relPath = currentFile.relPath
                        var username = loginVM.get_username()
                        var storageRelPath = "storage/"
                        var newRelPath
                        // 拼接新的路径
                        if (username !== "admin") {
                            newRelPath = storageRelPath + username + "/" + relPath
                        }else{
                            newRelPath = storageRelPath + relPath
                        }
                        console.log("newRelPath:", newRelPath)
                                                // 创建新的文件对象，使用处理后的路径
                        var processedFile = {
                            "relPath": newRelPath,
                            "name": currentFile.name,
                            "isDir": currentFile.isDir
                        }
        
                        deleteVM.set_selected_files([processedFile])
                        deleteVM.delete_selected_files()
                    }
                }
            }
        }
    }
    // 返回信号
    signal goBack()
    
    // 添加调试信息
    Component.onCompleted: {
        console.log("DocumentPage 加载完成")
        if (typefilesVM) {
            console.log("typefilesVM 在 DocumentPage 中可用")
            // 自动获取文档文件数据
            typefilesVM.fetchTypeFiles("document", 1, 30)
        } else {
            console.log("typefilesVM 在 DocumentPage 中不可用")
        }
    }

    ColumnLayout {
        anchors.fill: parent
        spacing: 16

        // 文件列表标题栏
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            color: "transparent"

            RowLayout {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 16

                                // 返回按钮
                Button {
                    text: "返回"
                    onClicked: {
                        // 发送返回信号
                        documentPage.goBack()
                    }
                    background: Rectangle {
                        radius: 4
                        color: "#417cd4"  
                    }
                    contentItem: Text {
                        text: "返回"
                        color: "white"
                        font.pixelSize: 16
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                }
                Item { Layout.fillWidth: true }
                
                Text {
                    text: "文件列表"
                    font.pixelSize: 18
                    font.weight: Font.Medium
                    // color: themeManager.textPrimaryColor
                    color: "#FFFFFF"   
                }
                
                Item { Layout.fillWidth: true }    

            }
        }
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
                Layout.leftMargin: 12
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
                    font.pixelSize: 18
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
                color: "transparent"
                border.color: themeManager.dividerColor
                border.width: 1

                Text {
                    anchors.fill: parent
                    anchors.margins: 8
                    text: fileVM ? (fileVM.current_directory || "主页") : "加载中..."
                    font.pixelSize: 16
                    color: "#ffffff"  
                    verticalAlignment: Text.AlignVCenter
                    elide: Text.ElideLeft
                }
            }
        }
        // 表头行
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 40
            color: "transparent"

            RowLayout {
                anchors.fill: parent
                anchors.margins: 16
                spacing: 16
                // 全选复选框
                // CheckBox {
                //     id: selectAllCheckBox
                //     Layout.preferredWidth: 24
                //     Layout.preferredHeight: 24
                //     checked: fileVM.all_files_selected
                //     tristate: fileVM.some_files_selected && !fileVM.all_files_selected
                    
                //     onClicked: {
                //         // 明确处理点击事件，而不是依赖checkedChanged
                //         if (checkState === Qt.PartiallyChecked) {
                //             // 当处于三态时，强制设置为选中状态
                //             fileVM.select_all_files(true)
                //         } else {
                //             // 根据当前状态决定下一步操作
                //             if (fileVM.all_files_selected) {
                //                 // 当前全选，点击后取消全选
                //                 fileVM.select_all_files(false)
                //             } else {
                //                 // 当前未全选，点击后全选
                //                 fileVM.select_all_files(true)
                //             }
                //         }
                //     }
                // }
                // 文件图标占位符（对应文件列表项中的图标）
                Item {
                    Layout.preferredWidth: 24
                    Layout.preferredHeight: 24
                }

                Text {
                    text: "文件名"
                    font.pixelSize: 18
                    font.weight: Font.Medium
                    color: "#ffffff" 
                    Layout.preferredWidth: 200
                }

                Text {
                    text: "类型"
                    font.pixelSize: 18
                    font.weight: Font.Medium
                    color: "#ffffff" 
                    Layout.preferredWidth: 80
                }

                Text {
                    text: "大小"
                    font.pixelSize: 18
                    font.weight: Font.Medium
                    color: "#ffffff" 
                    Layout.preferredWidth: 80
                }

                Text {
                    text: "修改日期"
                    font.pixelSize: 18
                    font.weight: Font.Medium
                    color: "#ffffff" 
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
                    font.pixelSize: 18
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
           
            background: Rectangle {
                color: "transparent" // 使用主题的背景色
            }
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
                    color: "transparent"
                    border.color: modelData.selected ? themeManager.primaryColor : "transparent"
                    border.width: modelData.selected ? 2 : 0

                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 16
                        spacing: 16

                        // // 文件选择复选框
                        // CheckBox {
                        //     Layout.preferredWidth: 24
                        //     Layout.preferredHeight: 24
                        //     checked: modelData.selected
                            
                        //     onCheckedChanged: {
                        //         // 只有当复选框状态与文件选择状态不一致时才调用
                        //         if (checked !== modelData.selected) {
                        //             fileVM.toggle_file_selection(index, checked)
                        //         }
                        //     }
                        // }

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
                            font.pixelSize: 18
                            color: "#FFFFFF"
                            Layout.preferredWidth: 200
                            elide: Text.ElideRight
                        }

                        // 文件类型
                        Text {
                            text: modelData.type
                            font.pixelSize: 18
                            color: "#FFFFFF"
                            Layout.preferredWidth: 80
                        }

                        // 文件大小
                        Text {
                            text: modelData.size
                            font.pixelSize: 18
                            color: "#FFFFFF"
                            Layout.preferredWidth: 80
                        }

                        // 修改日期
                        Text {
                            text: modelData.updatedAt
                            font.pixelSize: 18
                            color: "#FFFFFF"
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
                                videoContextMenu.contextIndex = index
                                videoContextMenu.popup()
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