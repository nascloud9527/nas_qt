import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import "components"

Item  {
    id: mainPage
    anchors.fill: parent

    // 背景
    // Background { }
    // 使用背景图片组件
    BackgroundImage {
        anchors.fill: parent
    }

    // 时间天气
    TimeWeatherCard { }

    // 右上角按钮
    // TopRightButtons { }
    
    // 页面加载器
    Loader {
        id: pageLoader
        anchors.fill: parent
        // 默认不加载任何页面，显示主菜单
        
        // 将pageLoader传递给加载的页面
        property var pageLoaderRef: pageLoader
        
        // 监听加载的页面的返回信号
        onItemChanged: {
            if (item && item.goBack) {
                item.goBack.connect(function() {
                    pageLoader.source = ""
                    // 显示底部菜单
                    mainMenu.visible = true
                })
            }
        }
        
        // 监听source变化
        onSourceChanged: {
            if (source && source !== "") {
                // 有页面加载时，隐藏底部菜单
                mainMenu.visible = false
            } else {
                // 没有页面加载时，显示底部菜单
                mainMenu.visible = true
            }
        }
    }

    // 底部菜单
    MainMenu_tv { 
        id: mainMenu
        onPageSelected: function(pagePath) {
            console.log("切换到页面:", pagePath)
            pageLoader.source = pagePath
        }
    }
}
