import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: videoPage
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
                    var currentFile = typefilesVM.files[videoContextMenu.contextIndex]
                    if (currentFile && currentFile.relPath) {
                        var relPath = currentFile.relPath
                        if (relPath.startsWith("storage/")) {
                            relPath = relPath.slice(8)
                        }
                        fileVM.open_file_with_system(relPath)
                    }
                }
            }
        }
        
        MenuItem {
            text: "复制"
            onTriggered: {
                if (videoContextMenu.contextIndex >= 0) {
                    var currentFile = typefilesVM.files[videoContextMenu.contextIndex]
                    if (currentFile && currentFile.relPath) {
                        var relPath = currentFile.relPath
                        if (relPath.startsWith("storage/")) {
                            relPath = relPath.slice(8)
                        }
                        // 创建新的文件对象，使用处理后的路径
                        var processedFile = {
                            "relPath": relPath,
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
                    var currentFile = typefilesVM.files[videoContextMenu.contextIndex]
                    if (currentFile && currentFile.relPath) {
                        var relPath = currentFile.relPath
                        if (relPath.startsWith("storage/")) {
                            relPath = relPath.slice(8)
                        }
                        // 创建新的文件对象，使用处理后的路径
                        var processedFile = {
                            "relPath": relPath,
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
                    var currentFile = typefilesVM.files[videoContextMenu.contextIndex]
                    if (currentFile && currentFile.relPath) {
                        deleteVM.set_selected_files([currentFile])
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
        console.log("VideoPage 加载完成")
        if (typefilesVM) {
            console.log("typefilesVM 在 VideoPage 中可用")
            // 自动获取视频文件数据
            typefilesVM.fetchTypeFiles("video", 1, 30)
        } else {
            console.log("typefilesVM 在 VideoPage 中不可用")
        }
        if (thumbnailVM) {
            console.log("thumbnailVM 在 VideoPage 中可用")
        } else {
            console.log("thumbnailVM 在 VideoPage 中不可用")
        }
    }

    // 连接缩略图信号
    Connections {
        target: thumbnailVM
        
        function onThumbnailReady(filePath, imageUrl) {
            //   console.log("onThumbnailReady 收到缩略图:", filePath, "imageUrl=", imageUrl)
            // 更新对应的缩略图
                Qt.callLater(function() {
                updateThumbnail(filePath, imageUrl)
            })
        }
        
        function onThumbnailFailed(filePath, error) {
            
            // 可以设置默认缩略图
            // setDefaultThumbnail(filePath)
        }
    }

    // 更新缩略图
    function updateThumbnail(filePath, imageUrl) {
        // console.log("updateThumbnail 被调用，filePath =", filePath, "imageUrl =", imageUrl)
        // console.log("videoGrid.count =", videoGrid.count)

        for (let i = 0; i < videoGrid.count; i++) {
            let item = videoGrid.itemAtIndex(i)
            // console.log("检查 index =", i, "item =", item, item ? item.filePath : "null")

            if (item && item.filePath === filePath) {
                // console.log("updateThumbnail: 为 filePath =", filePath, "赋值 thumbnailSource =", imageUrl)
                item.thumbnailSource = imageUrl
                break
            }
        }
    }


    ColumnLayout {
        anchors.fill: parent
        spacing: 16

        // 标题栏
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 50
            color: "transparent"
            
            RowLayout {
                anchors.fill: parent
                anchors.margins: 16
                
                // 返回按钮
                Button {
                    text: "返回"
                    onClicked: {
                        // 发送返回信号
                        videoPage.goBack()
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
                    text: "视频列表"
                    font.pixelSize: 18
                    font.weight: Font.Medium
                    // color: themeManager.textPrimaryColor
                    color: "#FFFFFF"  
                }
                
                Item { Layout.fillWidth: true }
            }
        }

        // 视频网格
        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            
            GridView {
                id: videoGrid
                anchors.fill: parent
                anchors.leftMargin: 32
                anchors.rightMargin: 32     
                cellWidth: 220
                cellHeight: 200
                
                model: typefilesVM ? typefilesVM.files : []
                
                delegate: Rectangle {
                    width: 200
                    height: 180
                    radius: 8
                    color: "transparent"
                    border.color: themeManager.dividerColor
                    border.width: 1
                    
                    property string filePath: modelData ? modelData.relPath : ""
                    property string thumbnailSource: ""

                    
                    
                    // 缩略图
                    Image {
                        id: thumbnailImage
                        anchors.top: parent.top
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.bottom: fileNameText.top
                        anchors.margins: 8
                        anchors.bottomMargin: 4
                        
                        source: parent.thumbnailSource
                        fillMode: Image.PreserveAspectCrop
                        asynchronous: true
                        cache: true
                        
                        // 默认视频图标
                        Rectangle {
                            anchors.fill: parent
                            color: themeManager.backgroundColor
                            visible: !parent.source || parent.status === Image.Error
                            
                            Text {
                                anchors.centerIn: parent
                                text: "🎬"
                                font.pixelSize: 32
                                color: themeManager.textSecondaryColor
                            }
                        }
                    }
                    
                    // 文件名
                    Text {
                        id: fileNameText
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        anchors.margins: 8
                        
                        text: modelData ? modelData.name : ""
                        font.pixelSize: 12
                        color: "white"
                        elide: Text.ElideRight
                        horizontalAlignment: Text.AlignHCenter
                    }
                    
                    // 点击事件
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        acceptedButtons: Qt.LeftButton | Qt.RightButton
                        
                        onClicked: function(mouse) {
                            if (mouse.button === Qt.LeftButton) {
                                console.log("点击视频文件:", modelData.name)
                                // 这里可以添加播放视频的逻辑
                            } else if (mouse.button === Qt.RightButton) {
                                // 右键菜单
                                videoContextMenu.contextIndex = index
                                videoContextMenu.popup()
                                console.log("右键菜单触发，视频索引:", index)
                            }
                        }
                        
                        onDoubleClicked: function(mouse) {
                            if (mouse.button === Qt.LeftButton) {
                                console.log("双击播放视频:", modelData.relPath)
                                // 双击播放视频
                                if (modelData && modelData.relPath) {
                                    // 调用系统播放器播放视频
                                    var relPath = modelData.relPath
                                    if (relPath.startsWith("storage/")) {
                                        relPath = relPath.slice(8)
                                    }
                                    fileVM.open_file_with_system(relPath)
                                }
                            }
                        }
                    }
                    
                    // 组件加载完成后请求缩略图
                    Component.onCompleted: {
                        // console.log("delegate completed", filePath, "thumbnailSource=", thumbnailSource)
                        if (modelData && modelData.relPath && thumbnailVM) {
                            thumbnailVM.requestThumbnail(modelData.relPath, 200, 150)
                        }
                    }
                }
            }
        }
    }
} 