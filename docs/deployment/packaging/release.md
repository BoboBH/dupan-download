# 百度网盘下载工具 - 完整打包部署指南

## 🎯 项目概述

本项目是一个百度网盘自动下载和SFTP上传工具，可以将百度网盘文件自动下载并上传到SFTP服务器。已实现完整的打包部署方案，支持在没有Python环境的Windows电脑上运行。

## 🚀 一键发布（推荐）

### 开发机操作

在开发机器上，只需运行一个命令即可创建完整的发布包：

```bash
create_release.bat
```

这个脚本会自动完成以下操作：
1. 打包程序为 `pan-download.exe`
2. 创建安装脚本 `install.bat`
3. 生成所有必要的文档
4. 组织完整的发布包结构

### 目标机器操作

将生成的发布包复制到目标电脑，然后：

```bash
# 以管理员身份运行
install.bat
```

## 📦 发布包内容

```
dupan-download-windows/
├── pan-download.exe          # 主程序（包含所有依赖）
├── install.bat               # 一键安装脚本
├── .env.example             # 配置文件模板
├── README.md                # 项目说明
├── DEPLOYMENT_GUIDE.md      # 完整部署指南
├── QUICK_START.txt          # 快速启动指南
├── VERSION.txt              # 版本信息
├── README_PACKAGE.txt       # 打包说明
└── docs/                    # 详细文档目录
    ├── USAGE_GUIDE.md
    ├── CONFIG_CLEAN.md
    ├── PROJECT_STATUS.md
    ├── build.bat
    └── build.spec
```

## 🔧 手动打包（如需自定义）

### 1. 安装打包依赖

```bash
pip install pyinstaller pywin32 bypy
```

### 2. 执行打包

```bash
# 方法1: 使用打包脚本
build.bat

# 方法2: 手动执行
pyinstaller build.spec --clean
```

### 3. 收集文件

将 `dist` 目录中的文件复制到发布包：
```bash
copy dist\pan-download.exe <发布目录>\
copy .env.example <发布目录>\
copy README.md <发布目录>\
```

## 📋 部署流程

### 步骤1: 复制文件到目标电脑

将整个发布包文件夹复制到目标Windows电脑。

### 步骤2: 运行安装脚本

```bash
# 以管理员身份运行
install.bat
```

安装脚本会：
1. 创建安装目录 `%USERPROFILE%\dupan-download`
2. 复制程序文件
3. 添加到系统PATH
4. 显示配置向导说明

### 步骤3: 配置百度网盘认证

```bash
pan-download --setup-bypy
```

按提示完成百度网盘OAuth认证：
1. 浏览器会打开百度网盘认证页面
2. 登录百度账号并授权
3. 复制授权码并粘贴
4. 完成认证

### 步骤4: 配置SFTP服务器

编辑 `%USERPROFILE%\dupan-download\.env` 文件：

```env
# SFTP服务器配置
SFTP_HOST=your.server.com
SFTP_PORT=22
SFTP_USERNAME=your_username
SFTP_PASSWORD=your_password
SFTP_REMOTE_PATH=/remote/path

# 百度网盘配置（可选）
BAIDU_BDUSS=your_bduss
BAIDU_COOKIES=your_cookies
```

### 步骤5: 测试配置

```bash
pan-download --test-config
```

确认所有配置正确。

### 步骤6: 开始使用

```bash
# 下载文件
pan-download 260701

# 下载并上传到SFTP
pan-download 260701 --upload-sftp

# 详细日志
pan-download 260701 --verbose
```

## 🛠️ 新增功能

### 1. 内置认证向导

`pan-download --setup-bypy` 命令提供交互式认证向导：
- 自动检查bypy安装状态
- 引导完成OAuth认证流程
- 验证认证结果

### 2. 配置测试功能

`pan-download --test-config` 命令可以：
- 测试百度网盘认证状态
- 测试SFTP连接配置
- 显示详细的配置问题诊断

### 3. 用户友好的命令界面

改进的命令行界面：
- 清晰的步骤说明
- 友好的错误提示
- 详细的执行日志

## 📚 文档说明

### 核心文档

- **DEPLOYMENT_GUIDE.md** - 完整的部署指南，包含详细步骤和故障排除
- **QUICK_START.txt** - 快速启动指南，帮助你快速上手
- **README.md** - 项目说明和功能介绍

### 配置文档

- **docs/CONFIG_CLEAN.md** - 详细的配置参数说明
- **docs/USAGE_GUIDE.md** - 使用方法和示例
- **docs/PROJECT_STATUS.md** - 项目开发状态

### 技术文档

- **docs/build.bat** - 打包脚本
- **docs/build.spec** - PyInstaller配置文件

## 🔍 故障排除

### 常见问题

#### 1. bypy认证失败

**问题**: `pan-download --setup-bypy` 认证失败

**解决方法**:
1. 确保网络连接正常
2. 检查是否有代理设置影响
3. 手动运行 `bypy info` 进行认证

#### 2. SFTP连接失败

**问题**: `--test-config` 显示SFTP连接失败

**解决方法**:
1. 检查 `.env` 文件配置
2. 确认服务器地址、端口正确
3. 验证用户名和密码
4. 检查网络连接和防火墙

#### 3. PATH设置失败

**问题**: 无法直接运行 `pan-download` 命令

**解决方法**:
1. 使用管理员权限运行安装脚本
2. 手动添加目录到PATH
3. 使用完整路径运行程序

#### 4. 程序无法启动

**问题**: 双击exe文件没有反应

**解决方法**:
1. 检查杀毒软件是否拦截
2. 使用管理员权限运行
3. 查看Windows事件日志
4. 在命令行中运行查看错误信息

## 🎨 自定义配置

### 修改安装位置

编辑 `install.bat` 中的：
```bat
set INSTALL_DIR=%USERPROFILE%\dupan-download
```

### 修改打包选项

编辑 `build.spec` 文件可以修改：
- 程序图标
- 打包模式
- 包含的文件

## 📋 版本信息

- **当前版本**: 1.0.0
- **Python版本**: 3.8+
- **bypy版本**: 1.8.9+
- **支持平台**: Windows 7/8/10/11

## 🔒 安全注意事项

1. **保护配置文件**: `.env` 文件包含敏感信息，请妥善保管
2. **使用强密码**: SFTP密码应使用强密码
3. **定期更新**: 及时更新程序以获取安全修复
4. **权限控制**: 建议限制程序的访问权限

## 📞 技术支持

如遇到问题，请按以下顺序查找解决方案：

1. 查看 `DEPLOYMENT_GUIDE.md` 中的"常见问题"章节
2. 查看 `docs/USAGE_GUIDE.md` 中的详细使用说明
3. 查看 `docs/CONFIG_CLEAN.md` 中的配置说明
4. 运行 `pan-download --test-config` 诊断配置问题

## 🎉 快速开始总结

```bash
# 开发机：创建发布包
create_release.bat

# 目标机：安装和配置
install.bat
pan-download --setup-bypy
# 编辑 .env 文件
pan-download --test-config

# 开始使用
pan-download 260701 --upload-sftp
```

---

**制作完成！** 现在你有了一个完整的打包部署方案，可以轻松地将项目部署到任何Windows电脑上。