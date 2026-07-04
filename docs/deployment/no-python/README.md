# 无Python环境部署指南

## 🔑 重要说明

**是的，目标机器完全不需要Python和bypy！** 

本程序使用PyInstaller打包，已将所有Python依赖（包括bypy）打包到一个独立的exe文件中。

## 🎯 部署要求

### 目标机器系统要求
- ✅ Windows 7/8/10/11
- ✅ **无需安装Python**
- ✅ **无需安装bypy**
- ✅ 建议管理员权限（用于添加到PATH）

### 目标机器需要的东西
- ✅ `pan-download.exe` 程序文件
- ⚠️  百度网盘认证文件（需手动配置）

## 🚀 快速部署步骤

### 1. 开发机：创建发布包

```bash
create_release.bat
```

这会生成一个包含所有文件的发布包。

### 2. 目标机：安装程序

```bash
# 以管理员身份运行
install.bat
```

### 3. 配置百度网盘认证

**方法一：从开发机复制认证文件（推荐）**

```bash
# 在开发机（已认证）上
# 认证文件位置：
# Windows: %USERPROFILE%\.bypy\
# Linux/Mac: ~/.bypy/

# 复制认证文件到目标机
# 源文件：开发机的认证目录
# 目标位置：目标机的 %USERPROFILE%\.bypy\
```

**方法二：在目标机手动认证（需要临时Python环境）**

如果目标机完全没有Python环境，最简单的方法是：

1. 在一台有Python的机器上完成认证
2. 将认证文件复制到目标机

**方法三：使用环境变量（高级用户）**

编辑 `%USERPROFILE%\dupan-download\.env` 文件：

```env
# 从浏览器开发者工具获取这些信息
BAIDU_BDUSS=your_bduss_value
BAIDU_COOKIES=your_cookies_value
```

### 4. 配置SFTP服务器

编辑 `%USERPROFILE%\dupan-download\.env` 文件：

```env
SFTP_HOST=sftp.example.com
SFTP_PORT=22
SFTP_USERNAME=your_username
SFTP_PASSWORD=your_password
SFTP_REMOTE_PATH=/remote/path
```

### 5. 测试配置

```bash
pan-download --test-config
```

### 6. 开始使用

```bash
pan-download 260701 --upload-sftp
```

## 📁 认证文件详解

### 什么是认证文件？

bypy的认证文件包含：
- `token.json` - OAuth认证令牌
- `cookie.json` - 百度网盘Cookie
- 其他配置文件

### 如何获取认证文件？

**步骤1：在有Python环境的机器上完成认证**

```bash
# 1. 安装bypy
pip install bypy

# 2. 运行认证命令
bypy info

# 3. 按提示在浏览器中完成OAuth认证
# 4. 认证成功后，bypy会自动保存认证文件
```

**步骤2：找到认证文件**

```bash
# Windows
dir %USERPROFILE%\.bypy

# Linux/Mac
ls ~/.bypy
```

**步骤3：复制到目标机器**

```bash
# 目标位置
# Windows: %USERPROFILE%\.bypy\
# Linux/Mac: ~/.bypy/

# 确保目录结构完整，包括：
# - token.json
# - cookie.json
# - 其他生成的文件
```

## 🔧 技术细节

### 打包原理

本程序使用PyInstaller技术，将以下内容打包到一个exe文件中：

1. **Python解释器** - 完整的Python运行时
2. **所有依赖包** - bypy, click, paramiko, requests等
3. **程序代码** - 你的应用程序代码
4. **支持文件** - 配置模板、文档等

### 为什么还需要认证文件？

虽然程序包含bypy模块，但**认证凭据**是用户特定的：
- OAuth令牌与你的百度账号绑定
- Cookie包含你的登录信息
- 这些信息不能预先打包

### 程序如何使用认证文件？

程序运行时会：
1. 检查 `%USERPROFILE%\.bypy\` 目录
2. 读取认证文件（token.json等）
3. 使用这些信息与百度网盘API通信
4. 如果没有认证文件，会提示配置

## 🎯 最佳实践

### 推荐部署流程

1. **开发机认证**
   ```bash
   pip install bypy
   bypy info
   # 完成认证
   ```

2. **打包程序**
   ```bash
   create_release.bat
   ```

3. **收集认证文件**
   ```bash
   # 复制认证文件到临时目录
   xcopy %USERPROFILE%\.bypy release_temp\auth_files\
   ```

4. **部署到目标机**
   ```bash
   # 复制整个发布包
   # 包含：程序 + 认证文件
   ```

5. **目标机安装**
   ```bash
   # 运行安装脚本
   install.bat
   
   # 手动放置认证文件
   # 复制到 %USERPROFILE%\.bypy\
   ```

## ⚡ 快速脚本

### 开发机：准备完整发布包

```bash
# 1. 认证并测试
pip install bypy
bypy info
bypy quota

# 2. 创建发布包
create_release.bat

# 3. 收集认证文件
mkdir release_1.0.0\auth_files
xcopy %USERPROFILE%\.bypy release_1.0.0\auth_files\ /E /I

# 4. 创建说明文件
echo 认证文件位于 auth_files 目录 > release_1.0.0\AUTH_FILES_README.txt
echo 请复制到目标机的 %%USERPROFILE%%\.bypy\ 目录 >> release_1.0.0\AUTH_FILES_README.txt
```

### 目标机：一键安装

```bash
# 1. 解压发布包
# 2. 运行安装
install.bat

# 3. 安装认证文件
mkdir %USERPROFILE%\.bypy
xcopy auth_files\*.* %USERPROFILE%\.bypy\ /E /I

# 4. 测试
pan-download --test-config
```

## 🔍 故障排除

### 问题1：认证文件位置错误

**症状**：程序提示认证失败

**解决**：
```bash
# 确保认证文件在正确位置
# Windows: %USERPROFILE%\.bypy\
# 检查：
dir %USERPROFILE%\.bypy
```

### 问题2：认证文件损坏

**症状**：认证文件存在但无法使用

**解决**：
1. 重新在源机器完成认证
2. 重新复制认证文件
3. 确保文件完整且未损坏

### 问题3：权限问题

**症状**：无法读取认证文件

**解决**：
1. 检查文件权限
2. 确保当前用户有读取权限
3. 尝试以管理员身份运行

## 📋 总结

### ✅ 可以做到的
- 完全不需要Python环境
- 不需要安装bypy
- 单个exe文件包含所有依赖
- 独立运行，无外部依赖

### ⚠️ 需要手动配置的
- 百度网盘认证文件（一次配置）
- SFTP服务器配置（如需上传功能）

### 🎯 推荐方案
**开发机认证 + 打包 → 目标机部署 + 认证文件**

这样可以确保：
- 程序完全独立运行
- 认证配置一次完成
- 部署过程简单快速

---

**现在你有一个完全独立的Windows程序，可以在任何Windows电脑上运行！**