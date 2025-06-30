import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: documentPage
    color: themeManager.backgroundColor
    
    // 添加调试信息
    Component.onCompleted: {
        console.log("DocumentPage 加载完成")
        if (typefilesVM) {
            console.log("typefilesVM 在 DocumentPage 中可用")
        } else {
            console.log("typefilesVM 在 DocumentPage 中不可用")
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
                    text: "文档文件"
                    font.pixelSize: 18
                    font.weight: Font.Medium
                    color: themeManager.textPrimaryColor
                }
                
                Item { Layout.fillWidth: true }
                
                // 刷新按钮
                Button {
                    text: "刷新"
                    onClicked: {
                        typefilesVM.fetchTypeFiles("document", 1, 30)
                    }
                }
            }
        }

        // 文档列表
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: themeManager.surfaceColor
            radius: 8
            
            // 表头
            Rectangle {
                id: headerRow
                anchors.top: parent.top
                anchors.left: parent.left
                anchors.right: parent.right
                height: 40
                color: themeManager.backgroundColor
                radius: 8
                
                RowLayout {
                    anchors.fill: parent
                    anchors.margins: 16
                    spacing: 16
                    
                    // 文件名
                    Text {
                        text: "文件名"
                        font.pixelSize: 14
                        font.weight: Font.Medium
                        color: themeManager.textPrimaryColor
                        Layout.preferredWidth: 300
                    }
                    
                    // 文件大小
                    Text {
                        text: "大小"
                        font.pixelSize: 14
                        font.weight: Font.Medium
                        color: themeManager.textPrimaryColor
                        Layout.preferredWidth: 100
                    }
                    
                    // 修改时间
                    Text {
                        text: "修改时间"
                        font.pixelSize: 14
                        font.weight: Font.Medium
                        color: themeManager.textPrimaryColor
                        Layout.preferredWidth: 150
                    }
                    
                    // 操作
                    Text {
                        text: "操作"
                        font.pixelSize: 14
                        font.weight: Font.Medium
                        color: themeManager.textPrimaryColor
                        Layout.fillWidth: true
                    }
                }
            }
            
            // 文件列表
            ListView {
                id: documentList
                anchors.top: headerRow.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.margins: 8
                
                model: typefilesVM ? typefilesVM.files : []
                
                delegate: Rectangle {
                    width: documentList.width
                    height: 50
                    color: mouseArea.containsMouse ? themeManager.hoverColor : "transparent"
                    radius: 4
                    
                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 16
                        spacing: 16
                        
                        // 文件图标
                        Rectangle {
                            width: 32
                            height: 32
                            radius: 4
                            color: themeManager.primaryColor + "20"
                            
                            Text {
                                anchors.centerIn: parent
                                text: getDocumentIcon(modelData ? modelData.name : "")
                                font.pixelSize: 16
                                color: themeManager.primaryColor
                            }
                        }
                        
                        // 文件名
                        Text {
                            text: modelData ? modelData.name : ""
                            font.pixelSize: 14
                            color: themeManager.textPrimaryColor
                            elide: Text.ElideRight
                            Layout.preferredWidth: 250
                        }
                        
                        // 文件大小
                        Text {
                            text: formatFileSize(modelData ? modelData.size : 0)
                            font.pixelSize: 12
                            color: themeManager.textSecondaryColor
                            Layout.preferredWidth: 80
                        }
                        
                        // 修改时间
                        Text {
                            text: formatDate(modelData ? modelData.updatedAt : "")
                            font.pixelSize: 12
                            color: themeManager.textSecondaryColor
                            Layout.preferredWidth: 130
                        }
                        
                        // 操作按钮
                        Row {
                            spacing: 8
                            Layout.fillWidth: true
                            
                            Button {
                                text: "打开"
                                height: 28
                                padding: 8
                                
                                background: Rectangle {
                                    radius: 4
                                    color: parent.pressed ? themeManager.primaryColor + "80" : themeManager.primaryColor
                                }
                                
                                contentItem: Text {
                                    text: parent.text
                                    font.pixelSize: 12
                                    color: "white"
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter
                                }
                                
                                onClicked: {
                                    console.log("打开文档:", modelData.relPath)
                                    if (modelData && modelData.relPath) {
                                        // 调用系统默认程序打开文档
                                        // fileVM.open_file_with_system(modelData.relPath)
                                    }
                                }
                            }
                            
                            Button {
                                text: "下载"
                                height: 28
                                padding: 8
                                
                                background: Rectangle {
                                    radius: 4
                                    color: parent.pressed ? themeManager.surfaceColor : "transparent"
                                    border.color: themeManager.dividerColor
                                    border.width: 1
                                }
                                
                                contentItem: Text {
                                    text: parent.text
                                    font.pixelSize: 12
                                    color: themeManager.textPrimaryColor
                                    horizontalAlignment: Text.AlignHCenter
                                    verticalAlignment: Text.AlignVCenter
                                }
                                
                                onClicked: {
                                    console.log("下载文档:", modelData.relPath)
                                    if (modelData && modelData.relPath) {
                                        // 调用下载功能
                                        // downloadVM.download_file(modelData.relPath)
                                    }
                                }
                            }
                        }
                    }
                    
                    // 点击事件
                    MouseArea {
                        id: mouseArea
                        anchors.fill: parent
                        cursorShape: Qt.PointingHandCursor
                        hoverEnabled: true
                        
                        onClicked: {
                            console.log("点击文档:", modelData.name)
                        }
                        
                        onDoubleClicked: {
                            console.log("双击打开文档:", modelData.relPath)
                            if (modelData && modelData.relPath) {
                                // 调用系统默认程序打开文档
                                // fileVM.open_file_with_system(modelData.relPath)
                            }
                        }
                    }
                }
            }
        }
    }
    
    // 获取文档图标
    function getDocumentIcon(fileName) {
        if (!fileName) return "📄"
        
        let ext = fileName.split('.').pop().toLowerCase()
        switch (ext) {
            case 'pdf': return "📕"
            case 'doc':
            case 'docx': return "📘"
            case 'xls':
            case 'xlsx': return "📗"
            case 'ppt':
            case 'pptx': return "📙"
            case 'txt': return "📄"
            case 'rtf': return "📄"
            default: return "📄"
        }
    }
    
    // 格式化文件大小
    function formatFileSize(bytes) {
        if (bytes === 0) return "0 B"
        
        const k = 1024
        const sizes = ['B', 'KB', 'MB', 'GB', 'TB']
        const i = Math.floor(Math.log(bytes) / Math.log(k))
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    }
    
    // 格式化日期
    function formatDate(dateString) {
        if (!dateString) return ""
        
        let date = new Date(dateString)
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
    }
} 