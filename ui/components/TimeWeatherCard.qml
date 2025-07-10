import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects

Rectangle {
    width: 300
    height: 150
    radius: 10
    color: "#1A2B6D80"
    anchors.left: parent.left
    anchors.leftMargin: 50
    anchors.top: parent.top
    anchors.topMargin: 50

    // 添加阴影效果
    layer.enabled: true
    layer.effect: DropShadow {
        transparentBorder: true
        horizontalOffset: 0
        verticalOffset: 0
        radius: shadowRadius
        samples: 17
        color: "#40000000"
    }

    property string hourText: Qt.formatTime(new Date(), "hh")
    property string minuteText: Qt.formatTime(new Date(), "mm")
    property string dateText: Qt.formatDate(new Date(), "yyyy-MM-dd")
    property string colonChar: ":"
    property real shadowRadius: 0

    Timer {
        interval: 1000
        running: true
        repeat: true
        onTriggered: {
            var now = new Date()
            var newHourText = Qt.formatTime(now, "hh")
            var newMinuteText = Qt.formatTime(now, "mm")
            
            // 检查时间是否发生变化，触发动画
            if (hourText !== newHourText) {
                hourText = newHourText
                hourChangeAnimation.start()
            }
            if (minuteText !== newMinuteText) {
                minuteText = newMinuteText
                minuteChangeAnimation.start()
            }
            
            dateText = Qt.formatDate(now, "yyyy-MM-dd")
        }
    }

    // 时间数字切换动画
    SequentialAnimation {
        id: hourChangeAnimation
        NumberAnimation {
            target: hourTextItem
            property: "opacity"
            from: 1.0
            to: 0.0
            duration: 150
            easing.type: Easing.OutQuad
        }
        NumberAnimation {
            target: hourTextItem
            property: "opacity"
            from: 0.0
            to: 1.0
            duration: 150
            easing.type: Easing.InQuad
        }
    }

    SequentialAnimation {
        id: minuteChangeAnimation
        NumberAnimation {
            target: minuteTextItem
            property: "opacity"
            from: 1.0
            to: 0.0
            duration: 150
            easing.type: Easing.OutQuad
        }
        NumberAnimation {
            target: minuteTextItem
            property: "opacity"
            from: 0.0
            to: 1.0
            duration: 150
            easing.type: Easing.InQuad
        }
    }

    // 冒号闪烁动画
    SequentialAnimation {
        id: colonBlinkAnimation
        running: true
        loops: Animation.Infinite
        NumberAnimation {
            target: colonTextItem
            property: "opacity"
            from: 1.0
            to: 0.3
            duration: 500
            easing.type: Easing.InOutQuad
        }
        NumberAnimation {
            target: colonTextItem
            property: "opacity"
            from: 0.3
            to: 1.0
            duration: 500
            easing.type: Easing.InOutQuad
        }
    }


    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 20
        spacing: 10

        RowLayout {
            spacing: 10

            RowLayout {
                spacing: 2

                Text {
                    id: hourTextItem
                    text: hourText
                    color: "white"
                    font.pixelSize: 48
                    font.bold: true
                }

                Text {
                    id: colonTextItem
                    text: colonChar
                    color: "white"
                    font.pixelSize: 48
                    font.bold: true
                }

                Text {
                    id: minuteTextItem
                    text: minuteText
                    color: "white"
                    font.pixelSize: 48
                    font.bold: true
                }
            }

            ColumnLayout {
                Text {
                    text: dateText
                    color: "white"
                    font.pixelSize: 16
                }
                Text {
                    text: weatherVM.weather + " " + weatherVM.tempRange
                    color: "white"
                    font.pixelSize: 16
                }
            }
        }

        RowLayout {
            spacing: 5
            Image {
                source: "location_icon.png"
                width: 16
                height: 16
            }
            Text {
                text: weatherVM.city
                color: "white"
                font.pixelSize: 16
            }
        }
    }
}
