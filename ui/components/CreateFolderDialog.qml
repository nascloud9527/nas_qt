import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Dialog {
    id: createFolderDialog
    modal: true
    width: 400
    height: 220  // 增加高度以容纳错误信息
    z: 1000
    
    // 居中定位
    anchors.centerIn: parent
    
    property string folderName: ""
    property string errorMessage: ""  // 添加错误信息属性
    signal folderCreated(string name)
    signal dialogCancelled()
    
    background: Rectangle {
        radius: 12
        color: themeManager.surfaceColor || "#FFFFFF"
        border.color: themeManager.dividerColor || "#BDBDBD"
        border.width: 1
    }
    
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 24
        spacing: 20
        
        // 标题
        RowLayout {
            Layout.fillWidth: true
            spacing: 8
            
            Text {
                text: "📁"
                font.pixelSize: 20
            }
            
            Text {
                text: "创建文件夹"
                font.pixelSize: 18
                font.weight: Font.Bold
                color: themeManager.textPrimaryColor || "#212121"
                Layout.fillWidth: true
            }
        }
        
        // 输入框
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 40
            radius: 8
            color: themeManager.backgroundColor || "#FAFAFA"
            border.color: folderNameInput.focus ? (themeManager.primaryColor || "#2196F3") : (themeManager.dividerColor || "#BDBDBD")
            border.width: folderNameInput.focus ? 2 : 1
            
            // 边框颜色动画
            Behavior on border.color {
                ColorAnimation { duration: 200 }
            }
            
            // 边框宽度动画
            Behavior on border.width {
                NumberAnimation { duration: 200 }
            }
            
            TextInput {
                id: folderNameInput
                anchors.fill: parent
                anchors.margins: 12
                text: createFolderDialog.folderName
                font.pixelSize: 14
                color: themeManager.textPrimaryColor || "#212121"
                verticalAlignment: TextInput.AlignVCenter
                
                onTextChanged: {
                    createFolderDialog.folderName = text
                    // 当用户开始输入时，清除错误信息
                    if (text !== "") {
                        createFolderDialog.errorMessage = ""
                    }
                }
                
                Component.onCompleted: {
                    forceActiveFocus()
                    selectAll()
                }
                
                // 处理回车键
                Keys.onReturnPressed: {
                    if (createFolderDialog.folderName.trim() !== "") {
                        createFolderDialog.folderCreated(createFolderDialog.folderName.trim())
                        // 注意：这里不关闭对话框，让调用者决定是否关闭
                    }
                }
                
                // 处理Escape键
                Keys.onEscapePressed: {
                    createFolderDialog.dialogCancelled()
                    createFolderDialog.close()
                }
            }
            
            // 占位符文本
            Text {
                anchors.fill: parent
                anchors.margins: 12
                text: "请输入文件夹名称"
                font.pixelSize: 14
                color: themeManager.textSecondaryColor || "#757575"
                verticalAlignment: Text.AlignVCenter
                visible: folderNameInput.text === ""
            }
        }
        
        // 错误信息显示
        Text {
            id: errorText
            Layout.fillWidth: true
            text: createFolderDialog.errorMessage
            font.pixelSize: 12
            color: "#FF4444"  // 红色错误文本
            visible: createFolderDialog.errorMessage !== ""
            wrapMode: Text.WordWrap
        }
        
        // 按钮
        RowLayout {
            Layout.fillWidth: true
            spacing: 12
            
            // 取消按钮
            Button {
                text: "取消"
                Layout.fillWidth: true
                Layout.preferredHeight: 36
                
                background: Rectangle {
                    radius: 18
                    color: parent.pressed ? (themeManager.hoverColor || "#F0F0F0") : 
                           parent.hovered ? (themeManager.hoverColor || "#F0F0F0") : (themeManager.backgroundColor || "#FFFFFF")
                    border.color: themeManager.dividerColor || "#BDBDBD"
                    border.width: 1
                }
                
                contentItem: Text {
                    text: parent.text
                    font.pixelSize: 12
                    font.weight: Font.Medium
                    color: themeManager.textPrimaryColor || "#212121"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                
                onClicked: {
                    createFolderDialog.dialogCancelled()
                    createFolderDialog.close()
                }
            }
            
            // 创建按钮
            Button {
                text: "创建"
                Layout.fillWidth: true
                Layout.preferredHeight: 36
                enabled: folderNameInput.text.trim() !== ""
                
                background: Rectangle {
                    radius: 18
                    color: parent.enabled ? 
                           (parent.pressed ? (themeManager.primaryDarkColor || "#1976D2") : 
                            parent.hovered ? (themeManager.primaryColor || "#2196F3") : (themeManager.primaryColor || "#2196F3")) :
                           (themeManager.disabledColor || "#E0E0E0")
                    border.color: parent.enabled ? "#40000000" : (themeManager.disabledColor || "#E0E0E0")
                    border.width: 1
                }
                
                contentItem: Text {
                    text: parent.text
                    font.pixelSize: 12
                    font.weight: Font.Medium
                    color: parent.enabled ? "white" : (themeManager.textDisabledColor || "#9E9E9E")
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                
                onClicked: {
                    createFolderDialog.folderCreated(folderNameInput.text.trim())
                    // 注意：这里不关闭对话框，让调用者决定是否关闭
                }
            }
        }
    }
    
    // 打开时的动画效果
    enter: Transition {
        NumberAnimation { 
            property: "opacity"; 
            from: 0; 
            to: 1; 
            duration: 200 
        }
        NumberAnimation { 
            property: "scale"; 
            from: 0.8; 
            to: 1; 
            duration: 200 
        }
    }
    
    // 关闭时的动画效果
    exit: Transition {
        NumberAnimation { 
            property: "opacity"; 
            from: 1; 
            to: 0; 
            duration: 150 
        }
        NumberAnimation { 
            property: "scale"; 
            from: 1; 
            to: 0.8; 
            duration: 150 
        }
    }
} 