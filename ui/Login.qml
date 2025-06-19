import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    width: 400
    height: 300

    property bool showPassword: false

    // Material Design 颜色
    property color primaryColor: "#2196F3"
    property color primaryDarkColor: "#1976D2"
    property color accentColor: "#FF4081"
    property color backgroundColor: "#FAFAFA"
    property color surfaceColor: "#FFFFFF"
    property color textPrimaryColor: "#212121"
    property color textSecondaryColor: "#757575"
    property color dividerColor: "#BDBDBD"

    Rectangle {
        anchors.fill: parent
        color: backgroundColor

        // 主卡片容器
        Rectangle {
            id: mainCard
            width: 320
            height: showPassword ? 200 : 120
            anchors.centerIn: parent
            radius: 8
            color: surfaceColor
            
            // 简单的阴影效果（使用边框模拟）
            border.color: "#20000000"
            border.width: 1

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 24
                spacing: 16

                // 标题
                Text {
                    text: "NAS 文件管理系统"
                    font.pixelSize: 20
                    font.weight: Font.Medium
                    color: textPrimaryColor
                    Layout.alignment: Qt.AlignHCenter
                }

                // 用户选择按钮区域
                Row {
                    visible: !showPassword
                    Layout.alignment: Qt.AlignHCenter
                    spacing: 12

                    Button {
                        text: "Admin"
                        width: 120
                        height: 48
                        
                        background: Rectangle {
                            radius: 24
                            color: parent.pressed ? primaryDarkColor : primaryColor
                            border.color: "#40000000"
                            border.width: 1
                        }
                        
                        contentItem: Text {
                            text: parent.text
                            font.pixelSize: 14
                            font.weight: Font.Medium
                            color: "white"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        
                        onClicked: {
                            loginVM.selectUser("admin")
                            showPassword = true
                        }
                    }

                    Button {
                        text: "Anonymous"
                        width: 120
                        height: 48
                        
                        background: Rectangle {
                            radius: 24
                            color: parent.pressed ? "#E0E0E0" : "#F5F5F5"
                            border.color: dividerColor
                            border.width: 1
                        }
                        
                        contentItem: Text {
                            text: parent.text
                            font.pixelSize: 14
                            font.weight: Font.Medium
                            color: textPrimaryColor
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        
                        onClicked: {
                            loginVM.selectUser("public")
                            showPassword = true
                        }
                    }
                }

                // 密码输入区域
                ColumnLayout {
                    visible: showPassword
                    Layout.fillWidth: true
                    spacing: 16

                    // 密码输入框
                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 48
                        radius: 24
                        color: "#F5F5F5"
                        border.color: passwordField.focus ? primaryColor : dividerColor
                        border.width: passwordField.focus ? 2 : 1

                        TextField {
                            id: passwordField
                            anchors.fill: parent
                            anchors.margins: 4
                            placeholderText: "请输入密码"
                            echoMode: TextInput.Password
                            font.pixelSize: 14
                            color: textPrimaryColor
                            background: null
                            padding: 16
                            
                            onTextChanged: loginVM.setPassword(text)
                        }
                    }

                    // 登录按钮
                    Button {
                        text: "登录"
                        Layout.fillWidth: true
                        Layout.preferredHeight: 48
                        
                        background: Rectangle {
                            radius: 24
                            color: parent.pressed ? primaryDarkColor : primaryColor
                            border.color: "#40000000"
                            border.width: 1
                        }
                        
                        contentItem: Text {
                            text: parent.text
                            font.pixelSize: 14
                            font.weight: Font.Medium
                            color: "white"
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        
                        onClicked: loginVM.doLogin()
                    }
                }

                // 结果显示
                Text {
                    id: resultText
                    text: ""
                    font.pixelSize: 12
                    color: resultText.text.includes("成功") ? "#4CAF50" : "#F44336"
                    Layout.alignment: Qt.AlignHCenter
                    visible: resultText.text !== ""
                }
            }
        }
    }

    Connections {
        target: loginVM
        function onLoginResult(msg) {
            resultText.text = msg
        }
    }
} 