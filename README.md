# NAS 文件管理系统

一个基于 PySide6 和 QML 开发的现代化 NAS 文件管理客户端应用。

## 📋 项目简介

这是一个使用 Python 和 Qt 技术栈开发的 NAS 文件管理系统客户端。应用采用 MVVM 架构模式，提供了直观的用户界面和强大的文件管理功能。

## ✨ 主要功能

### 🔐 用户认证

- 用户登录验证
- JWT Token 认证
- 安全的密码管理

### 📁 文件管理

- 浏览文件和文件夹
- 文件列表显示
- 文件选择操作
- 目录导航
- 文件信息展示（大小、修改时间等）
- 空文件夹友好提示（显示"No data"）

### 🖱️ 鼠标操作

- **左键单击**: 选中文件/文件夹
- **左键双击**: 打开文件或进入文件夹
- **右键菜单**: 提供文件操作选项（打开、复制、删除、重命名、属性等）

### 🎨 用户界面

- 现代化的 Material Design 风格
- 响应式布局设计
- 主题管理支持
- 直观的操作界面

## 🏗️ 技术架构

### 前端技术栈

- **PySide6**: Python Qt 绑定
- **QML**: 声明式用户界面语言
- **Qt Quick Controls**: 现代化 UI 组件

### 后端技术栈

- **Python**: 主要开发语言
- **RESTful API**: 与 NAS 服务器通信
- **JWT**: 用户认证

### 架构模式

- **MVVM (Model-View-ViewModel)**: 分离业务逻辑和用户界面
- **组件化设计**: 模块化的代码结构

## 📁 项目结构

```python
nas_qt/
├── main.py                          # 应用程序入口
├── config.py                        # 配置文件
├── .env                             # 环境变量配置
├── viewmodels/                      # ViewModel 层
│   ├── login_vm.py                 # 登录视图模型
│   ├── file_vm.py                  # 文件管理视图模型
│   └── theme_manager.py            # 主题管理
├── api/                            # API 接口层
│   ├── login_api.py               # 登录 API
│   └── file_api.py                # 文件操作 API
├── ui/                             # 用户界面
│   ├── MainWindow.qml             # 主窗口
│   ├── Login.qml                  # 登录页面
│   ├── MainPage.qml               # 主页面
│   ├── qmldir                     # QML 模块定义
│   └── components/                # 可复用组件
└── nas-server-api-login-filemanager.yaml  # API 文档
```

## 🚀 安装和运行

### 环境要求

- Python 3.8+
- PySide6
- 网络连接（用于连接 NAS 服务器）

### 安装步骤

1. **克隆项目**

   ```bash
   git clone <repository-url>
   cd nas_qt
   ```

2. **安装依赖**

   ```bash
   pip install PySide6
   ```

3. **配置环境**

   ```bash
   # 编辑 .env 文件，设置文件存储路径
   echo "FILE_BASE_PATH=/path/to/your/storage" > .env
   echo "API_BASE_URL=http://your-server:8080" >> .env
   ```

4. **运行应用**

   ```bash
   python3 main.py
   ```

## 📖 使用说明

### 登录

1. 启动应用后，首先显示登录界面
2. 输入用户名和密码
3. 点击登录按钮进行身份验证

### 文件管理

1. 登录成功后自动进入文件管理界面
2. 浏览当前目录下的文件和文件夹
3. 点击文件夹进入子目录
4. 选择文件进行批量操作

### 鼠标操作

1. **左键单击**: 点击文件或文件夹进行选中
2. **左键双击**: 
   - 双击文件夹：进入该文件夹
   - 双击文件：使用系统默认程序打开文件
3. **右键菜单**: 右键点击文件或文件夹显示操作菜单
   - 打开：打开文件或进入文件夹
   - 复制：复制文件（待实现）
   - 删除：删除文件（待实现）
   - 重命名：重命名文件（待实现）
   - 属性：查看文件属性（待实现）

## 🔧 配置说明

### 环境变量配置 (.env)

创建 `.env` 文件来配置应用程序：

```bash
# 文件存储的基础路径
FILE_BASE_PATH=/home/lanyang/nasserver/FileManager/storage

# API服务器地址
API_BASE_URL=http://127.0.0.1:8080
```

### 配置项说明

- **FILE_BASE_PATH**: NAS服务器上文件存储的根目录路径
- **API_BASE_URL**: NAS服务器API的访问地址

### 配置优先级

配置加载优先级（从高到低）：
1. 环境变量（`FILE_BASE_PATH`, `API_BASE_URL`）
2. `.env` 文件
3. 默认配置

### API 服务器配置
应用默认连接到 `http://127.0.0.1:8080`，可通过 `.env` 文件或环境变量修改。

### 主题配置
应用支持主题切换功能，可通过 `ThemeManager` 进行配置。

## 🛠️ 开发指南

### 添加新功能

1. 在 `viewmodels/` 目录下创建新的 ViewModel
2. 在 `api/` 目录下添加相应的 API 接口
3. 在 `ui/` 目录下创建 QML 界面文件
4. 在 `main.py` 中注册新的 ViewModel

### 代码规范

- 使用 Python 类型注解
- 遵循 PEP 8 代码风格
- QML 文件使用 2 空格缩进
- 添加适当的注释和文档字符串

## 📄 API 文档

详细的 API 文档请参考 `nas-server-api-login-filemanager.yaml` 文件，其中包含了所有可用的接口说明。

### 主要接口

- `POST /api/login`: 用户登录
- `GET /api/files`: 获取文件列表
- `POST /api/chpwd`: 修改用户密码（管理员专用）

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request 来改进这个项目。

### 提交规范

- 使用清晰的提交信息
- 确保代码通过测试
- 更新相关文档

## 📝 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 GitHub Issue
- 发送邮件至项目维护者

---

**注意**: 使用前请确保 NAS 服务器正在运行且网络连接正常。
