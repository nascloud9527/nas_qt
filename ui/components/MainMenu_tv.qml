// components/MainMenu.qml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    id: mainMenu
    spacing: 40
    anchors.bottom: parent.bottom
    anchors.bottomMargin: 50
    anchors.horizontalCenter: parent.horizontalCenter

    // 页面选择信号
    signal pageSelected(string pagePath)

    Repeater {
        model: [
            { icon: "video_icon.png", titleCN: "视频", titleEN: "Video", pagePath: "pages/VideoPage.qml" },
            { icon: "music_icon.png", titleCN: "音乐", titleEN: "Music", pagePath: "pages/AudioPage.qml" },
            { icon: "photo_icon.png", titleCN: "照片", titleEN: "Photo", pagePath: "pages/PhotoPage.qml" },
            { icon: "folder_icon.png", titleCN: "文件夹", titleEN: "Folder", pagePath: "pages/DocumentPage.qml" }
        ]

        delegate: Rectangle {
            width: 200
            height: 150
            radius: 8
            color: "#1A2B6D80"

            ColumnLayout {
                anchors.centerIn: parent
                spacing: 10

                Image {
                    source: modelData.icon
                    width: 48
                    height: 48
                }
                Text {
                    text: modelData.titleCN
                    color: "white"
                    font.pixelSize: 20
                }
                Text {
                    text: modelData.titleEN
                    color: "white"
                    font.pixelSize: 14
                }
            }

            MouseArea {
                anchors.fill: parent
                onClicked: {
                    console.log("Clicked: " + modelData.titleEN + " -> " + modelData.pagePath)
                    mainMenu.pageSelected(modelData.pagePath)
                }
            }
        }
    }
}
