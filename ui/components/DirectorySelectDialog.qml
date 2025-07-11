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
    property var directoryTree: []
    property var treeDataCache: []          // 🌟 保留全局树数据
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

                        // 缩进
                        Item {
                            Layout.preferredWidth: model.level * 20
                        }

                        // 展开/折叠图标
                        Text {
                            text: model.hasChildren ? (model.expanded ? "▼" : "▶") : "  "
                            font.pixelSize: 12
                            color: "#666666"
                            Layout.preferredWidth: 20
                            visible: model.hasChildren
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
                            directorySelectDialog.selectedDirectory = model.fullPath

                            if (model.hasChildren) {
                                if (!model.expanded) {
                                    console.log(`展开节点: ${model.title}`)
                                    expandChildren(model.index, model.fullPath)
                                } else {
                                    console.log(`折叠节点: ${model.title}`)
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
                    directorySelectDialog.dialogCancelled()
                    directorySelectDialog.close()
                }
            }

            Button {
                text: "确定"
                Layout.preferredWidth: 80
                Layout.preferredHeight: 32
                enabled: selectedDirectory !== ""
                onClicked: {
                    directorySelectDialog.directorySelected(selectedDirectory)
                    directorySelectDialog.close()
                }
            }
        }
    }

    // 更新目录树数据
    function updateDirectoryTree(treeData) {
        console.log("开始更新目录树数据")

        directoryModel.clear()

        if (typeof treeData === 'string') {
            try {
                treeData = JSON.parse(treeData)
                console.log("成功解析JSON数据")
            } catch (e) {
                console.error("JSON解析失败:", e)
                return
            }
        }

        if (Array.isArray(treeData)) {
            treeDataCache = treeData   // 🌟 缓存全局树数据
            console.log(`根节点数量: ${treeData.length}`)
            processDirectoryTree(treeData, 0, "")
        } else {
            console.error("目录树数据不是数组格式")
        }
    }

    function processDirectoryTree(nodes, level, parentPath) {
        if (!Array.isArray(nodes)) return

        nodes.forEach(node => {
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
                index: directoryModel.count
            })

            console.log(`添加节点: ${nodeTitle}, 路径: ${fullPath}`)
        })
    }

    function expandChildren(parentIndex, fullPath) {
        const parentItem = directoryModel.get(parentIndex)
        parentItem.expanded = true
        directoryModel.set(parentIndex, parentItem)

        const children = findChildrenByPath(treeDataCache, fullPath)

        if (!children || children.length === 0) {
            console.log(`节点 ${parentItem.title} 无子节点`)
            return
        }

        let insertIndex = parentIndex + 1

        children.forEach(child => {
            const childValue = child.value || child.title || ""
            const childTitle = child.title || childValue
            const childFullPath = `${childValue}`
            // const childFullPath = fullPath ? `${fullPath}/${childValue}` : childValue
            const hasChildren = Array.isArray(child.children) && child.children.length > 0

            directoryModel.insert(insertIndex, {
                value: childValue,
                title: childTitle,
                level: parentItem.level + 1,
                fullPath: childFullPath,
                hasChildren: hasChildren,
                expanded: false,
                index: insertIndex
            })

            console.log(`插入子节点: ${childTitle}, 路径: ${childFullPath}`)

            insertIndex += 1
        })

        updateIndices(parentIndex + 1)
    }

    function collapseChildren(parentIndex) {
        const parentItem = directoryModel.get(parentIndex)
        parentItem.expanded = false
        directoryModel.set(parentIndex, parentItem)

        const parentLevel = parentItem.level
        let i = parentIndex + 1

        while (i < directoryModel.count) {
            const item = directoryModel.get(i)
            if (item.level <= parentLevel) break
            console.log(`移除子节点: ${item.title}`)
            directoryModel.remove(i)
        }

        updateIndices(parentIndex + 1)
    }

    function updateIndices(startIndex) {
        for (let i = startIndex; i < directoryModel.count; i++) {
            const item = directoryModel.get(i)
            item.index = i
            directoryModel.set(i, item)
        }
    }

    // 根据路径查找 children
    function findChildrenByPath(nodes, path) {
        if (!path) return nodes

        const parts = path.split("/")
        let current = nodes

        for (let i = 0; i < parts.length; i++) {
            const node = current.find(n => n.value === parts[i])
            if (!node) return []
            current = node.children || []
        }
        return current
    }

    Component.onCompleted: {
        if (directoryTree && directoryTree.length > 0) {
            updateDirectoryTree(directoryTree)
        }
    }

    onDirectoryTreeChanged: {
        if (directoryTree && directoryTree.length > 0) {
            updateDirectoryTree(directoryTree)
        }
    }
}
