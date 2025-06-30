import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: photoPage
    color: themeManager.backgroundColor
    
    // 添加调试信息
    Component.onCompleted: {
        console.log("PhotoPage 加载完成")
        if (typefilesVM) {
            console.log("typefilesVM 在 PhotoPage 中可用")
        } else {
            console.log("typefilesVM 在 PhotoPage 中不可用")
        }
        if (thumbnailVM) {
            console.log("thumbnailVM 在 PhotoPage 中可用")
        } else {
            console.log("thumbnailVM 在 PhotoPage 中不可用")
        }
    }

    // 连接缩略图信号
    Connections {
        target: thumbnailVM
        
        function onThumbnailReady(filePath, imageUrl) {
            console.log("图片缩略图准备完成:", filePath)
            // 更新对应的缩略图
            updateThumbnail(filePath, imageUrl)
        }
        
        function onThumbnailFailed(filePath, error) {
            console.log("图片缩略图获取失败:", filePath, error)
            // 可以设置默认缩略图
            setDefaultThumbnail(filePath)
        }
    }

    // 更新缩略图
    function updateThumbnail(filePath, imageUrl) {
        for (let i = 0; i < photoGrid.count; i++) {
            let item = photoGrid.itemAtIndex(i)
            if (item && item.filePath === filePath) {
                item.thumbnailSource = imageUrl
                break
            }
        }
    }

    // 设置默认缩略图
    function setDefaultThumbnail(filePath) {
        for (let i = 0; i < photoGrid.count; i++) {
            let item = photoGrid.itemAtIndex(i)
            if (item && item.filePath === filePath) {
                item.thumbnailSource = "qrc:/icons/image_default.png" // 默认图片图标
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
                    text: "图片文件"
                    font.pixelSize: 18
                    font.weight: Font.Medium
                    color: themeManager.textPrimaryColor
                }
                
                Item { Layout.fillWidth: true }
                
                // 刷新按钮
                Button {
                    text: "刷新"
                    onClicked: {
                        typefilesVM.fetchTypeFiles("photo", 1, 30)
                    }
                }
            }
        }

        // 图片网格
        ScrollView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            
            GridView {
                id: photoGrid
                anchors.fill: parent
                cellWidth: 200
                cellHeight: 200
                
                model: typefilesVM ? typefilesVM.files : []
                
                delegate: Rectangle {
                    width: 180
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
                        anchors.fill: parent
                        anchors.margins: 8
                        
                        source: parent.thumbnailSource
                        fillMode: Image.PreserveAspectCrop
                        asynchronous: true
                        cache: true
                        
                        // 默认图片图标
                        Rectangle {
                            anchors.fill: parent
                            color: themeManager.backgroundColor
                            visible: !parent.source || parent.status === Image.Error
                            
                            Text {
                                anchors.centerIn: parent
                                text: "🖼️"
                                font.pixelSize: 32
                                color: themeManager.textSecondaryColor
                            }
                        }
                    }
                    
                    // 文件名（悬停时显示）
                    Rectangle {
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        height: 30
                        color: "#80000000"
                        opacity: mouseArea.containsMouse ? 1 : 0
                        
                        Behavior on opacity {
                            NumberAnimation { duration: 200 }
                        }
                        
                        Text {
                            anchors.fill: parent
                            anchors.margins: 4
                            
                            text: modelData ? modelData.name : ""
                            font.pixelSize: 10
                            color: "white"
                            elide: Text.ElideRight
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                    }
                    
                    // 点击事件
                    MouseArea {
                        id: mouseArea
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        hoverEnabled: true
                        
                        onClicked: {
                            console.log("点击图片文件:", modelData.name)
                            // 这里可以添加查看大图的逻辑
                        }
                        
                        onDoubleClicked: {
                            console.log("双击查看图片:", modelData.relPath)
                            // 双击查看大图
                            if (modelData && modelData.relPath) {
                                // 调用系统图片查看器
                                // 这里可以调用 fileVM.open_file_with_system(modelData.relPath)
                            }
                        }
                    }
                    
                    // 组件加载完成后请求缩略图
                    Component.onCompleted: {
                        if (modelData && modelData.relPath && thumbnailVM) {
                            thumbnailVM.requestThumbnail(modelData.relPath, 180, 180)
                        }
                    }
                }
            }
        }
    }
} 