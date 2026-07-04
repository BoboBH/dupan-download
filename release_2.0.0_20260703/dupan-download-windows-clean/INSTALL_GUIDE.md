# 百度网盘下载工具 - 安装指南

## 快速开始

### 1. 系统要求

- **操作系统：** Windows 10/11 (64位)
- **内存：** 至少 2 GB RAM
- **磁盘空间：** 至少 100 MB 可用空间
- **网络：** 需要互联网连接（用于百度网盘和SFTP）

### 2. 安装步骤

#### 方法一：直接使用（推荐）

1. **将整个文件夹复制到目标位置**
   ```
   复制位置：C:\Program Files\dupan-download\
   或：D:\tools\dupan-download\
   ```

2. **配置环境变量（可选）**
   - 右键点击"此电脑" → "属性" → "高级系统设置"
   - 点击"环境变量"
   - 在"系统变量"中找到"Path"，点击"编辑"
   - 添加程序路径，例如：`C:\Program Files\dupan-download`
   - 点击"确定"保存

3. **验证安装**
   ```cmd
   pan-download.exe --version
   pan-download.exe --help
   ```

#### 方法二：使用安装脚本

1. **以管理员身份运行**
   ```cmd
   右键点击 install.bat → 以管理员身份运行
   ```

2. **按照提示完成安装**

### 3. 配置

#### 3.1 创建配置文件

```cmd
# 复制配置模板
copy .env.example .env

# 编辑配置文件
notepad .env
```

#### 3.2 配置百度网盘

**方法一：使用向导（推荐）**
```cmd
pan-download.exe --setup-bypy
```

**方法二：手动配置**
```cmd
# 在有 Python 的机器上
pip install bypy
bypy info
# 按提示完成认证

# 复制认证文件到目标机器
# 从：C:\Users\<用户名>\.bypy\
# 到：目标机器的相同位置
```

**方法三：环境变量配置**
编辑 `.env` 文件，添加：
```env
BAIDU_BDUSS=你的BDUSS
BAIDU_COOKIES=你的Cookie信息
```

#### 3.3 配置 SFTP（可选）

如果需要自动上传到SFTP服务器，编辑 `.env` 文件：

```env
# SFTP服务器配置
SFTP_HOST=your.server.com
SFTP_PORT=22
SFTP_USERNAME=your_username
SFTP_PASSWORD=your_password
SFTP_REMOTE_PATH=/remote/path

# 或使用SSH密钥
SFTP_KEY_FILE=C:\path\to\private.key
SFTP_PASSPHRASE=your_passphrase
```

### 4. 使用示例

#### 4.1 基本下载

```cmd
# 下载到临时目录（程序退出后自动删除）
pan-download.exe apps/bypy/my_folder

# 下载到临时目录并保留文件
pan-download.exe apps/bypy/my_folder --keep-temp

# 下载到指定目录
pan-download.exe apps/bypy/my_folder --local-dir "D:\MyDownloads"
```

#### 4.2 下载并上传到SFTP

```cmd
# 下载后自动上传到SFTP服务器
pan-download.exe apps/bypy/my_folder --upload-sftp

# 下载到指定目录并上传
pan-download.exe apps/bypy/my_folder --local-dir "D:\MyDownloads" --upload-sftp
```

#### 4.3 高级选项

```cmd
# 详细输出模式
pan-download.exe apps/bypy/my_folder --verbose

# 指定临时目录并保留
pan-download.exe apps/bypy/my_folder --keep-temp --temp-dir "C:\TempDownloads"

# 测试配置
pan-download.exe --test-config
```

### 5. 故障排除

#### 5.1 程序无法启动

**症状：** 双击程序无反应或闪退

**解决方案：**
1. 检查是否是 64 位 Windows
2. 以管理员身份运行
3. 检查杀毒软件是否阻止
4. 在命令提示符中运行以查看错误信息：
   ```cmd
   pan-download.exe --help
   ```

#### 5.2 百度网盘认证失败

**症状：** 提示认证失败或无法连接

**解决方案：**
```cmd
# 1. 重新运行认证向导
pan-download.exe --setup-bypy

# 2. 检查认证文件
dir %USERPROFILE%\.bypy

# 3. 手动测试（需要在有 Python 的机器上）
pip install bypy
bypy quota
```

