import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Dialog {
    id: deleteConfirmDialog
    modal: true
    anchors.centerIn: parent
    width: 400
    height: 200

    title: "确认删除"
    
    property var filesToDelete: []
    // property string title: "确认删除"
    property string message: "确定要删除选中的文件吗？"
    
    // 信号定义
    signal deleteConfirmed()
    signal deleteCancelled()
    
    background: Rectangle {
        radius: 8
        color: themeManager.surfaceColor
        border.color: themeManager.dividerColor
        border.width: 1
    }
    
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 12
        
        // 标题和图标
        RowLayout {
            Layout.fillWidth: true
            spacing: 8
            
            Text {
                text: "⚠️"
                font.pixelSize: 24
            }
            
            Text {
                text: deleteConfirmDialog.title
                font.pixelSize: 16
                font.weight: Font.Bold
                color: themeManager.textPrimaryColor
                Layout.fillWidth: true
            }
        }
        
        // 消息内容
        Text {
            text: message
            font.pixelSize: 14
            color: themeManager.textSecondaryColor
            wrapMode: Text.WordWrap
            Layout.fillWidth: true
        }
        
        // 文件列表
        ScrollView {
            Layout.fillWidth: true
            Layout.preferredHeight: 60
            visible: filesToDelete.length > 0
            
            ListView {
                model: filesToDelete
                delegate: Text {
                    text: modelData
                    font.pixelSize: 12
                    color: themeManager.textSecondaryColor
                    elide: Text.ElideRight
                    width: parent.width
                }
            }
        }
        
        // 按钮区域
        RowLayout {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignRight
            spacing: 8
            
            Button {
                text: "取消"
                Layout.preferredWidth: 80
                Layout.preferredHeight: 32
                
                background: Rectangle {
                    radius: 16
                    color: parent.pressed ? themeManager.surfaceDarkColor : themeManager.surfaceColor
                    border.color: themeManager.dividerColor
                    border.width: 1
                }
                
                contentItem: Text {
                    text: parent.text
                    font.pixelSize: 12
                    font.weight: Font.Medium
                    color: themeManager.textPrimaryColor
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                
                onClicked: {
                    deleteConfirmDialog.deleteCancelled()
                    deleteConfirmDialog.close()
                }
            }
            
            Button {
                text: "删除"
                Layout.preferredWidth: 80
                Layout.preferredHeight: 32
                
                background: Rectangle {
                    radius: 16
                    color: parent.pressed ? themeManager.errorDarkColor : themeManager.errorColor
                    border.color: "#40000000"
                    border.width: 1
                }
                
                contentItem: Text {
                    text: parent.text
                    font.pixelSize: 12
                    font.weight: Font.Medium
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                
                onClicked: {
                    console.log("准备删除以下文件：", deleteConfirmDialog.filesToDelete)
                    deleteConfirmDialog.deleteConfirmed()
                    deleteConfirmDialog.close()
                }
            }
        }
    }
} 