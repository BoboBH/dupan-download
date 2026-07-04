# 百度网盘下载工具 - 打包部署指南

## 快速开始

### 开发机打包

在开发机器上执行以下步骤:

```bash
# 1. 安装打包依赖
pip install pyinstaller pywin32

# 2. 执行打包脚本
build.bat

# 打包完成后，可执行文件位于: dist\pan-download.exe
```

### 目标机器部署

将 `dist` 目录中的所有文件复制到目标Windows电脑，然后运行:

```bash
deploy_setup.bat
```

## 详细说明

### 1. 开发机打包步骤

#### 1.1 环境准备

确保开发机已安装:
- Python 3.8+
- 项目依赖包

```bash
# 安装项目依赖
pip install -r requirements.txt
```

#### 1.2 打包配置

项目使用PyInstaller进行打包，配置文件为 `build.spec`。

打包包含的文件:
- `pan-download.exe` (主程序)
- `.env.example` (配置模板)
- `README.md` (说明文档)

#### 1.3 执行打包

```bash
# Windows
build.bat

# 或手动执行
pyinstaller build.spec --clean
```

#### 1.4 打包输出

打包完成后，`dist` 目录包含:
```
dist/
├── pan-download.exe          # 主程序
├── .env.example              # 配置模板
└── README.md                 # 说明文档
```

### 2. 目标机器部署步骤

#### 2.1 系统要求

- Windows 7/8/10/11
- 无需安装Python（已打包为exe）
- 需要管理员权限（推荐）

#### 2.2 部署文件

将 `dist` 目录复制到目标机器，执行:

```bash
deploy_setup.bat
```

安装脚本会:
1. 创建安装目录 `%USERPROFILE%\dupan-download`
2. 复制程序文件
3. 添加到系统PATH
4. 启动配置向导

#### 2.3 配置向导

安装完成后，需要完成以下配置:

##### A. 百度网盘认证

```bash
pan-download --setup-bypy
```

认证步骤:
1. 在浏览器中打开百度网盘OAuth认证页面
2. 登录百度账号并授权
3. 复制授权码
4. 粘贴授权码完成认证

##### B. SFTP服务器配置

编辑 `.env` 文件:

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

##### C. 测试配置

```bash
pan-download --test-config
```

### 3. 使用方法

#### 3.1 基本下载

```bash
# 下载到默认临时目录
pan-download 260701

# 下载到指定目录
pan-download 260701 --local-dir "D:\我的文件"

# 保留临时文件
pan-download 260701 --keep-temp
```

#### 3.2 下载并上传到SFTP

```bash
pan-download 260701 --upload-sftp
```

#### 3.3 详细日志

```bash
pan-download 260701 --verbose
```

### 4. 常见问题

#### 4.1 bypy认证失败

**问题**: `pan-download --setup-bypy` 认证失败

**解决方法**:
1. 确保网络连接正常
2. 手动运行 `bypy info` 进行认证
3. 检查代理设置

#### 4.2 SFTP连接失败

**问题**: `--test-config` 显示SFTP连接失败

**解决方法**:
1. 检查 `.env` 文件中的SFTP配置
2. 确认服务器地址、端口、用户名密码正确
3. 检查网络连接和防火墙设置

#### 4.3 下载失败

**问题**: 下载时出现错误

**解决方法**:
1. 使用 `--verbose` 参数查看详细日志
2. 检查百度网盘路径是否正确
3. 确认bypy认证状态

#### 4.4 PATH设置失败

**问题**: 无法直接运行 `pan-download` 命令

**解决方法**:
1. 使用管理员权限运行 `deploy_setup.bat`
2. 或手动添加 `%USERPROFILE%\dupan-download` 到PATH
3. 或使用完整路径: `%USERPROFILE%\dupan-download\pan-download.exe`

### 5. 卸载

```bash
# 1. 删除安装目录
rmdir /s "%USERPROFILE%\dupan-download"

# 2. 从PATH中移除（需要管理员权限）
# 手动编辑系统环境变量
```

### 6. 更新

```bash
# 1. 停止正在运行的程序
# 2. 替换 pan-download.exe
# 3. 重新运行配置测试
pan-download --test-config
```

## 高级配置

### 自定义安装位置

编辑 `deploy_setup.bat`，修改:
```bat
set INSTALL_DIR=%USERPROFILE%\dupan-download
```

### 打包选项

编辑 `build.spec` 文件，可以修改:
- 程序图标
- 打包模式
- 包含的文件
- 隐藏导入

## 安全注意事项

1. **保护敏感信息**: `.env` 文件包含密码等敏感信息，请妥善保管
2. **传输安全**: 建议使用SFTP密钥认证而非密码
3. **权限控制**: 建议限制程序的访问权限

## 技术支持

如遇到问题，请查看:
1. 项目文档: `README.md`
2. 使用指南: `USAGE_GUIDE.md`
3. 配置说明: `CONFIG_CLEAN.md`
4. 项目状态: `PROJECT_STATUS.md`

## 版本信息

- 当前版本: 1.0.0
- 最后更新: 2025-07-02
- Python版本: 3.8+
- bypy版本: 1.8.9+