#### 5.3 SFTP 连接失败

**症状：** 提示 SFTP 连接失败

**解决方案：**
1. 检查 `.env` 文件中的 SFTP 配置
2. 测试网络连接：
   ```cmd
   ping your.server.com
   telnet your.server.com 22
   ```
3. 验证用户名和密码
4. 如果使用 SSH 密钥，检查密钥文件路径

#### 5.4 下载失败

**症状：** 下载过程中出错

**解决方案：**
```cmd
# 1. 使用详细模式查看详细信息
pan-download.exe apps/bypy/my_folder --verbose

# 2. 检查百度网盘路径是否正确
# （不要包含 'apps/bypy/' 前缀）
pan-download.exe my_folder --verbose

# 3. 测试配置
pan-download.exe --test-config
```

### 6. 卸载

#### 方法一：手动删除

1. **删除程序文件夹**
2. **删除配置文件**
   ```cmd
   del %USERPROFILE%\.bypy
   del <程序目录>\.env
   ```
3. **从 PATH 中移除**（如果添加过）

#### 方法二：使用卸载脚本

```cmd
uninstall.bat
```

### 7. 高级配置

#### 7.1 配置文件位置

- **配置文件：** `<程序目录>\.env`
- **认证文件：** `%USERPROFILE%\.bypy\`
- **日志文件：** 临时文件位置

#### 7.2 环境变量

可以通过环境变量覆盖配置：

```cmd
set SFTP_HOST=alternate.server.com
pan-download.exe apps/bypy/test --upload-sftp
```

#### 7.3 批处理脚本

创建批处理脚本简化常用操作：

```batch
@echo off
REM download_and_upload.bat
pan-download.exe apps/bypy/work_files --upload-sftp --keep-temp --temp-dir "D:\WorkDownloads"
```

### 8. 安全建议

1. **保护敏感信息**
   - 不要共享包含认证信息的 `.env` 文件
   - 定期更换密码
   - 使用 SSH 密钥而非密码

2. **网络安全**
   - 在受信任的网络中使用
   - 使用 SFTP 而非 FTP
   - 验证服务器 SSL 证书

3. **文件安全**
   - 定期清理临时文件
   - 验证下载文件的完整性

### 9. 性能优化

#### 9.1 大文件下载

```cmd
# 使用临时目录保留文件
pan-download.exe apps/bypy/large_folder --keep-temp --temp-dir "D:\FastDrive"
```

#### 9.2 批量下载

创建批处理脚本：
```batch
@echo off
for %%f in (folder1 folder2 folder3) do (
    pan-download.exe apps/bypy/%%f --upload-sftp
)
```

### 10. 更新和升级

#### 检查版本

```cmd
pan-download.exe --version
```

#### 升级

1. 下载新版本
2. 备份配置文件：
   ```cmd
   copy .env .env.backup
   ```
3. 替换程序文件
4. 恢复配置文件：
   ```cmd
   copy .env.backup .env
   ```
5. 测试新版本：
   ```cmd
   pan-download.exe --test-config
   ```

### 11. 支持和帮助

#### 获取帮助

```cmd
# 显示帮助信息
pan-download.exe --help

# 测试配置
pan-download.exe --test-config

# 详细日志
pan-download.exe <命令> --verbose
```

#### 常用命令参考

| 命令 | 说明 |
|-----|------|
| `--help` | 显示帮助信息 |
| `--version` | 显示版本信息 |
| `--setup-bypy` | 启动百度网盘认证向导 |
| `--test-config` | 测试配置是否正确 |
| `--verbose` | 详细输出模式 |
| `--keep-temp` | 保留临时文件 |
| `--upload-sftp` | 上传到SFTP服务器 |
| `--local-dir PATH` | 指定本地目录 |
| `--temp-dir PATH` | 指定临时目录 |

### 12. 许可和免责

本工具仅供学习和个人使用。请遵守百度网盘和目标服务器的使用条款。

---

**文档版本：** 2.0.0
**最后更新：** 2026-07-03
**程序版本：** 2.0.0
