import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Effects

Item {
    // 铺满整个屏幕
    anchors.fill: parent

    property bool showPassword: false
    property int currentUserIndex: 0
    property var users: ["admin", "public"]

    // 添加信号通知登录成功
    signal loginSuccess()

    // 使用背景图片组件
    BackgroundImage {
        anchors.fill: parent
    }

    // 主卡片容器 - 调整尺寸以适应大屏幕
    Rectangle {
        id: mainCard
        width: Math.min(parent.width * 0.8, 600)  // 响应式宽度
        height: showPassword ? Math.min(parent.height * 0.6, 400) : Math.min(parent.height * 0.4, 300)
        anchors.centerIn: parent
        radius: 16  // 增大圆角
        color: "transparent"  // 完全透明
        
        // 移除阴影效果，让背景完全显示
        // layer.enabled: false

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 40  // 增大边距
            spacing: 24  // 增大间距

            // 标题 - 增大字体
            // Text {
            //     text: "NAS 文件管理系统"
            //     font.pixelSize: 32  // 增大字体
            //     font.weight: Font.Medium
            //     color: themeManager.textPrimaryColor
            //     Layout.alignment: Qt.AlignHCenter
            // }

            // 用户选择区域
            Row {
                Layout.alignment: Qt.AlignHCenter
                visible: !showPassword
                spacing: 60  // 增大间距，让按钮分开更远

                // 向左切换按钮 - 增大尺寸
                Button {
                    text: "←"
                    width: 80  // 增大按钮宽度，与中间按钮高度一致
                    height: 80  // 增大按钮高度，与中间按钮高度一致
                    
                    background: Rectangle {
                        radius: 40  // 增大圆角，与高度一致
                        color: parent.pressed ? "#40ffffff" : "#20ffffff"  // 半透明白色背景
                        border.color: "#40ffffff"  // 半透明白色边框
                        border.width: 1
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font.pixelSize: 28  // 增大字体，适应更大的按钮
                        font.weight: Font.Bold
                        color: "white"  // 白色文字，在透明背景上更清晰
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        console.log("向左切换按钮被点击")
                        currentUserIndex = (currentUserIndex - 1 + users.length) % users.length
                        console.log("新的用户索引:", currentUserIndex, "用户:", users[currentUserIndex])
                        // 移除 loginVM.selectUser 调用，避免直接进入登录界面
                    }
                }

                // 中间用户按钮 - 增大尺寸
                Button {
                    text: users[currentUserIndex]
                    width: 200  // 增大宽度
                    height: 80  // 增大高度
                    
                    background: Rectangle {
                        radius: 40
                        color: parent.pressed ? "#80ffffff" : "#60ffffff"  // 半透明白色背景
                        border.color: "#80ffffff"  // 半透明白色边框
                        border.width: 2
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font.pixelSize: 20  // 增大字体
                        font.weight: Font.Medium
                        color: "#ffffff"  // 深色文字，在白色透明背景上清晰可见
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        console.log("中间用户按钮被点击，用户:", users[currentUserIndex])
                        loginVM.selectUser(users[currentUserIndex])
                        showPassword = true
                    }
                }

                // 向右切换按钮 - 增大尺寸
                Button {
                    text: "→"
                    width: 80  // 增大按钮宽度，与中间按钮高度一致
                    height: 80  // 增大按钮高度，与中间按钮高度一致
                    
                    background: Rectangle {
                        radius: 40  // 增大圆角，与高度一致
                        color: parent.pressed ? "#40ffffff" : "#20ffffff"  // 半透明白色背景
                        border.color: "#40ffffff"  // 半透明白色边框
                        border.width: 1
                    }
                    
                    contentItem: Text {
                        text: parent.text
                        font.pixelSize: 28  // 增大字体，适应更大的按钮
                        font.weight: Font.Bold
                        color: "white"  // 白色文字，在透明背景上更清晰
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }
                    
                    onClicked: {
                        console.log("向右切换按钮被点击")
                        currentUserIndex = (currentUserIndex + 1) % users.length
                        console.log("新的用户索引:", currentUserIndex, "用户:", users[currentUserIndex])
                        // 移除 loginVM.selectUser 调用，避免直接进入登录界面
                    }
                }
            }

            // 密码输入区域
            ColumnLayout {
                visible: showPassword
                Layout.fillWidth: true
                spacing: 24  // 增大间距

                // 显示当前用户 - 增大字体
                Text {
                    text: "当前用户: " + users[currentUserIndex]
                    font.pixelSize: 18  // 增大字体
                    font.weight: Font.Medium
                    color: "white"  // 改为白色，与用户选择区域一致
                    Layout.alignment: Qt.AlignHCenter
                }

                // 密码输入框 - 增大尺寸
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 80  // 增大高度
                    radius: 40  // 增大圆角
                    color: "#60ffffff"  // 半透明白色背景，与用户选择区域一致
                    border.color: passwordField.focus ? "#80ffffff" : "#40ffffff"  // 半透明白色边框
                    border.width: passwordField.focus ? 3 : 2  // 增大边框

                    TextField {
                        id: passwordField
                        anchors.fill: parent
                        anchors.margins: 8  // 增大边距
                        placeholderText: "请输入密码"
                        echoMode: TextInput.Password
                        font.pixelSize: 18  // 增大字体
                        color: "#ffffff"  // 深色文字，与用户选择区域一致
                        background: null
                        padding: 24  // 增大内边距
                        
                        onTextChanged: loginVM.setPassword(text)
                    }
                }

                // 按钮区域 - 水平并排显示
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 16  // 按钮之间的间距

                    // 登录按钮 - 增大尺寸
                    Button {
                        text: "登录"
                        Layout.fillWidth: true
                        Layout.preferredHeight: 80  // 增大高度
                        
                        background: Rectangle {
                            radius: 40  // 增大圆角
                            color: parent.pressed ? "#80ffffff" : "#60ffffff"  // 半透明白色背景，与用户选择区域一致
                            border.color: "#80ffffff"  // 半透明白色边框
                            border.width: 2
                        }
                        
                        contentItem: Text {
                            text: parent.text
                            font.pixelSize: 20  // 增大字体
                            font.weight: Font.Medium
                            color: "#ffffff"  // 深色文字，与用户选择区域一致
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        
                        onClicked: loginVM.doLogin()
                    }

                    // 取消按钮 - 返回到选择用户
                    Button {
                        text: "取消"
                        Layout.fillWidth: true
                        Layout.preferredHeight: 80  // 增大高度
                        
                        background: Rectangle {
                            radius: 40  // 增大圆角
                            color: parent.pressed ? "#80ffffff" : "#60ffffff"  // 半透明白色背景，与用户选择区域一致
                            border.color: "#80ffffff"  // 半透明白色边框
                            border.width: 2
                        }
                        
                        contentItem: Text {
                            text: parent.text
                            font.pixelSize: 20  // 增大字体
                            font.weight: Font.Medium
                            color: "#ffffff"  // 深色文字，与用户选择区域一致
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }
                        
                        onClicked: loginVM.goBackToUserSelection()
                    }
                }
            }

            // 结果显示 - 增大字体
            Text {
                id: resultText
                text: ""
                font.pixelSize: 16  // 增大字体
                color: resultText.text.includes("成功") ? themeManager.successColor : themeManager.errorColor
                Layout.alignment: Qt.AlignHCenter
                visible: resultText.text !== ""
            }
        }
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
        
        function onShowPasswordInput(show) {
            showPassword = show
        }
    }
} 