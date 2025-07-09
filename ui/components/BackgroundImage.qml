import QtQuick 6.5
import QtQuick.Controls 2.15

Item {
    id: backgroundImage
    anchors.fill: parent
    
    // 背景图片
    Image {
        id: backgroundImg
        anchors.fill: parent
        source: "/home/lanyang/work2/tv_qt2/ui_background/IMG_1326.PNG"
        fillMode: Image.PreserveAspectCrop  // 保持宽高比并裁剪
        smooth: true
        mipmap: true
        
        // 加载状态处理
        onStatusChanged: {
            if (status === Image.Ready) {
                console.log("背景图片加载成功")
            } else if (status === Image.Error) {
                console.log("背景图片加载失败:", source)
            }
        }
        
        // 添加一个半透明的遮罩层，让内容更容易阅读
        Rectangle {
            anchors.fill: parent
            color: "#80000000"  // 半透明黑色遮罩
            opacity: 0.3  // 30%透明度
        }
    }
    
    // 可选：添加渐变遮罩效果，增强视觉效果
    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#40000000" }  // 顶部稍微暗一些
            GradientStop { position: 0.3; color: "#20000000" }  // 上部较亮
            GradientStop { position: 0.7; color: "#20000000" }  // 下部较亮
            GradientStop { position: 1.0; color: "#60000000" }  // 底部稍微暗一些
        }
    }
    
    // 如果图片加载失败，显示备用背景
    Rectangle {
        anchors.fill: parent
        visible: backgroundImg.status === Image.Error
        gradient: Gradient {
            GradientStop { position: 0.0; color: "#2c3e50" }
            GradientStop { position: 1.0; color: "#34495e" }
        }
    }
} 