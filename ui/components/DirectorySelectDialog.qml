import QtQuick 6.5
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Dialog {
    id: directorySelectDialog
    modal: true
    anchors.centerIn: parent
    width: 500
    height: 400
    
    property string dialogTitle: "选择目标目录"
    property var directoryTree: []  // 原始目录树数据（需保持结构完整）
    property string selectedDirectory: ""
    
    signal directorySelected(string directory)
    signal dialogCancelled()

    background: Rectangle {
        radius: 8
        color: "#FFFFFF"
        border.color: "#E0E0E0"
        border.width: 1
    }
    
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 12
        
        // 标题
        Text {
            text: dialogTitle
            font.pixelSize: 16
            font.weight: Font.Bold
            color: "#333333"
            Layout.fillWidth: true
        }
        
        // 目录树视图
        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "#F5F5F5"
            border.color: "#E0E0E0"
            border.width: 1
            radius: 4
            
            ListView {
                id: directoryListView
                anchors.fill: parent
                anchors.margins: 8
                
                model: ListModel {
                    id: directoryModel
                }
                
                delegate: Rectangle {
                    width: directoryListView.width
                    height: 40
                    color: mouseArea.containsMouse ? "#E3F2FD" : "transparent"
                    radius: 4
                    
                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 8
                        spacing: 8
                        
                        // 缩进（根据层级）
                        Item {
                            Layout.preferredWidth: model.level * 20
                        }
                        
                        // 展开/折叠图标
                        Text {
                            text: model.hasChildren ? (model.expanded ? "▼" : "▶") : "  "
                            font.pixelSize: 12
                            color: "#666666"
                            Layout.preferredWidth: 20
                        }
                        
                        // 文件夹图标
                        Text {
                            text: "📁"
                            font.pixelSize: 16
                            color: "#666666"
                        }
                        
                        // 目录名
                        Text {
                            text: model.title || model.value
                            font.pixelSize: 14
                            color: "#333333"
                            Layout.fillWidth: true
                            elide: Text.ElideRight
                        }
                    }
                    
                    MouseArea {
                        id: mouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        
                        onClicked: {
                            // 选中当前目录
                            directorySelectDialog.selectedDirectory = model.fullPath
                            
                            // 切换展开/折叠状态（如果有子目录）
                            if (model.hasChildren) {
                                if (!model.expanded) {
                                    expandChildren(model.index, model.rawChildren)  // 使用原始子数据
                                } else {
                                    collapseChildren(model.index)
                                }
                            }
                        }
                    }
                }
            }
        }
        
        // 当前选择的目录
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 40
            color: "#F5F5F5"
            border.color: "#E0E0E0"
            border.width: 1
            radius: 4
            
            Text {
                anchors.fill: parent
                anchors.margins: 8
                text: "选择目录: " + (selectedDirectory || "未选择")
                font.pixelSize: 12
                color: "#666666"
                verticalAlignment: Text.AlignVCenter
            }
        }
        
        // 按钮区域
        RowLayout {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignRight
            spacing: 8
            
            Button {
                text: "取消"
                Layout.preferredWidth: 80
                Layout.preferredHeight: 32
                onClicked: {
                    dialogCancelled()
                    close()
                }
            }
            
            Button {
                text: "确定"
                Layout.preferredWidth: 80
                Layout.preferredHeight: 32
                enabled: selectedDirectory !== ""
                onClicked: {
                    if (selectedDirectory) {
                        directorySelected(selectedDirectory)
                        close()
                    }
                }
            }
        }
    }
    
    // 更新目录树数据
    function updateDirectoryTree(treeData) {
        directoryModel.clear()
        if (typeof treeData === 'string') {
            try {
                treeData = JSON.parse(treeData)
            } catch (e) {
                console.error("JSON解析失败:", e)
                return
            }
        }
        if (Array.isArray(treeData)) {
            processDirectoryTree(treeData, 0, "")
        }
    }
    
    // 处理目录树数据（核心修复：保留原始子节点数据）
    function processDirectoryTree(nodes, level, parentPath) {
        if (!Array.isArray(nodes)) return
        
        nodes.forEach((node, index) => {
            if (typeof node !== 'object') return
            
            const nodeValue = node.value || node.title || ""
            const nodeTitle = node.title || nodeValue
            const fullPath = parentPath ? `${parentPath}/${nodeValue}` : nodeValue
            const hasChildren = Array.isArray(node.children) && node.children.length > 0
            
            directoryModel.append({
                value: nodeValue,
                title: nodeTitle,
                level: level,
                fullPath: fullPath,
                hasChildren: hasChildren,
                expanded: false,
                rawChildren: node.children || [],  // 存储原始子节点数据（关键修复）
                index: directoryModel.count  // 动态计算索引
            })
        })
    }
    
    // 展开子目录（使用原始子数据）
    function expandChildren(parentIndex, children) {
        if (!children || !children.length) return
        
        const parentItem = directoryModel.get(parentIndex)
        parentItem.expanded = true
        directoryModel.set(parentIndex, parentItem)
        
        let insertIndex = parentIndex + 1
        // 基于原始子数据生成子节点（关键修复）
        children.forEach(child => {
            const childValue = child.value || child.title || ""
            const childTitle = child.title || childValue
            const fullPath = `${parentItem.fullPath}/${childValue}`
            const hasChildren = Array.isArray(child.children) && child.children.length > 0
            
            directoryModel.insert(insertIndex, {
                value: childValue,
                title: childTitle,
                level: parentItem.level + 1,
                fullPath: fullPath,
                hasChildren: hasChildren,
                expanded: false,
                rawChildren: child.children || [],  // 传递原始子数据
                index: insertIndex
            })
            insertIndex++
        })
        
        updateIndices(parentIndex + 1)
    }
    
    // 折叠子目录
    function collapseChildren(parentIndex) {
        const parentItem = directoryModel.get(parentIndex)
        parentItem.expanded = false
        directoryModel.set(parentIndex, parentItem)
        
        const parentLevel = parentItem.level
        let i = parentIndex + 1
        
        while (i < directoryModel.count) {
            const item = directoryModel.get(i)
            if (item.level <= parentLevel) break
            directoryModel.remove(i)
        }
        
        updateIndices(parentIndex + 1)
    }
    
    // 更新索引（确保索引连续）
    function updateIndices(startIndex) {
        for (let i = startIndex; i < directoryModel.count; i++) {
            const item = directoryModel.get(i)
            item.index = i
            directoryModel.set(i, item)
        }
    }
    
    Component.onCompleted: {
        if (directoryTree.length) updateDirectoryTree(directoryTree)
    }
    
    onDirectoryTreeChanged: {
        if (directoryTree.length) updateDirectoryTree(directoryTree)
    }
}