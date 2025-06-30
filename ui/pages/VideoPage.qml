import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: videoPage
    color: themeManager.backgroundColor
    
    // 添加调试信息
    Component.onCompleted: {
        console.log("VideoPage 加载完成")
        if (typefilesVM) {
            console.log("typefilesVM 在 VideoPage 中可用")
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
            console.log("视频缩略图准备完成:", filePath)
            // 更新对应的缩略图
            updateThumbnail(filePath, imageUrl)
        }
        
        function onThumbnailFailed(filePath, error) {
            console.log("视频缩略图获取失败:", filePath, error)
            // 可以设置默认缩略图
            setDefaultThumbnail(filePath)
        }
    }

    // 更新缩略图
    function updateThumbnail(filePath, imageUrl) {
        console.log("赋值缩略图", filePath, imageUrl)
        for (let i = 0; i < videoGrid.count; i++) {
            let item = videoGrid.itemAtIndex(i)
            if (item && item.filePath === filePath) {
                item.thumbnailSource = imageUrl
                break
            }
        }
    }

    // 设置默认缩略图
    function setDefaultThumbnail(filePath) {
        for (let i = 0; i < videoGrid.count; i++) {
            let item = videoGrid.itemAtIndex(i)
            if (item && item.filePath === filePath) {
                item.thumbnailSource = "qrc:/icons/video_default.png" // 默认视频图标
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
            color: themeManager.surfaceColor
            
            RowLayout {
                anchors.fill: parent
                anchors.margins: 16
                
                Text {
                    text: "视频文件"
                    font.pixelSize: 18
                    font.weight: Font.Medium
                    color: themeManager.textPrimaryColor
                }
                
                Item { Layout.fillWidth: true }
                
                // 刷新按钮
                Button {
                    text: "刷新"
                    onClicked: {
                        typefilesVM.fetchTypeFiles("video", 1, 30)
                    }
                }
            }
        }

        // 视频网格
        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            
            GridView {
                id: videoGrid
                anchors.fill: parent
                cellWidth: 220
                cellHeight: 200
                
                model: typefilesVM ? typefilesVM.files : []
                
                delegate: Rectangle {
                    width: 200
                    height: 180
                    radius: 8
                    color: themeManager.surfaceColor
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
                        //   source: "http://localhost:8080/api/thumbnail?fullpath=" + encodeURIComponent(modelData.relPath)
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
                        color: themeManager.textPrimaryColor
                        elide: Text.ElideRight
                        horizontalAlignment: Text.AlignHCenter
                    }
                    
                    // 点击事件
                    MouseArea {
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        
                        onClicked: {
                            console.log("点击视频文件:", modelData.name)
                            // 这里可以添加播放视频的逻辑
                        }
                        
                        onDoubleClicked: {
                            console.log("双击播放视频:", modelData.relPath)
                            // 双击播放视频
                            if (modelData && modelData.relPath) {
                                // 调用系统播放器播放视频
                                // 这里可以调用 fileVM.open_file_with_system(modelData.relPath)
                            }
                        }
                    }
                    
                    // 组件加载完成后请求缩略图
                    Component.onCompleted: {
                        if (modelData && modelData.relPath && thumbnailVM) {
                            thumbnailVM.requestThumbnail(modelData.relPath, 200, 150)
                        }
                    }
                }
            }
        }
    }
} 