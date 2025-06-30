# NAS 文件管理系统 - 页面功能说明

## 概述

本项目实现了4个不同的文件类型界面，每个界面都有独立的QML文件，便于后期维护和扩展。

## 页面结构

### 1. 视频界面 (VideoPage.qml)
- **位置**: `nas_qt/ui/pages/VideoPage.qml`
- **功能**: 显示视频文件缩略图网格布局
- **特点**:
  - 使用 `thumbnailVM.requestThumbnail()` 获取视频缩略图
  - 网格布局显示，每个视频项包含缩略图和文件名
  - 支持点击和双击操作
  - 默认显示视频图标 (🎬)
  - 包含刷新按钮

### 2. 图片界面 (PhotoPage.qml)
- **位置**: `nas_qt/ui/pages/PhotoPage.qml`
- **功能**: 显示图片文件缩略图网格布局
- **特点**:
  - 使用 `thumbnailVM.requestThumbnail()` 获取图片缩略图
  - 正方形网格布局，适合图片预览
  - 悬停时显示文件名
  - 默认显示图片图标 (🖼️)
  - 支持点击查看大图

### 3. 文档界面 (DocumentPage.qml)
- **位置**: `nas_qt/ui/pages/DocumentPage.qml`
- **功能**: 采用文件列表方式显示文档
- **特点**:
  - 列表布局，显示文件名、大小、修改时间
  - 根据文件类型显示不同图标 (📕📘📗📙📄)
  - 包含"打开"和"下载"操作按钮
  - 支持双击打开文档

### 4. 音频界面 (AudioPage.qml)
- **位置**: `nas_qt/ui/pages/AudioPage.qml`
- **功能**: 采用文件列表方式显示音频文件
- **特点**:
  - 列表布局，显示文件名、大小、时长、修改时间
  - 音频格式识别和显示
  - 基于文件大小估算音频时长
  - 包含"播放"和"下载"操作按钮
  - 圆形音频图标 (🎵)

## 导航机制

### 导航栏修改 (NavigationBar.qml)
- 添加了 `pageTypeChanged(int pageType)` 信号
- 修改按钮点击逻辑，根据按钮类型切换页面
- 标题点击跳转到主页功能

### 主页面修改 (MainPage.qml)
- 添加了 `currentPageType` 属性来跟踪当前页面类型
- 实现了 `switchPageType()` 函数来切换页面
- 根据页面类型动态加载不同的QML组件
- 工具栏只在文件列表页面显示

## 页面类型映射

| 按钮 | 页面类型 | 页面文件 | 数据源 |
|------|----------|----------|--------|
| 默认 | 0 (文件列表) | FileListArea.qml | fileVM |
| 视频 | 1 | VideoPage.qml | typefilesVM.fetchTypeFiles("video") |
| 图片 | 2 | PhotoPage.qml | typefilesVM.fetchTypeFiles("photo") |
| 文档 | 3 | DocumentPage.qml | typefilesVM.fetchTypeFiles("document") |
| 音频 | 4 | AudioPage.qml | typefilesVM.fetchTypeFiles("audio") |

## 缩略图功能

### 视频和图片页面
- 使用 `thumbnailVM.requestThumbnail(filePath, width, height)` 请求缩略图
- 通过 `onThumbnailReady` 和 `onThumbnailFailed` 信号处理结果
- 支持异步加载和缓存
- 失败时显示默认图标

### 缩略图尺寸
- 视频: 200x150 像素
- 图片: 180x180 像素

## 文件操作

### 通用操作
- 双击打开文件
- 下载文件
- 刷新文件列表

### 特定操作
- 视频: 播放视频
- 图片: 查看大图
- 文档: 打开文档
- 音频: 播放音频

## 配置更新

### qmldir 文件
添加了新的页面组件注册：
```
VideoPage 1.0 pages/VideoPage.qml
PhotoPage 1.0 pages/PhotoPage.qml
DocumentPage 1.0 pages/DocumentPage.qml
AudioPage 1.0 pages/AudioPage.qml
```

### main.py
添加了 pages 目录到 QML 导入路径：
```python
pages_path = os.path.join(ui_path, "pages")
engine.addImportPath(pages_path)
```

## 使用说明

1. 启动应用后，默认显示文件列表页面
2. 点击导航栏的"视频"、"图片"、"文档"、"音频"按钮切换对应页面
3. 点击标题"NAS 文件管理系统"可以跳转到主页
4. 每个页面都有独立的刷新按钮
5. 支持文件的双击操作和右键菜单

## 扩展性

- 每个页面都是独立的QML文件，便于单独维护
- 可以轻松添加新的文件类型页面
- 缩略图功能可以扩展到其他文件类型
- 页面切换机制支持动态加载

## 注意事项

- 确保 `thumbnailVM` 和 `typefilesVM` 在应用中正确初始化
- 缩略图功能需要后端支持
- 文件操作功能需要根据实际需求实现
- 主题管理器 `themeManager` 需要在所有页面中可用 