import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Item {
    id: mainPage
    anchors.fill: parent

    // Material Design 颜色
    property color primaryColor: "#2196F3"
    property color primaryDarkColor: "#1976D2"
    property color backgroundColor: "#FAFAFA"
    property color surfaceColor: "#FFFFFF"
    property color textPrimaryColor: "#212121"
    property color textSecondaryColor: "#757575"
    property color dividerColor: "#BDBDBD"

    Rectangle {
        anchors.fill: parent
        color: backgroundColor

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
                color: dividerColor
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
                color: dividerColor
            }

            // 3. 文件列表区
            Loader {
                Layout.fillWidth: true
                Layout.fillHeight: true
                source: "components/FileListArea.qml"
            }
        }
    }
} 