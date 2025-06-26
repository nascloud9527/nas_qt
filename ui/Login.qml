import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    width: 400
    height: 300

    property bool showPassword: false

    // 添加信号通知登录成功
    signal loginSuccess()

    Rectangle {
        anchors.fill: parent
        color: themeManager.backgroundColor

        // 主卡片容器
        Rectangle {
            id: mainCard
            width: 320
            height: showPassword ? 200 : 120
            anchors.centerIn: parent
            radius: 8
            color: themeManager.surfaceColor
            
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
                    color: themeManager.textPrimaryColor
                    Layout.alignment: Qt.AlignHCenter
                }

                // 用户选择按钮区域
                Row {
                    Layout.alignment: Qt.AlignHCenter
                    visible: !showPassword
                    spacing: 12

                    Button {
                        text: "Admin"
                        width: 120
                        height: 48
                        
                        background: Rectangle {
                            radius: 24
                            color: parent.pressed ? themeManager.primaryDarkColor : themeManager.primaryColor
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
                        text: "Public"
                        width: 120
                        height: 48
                        
                        background: Rectangle {
                            radius: 24
                            color: parent.pressed ? themeManager.hoverColor : themeManager.backgroundColor
                            border.color: themeManager.dividerColor
                            border.width: 1
                        }
                        
                        contentItem: Text {
                            text: parent.text
                            font.pixelSize: 14
                            font.weight: Font.Medium
                            color: themeManager.textPrimaryColor
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
                        color: themeManager.backgroundColor
                        border.color: passwordField.focus ? themeManager.primaryColor : themeManager.dividerColor
                        border.width: passwordField.focus ? 2 : 1

                        TextField {
                            id: passwordField
                            anchors.fill: parent
                            anchors.margins: 4
                            placeholderText: "请输入密码"
                            echoMode: TextInput.Password
                            font.pixelSize: 14
                            color: themeManager.textPrimaryColor
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
                            color: parent.pressed ? themeManager.primaryDarkColor : themeManager.primaryColor
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
                    color: resultText.text.includes("成功") ? themeManager.successColor : themeManager.errorColor
                    Layout.alignment: Qt.AlignHCenter
                    visible: resultText.text !== ""
                }
            }
        }

        // 主题切换按钮（右上角）
        // Button {
        //     anchors.top: parent.top
        //     anchors.right: parent.right
        //     anchors.margins: 16
        //     width: 40
        //     height: 40
            
        //     background: Rectangle {
        //         radius: 20
        //         color: themeManager.surfaceColor
        //         border.color: themeManager.dividerColor
        //         border.width: 1
        //     }
            
        //     contentItem: Text {
        //         text: themeManager.isDarkTheme ? "☀️" : "🌙"
        //         font.pixelSize: 16
        //         horizontalAlignment: Text.AlignHCenter
        //         verticalAlignment: Text.AlignVCenter
        //     }
            
        //     onClicked: {
        //         themeManager.toggleTheme()
        //     }
        // }
    }

    Connections {
        target: loginVM
        function onLoginResult(msg) {
            resultText.text = msg
            if (msg.includes("成功")) {
                // 登录成功后发送信号
                loginSuccess()
            }
        }
    }
} 