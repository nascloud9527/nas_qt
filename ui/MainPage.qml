import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    id: mainPage
    anchors.fill: parent

    Rectangle {
        anchors.fill: parent
        color: themeManager.backgroundColor

        ColumnLayout {
            anchors.fill: parent
            spacing: 0

            // 1. 导航区域
            Loader {
                Layout.fillWidth: true
                Layout.preferredHeight: 60
                source: "components/NavigationBar.qml"
            }

            // 分隔线
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 1
                color: themeManager.dividerColor
            }

            // 2. 工具栏
            Loader {
                Layout.fillWidth: true
                Layout.preferredHeight: 50
                source: "components/ToolBar.qml"
            }

            // 分隔线
            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 1
                color: themeManager.dividerColor
            }

            // 3. 文件列表区
            Loader {
                Layout.fillWidth: true
                Layout.fillHeight: true
                source: "components/FileListArea.qml"
            }
        }

        // 主题切换按钮（右上角）
        Button {
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.margins: 16
            width: 40
            height: 40
            
            background: Rectangle {
                radius: 20
                color: themeManager.surfaceColor
                border.color: themeManager.dividerColor
                border.width: 1
            }
            
            contentItem: Text {
                text: themeManager.isDarkTheme ? "☀️" : "🌙"
                font.pixelSize: 16
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            
            onClicked: {
                themeManager.toggleTheme()
            }
        }
    }
} 