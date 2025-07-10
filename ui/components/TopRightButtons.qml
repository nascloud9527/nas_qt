import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    spacing: 20
    anchors.top: parent.top
    anchors.topMargin: 50
    anchors.right: parent.right
    anchors.rightMargin: 50

    Repeater {
        model: [
            { icon: "🖼️" },
            { icon: "📶" },
            { icon: "⚙️" },
            { icon: "❌" }
        ]

        delegate: Button {
            width: 48
            height: 48
            background: Rectangle {
                color: "#1A2B6D80"
                radius: 24
            }

            contentItem: Text {
                text: modelData.icon
                anchors.centerIn: parent
                font.pixelSize: 24
            }

            onClicked: {
                console.log("Clicked:", modelData.icon)
            }
        }
    }
}
