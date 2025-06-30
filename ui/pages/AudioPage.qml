import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: audioPage
    color: themeManager.backgroundColor
    
    // 添加调试信息
    Component.onCompleted: {
        console.log("AudioPage 加载完成")
        if (typefilesVM) {
            console.log("typefilesVM 在 AudioPage 中可用")
        } else {
            console.log("typefilesVM 在 AudioPage 中不可用")
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
                    text: "音频文件"
                    font.pixelSize: 18
                    font.weight: Font.Medium
                    color: themeManager.textPrimaryColor
                }
                
                Item { Layout.fillWidth: true }
                
                // 刷新按钮
                Button {
                    text: "刷新"
                    onClicked: {
                        typefilesVM.fetchTypeFiles("audio", 1, 30)
                    }
                }
            }
        }

        // 音频列表
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
                    
                    // 时长（音频特有）
                    Text {
                        text: "时长"
                        font.pixelSize: 14
                        font.weight: Font.Medium
                        color: themeManager.textPrimaryColor
                        Layout.preferredWidth: 80
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
                id: audioList
                anchors.top: headerRow.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.margins: 8
                
                model: typefilesVM ? typefilesVM.files : []
                
                delegate: Rectangle {
                    width: audioList.width
                    height: 60
                    color: mouseArea.containsMouse ? themeManager.hoverColor : "transparent"
                    radius: 4
                    
                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 16
                        spacing: 16
                        
                        // 音频图标
                        Rectangle {
                            width: 40
                            height: 40
                            radius: 20
                            color: themeManager.primaryColor + "20"
                            
                            Text {
                                anchors.centerIn: parent
                                text: getAudioIcon(modelData ? modelData.name : "")
                                font.pixelSize: 18
                                color: themeManager.primaryColor
                            }
                        }
                        
                        // 文件名
                        Column {
                            Layout.preferredWidth: 280
                            spacing: 4
                            
                            Text {
                                text: modelData ? modelData.name : ""
                                font.pixelSize: 14
                                font.weight: Font.Medium
                                color: themeManager.textPrimaryColor
                                elide: Text.ElideRight
                            }
                            
                            Text {
                                text: getAudioFormat(modelData ? modelData.name : "")
                                font.pixelSize: 12
                                color: themeManager.textSecondaryColor
                            }
                        }
                        
                        // 文件大小
                        Text {
                            text: formatFileSize(modelData ? modelData.size : 0)
                            font.pixelSize: 12
                            color: themeManager.textSecondaryColor
                            Layout.preferredWidth: 80
                        }
                        
                        // 时长（音频特有）
                        Text {
                            text: getAudioDuration(modelData ? modelData.size : 0)
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
                                text: "播放"
                                height: 32
                                padding: 8
                                
                                background: Rectangle {
                                    radius: 16
                                    color: parent.pressed ? themeManager.primaryColor + "80" : themeManager.primaryColor
                                }
                                
                                contentItem: Row {
                                    spacing: 4
                                    
                                    Text {
                                        text: "▶"
                                        font.pixelSize: 12
                                        color: "white"
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                    
                                    Text {
                                        text: parent.text
                                        font.pixelSize: 12
                                        color: "white"
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                }
                                
                                onClicked: {
                                    console.log("播放音频:", modelData.relPath)
                                    if (modelData && modelData.relPath) {
                                        // 调用系统音频播放器
                                        // fileVM.open_file_with_system(modelData.relPath)
                                    }
                                }
                            }
                            
                            Button {
                                text: "下载"
                                height: 32
                                padding: 8
                                
                                background: Rectangle {
                                    radius: 16
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
                                    console.log("下载音频:", modelData.relPath)
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
                            console.log("点击音频:", modelData.name)
                        }
                        
                        onDoubleClicked: {
                            console.log("双击播放音频:", modelData.relPath)
                            if (modelData && modelData.relPath) {
                                // 调用系统音频播放器
                                // fileVM.open_file_with_system(modelData.relPath)
                            }
                        }
                    }
                }
            }
        }
    }
    
    // 获取音频图标
    function getAudioIcon(fileName) {
        if (!fileName) return "🎵"
        
        let ext = fileName.split('.').pop().toLowerCase()
        switch (ext) {
            case 'mp3': return "🎵"
            case 'wav': return "🎵"
            case 'flac': return "🎵"
            case 'aac': return "🎵"
            case 'ogg': return "🎵"
            case 'wma': return "🎵"
            case 'm4a': return "🎵"
            default: return "🎵"
        }
    }
    
    // 获取音频格式
    function getAudioFormat(fileName) {
        if (!fileName) return ""
        
        let ext = fileName.split('.').pop().toLowerCase()
        return ext.toUpperCase()
    }
    
    // 估算音频时长（基于文件大小，这是一个粗略估算）
    function getAudioDuration(fileSize) {
        if (fileSize === 0) return "--:--"
        
        // 假设平均比特率为 128kbps，这是一个粗略估算
        const avgBitrate = 128 * 1024 // 128 kbps in bits per second
        const durationSeconds = (fileSize * 8) / avgBitrate
        
        const minutes = Math.floor(durationSeconds / 60)
        const seconds = Math.floor(durationSeconds % 60)
        
        return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
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