# 百度网盘自动下载SFTP上传工具 v2.1.5

## 🎯 功能简介

这是一个强大的命令行工具，用于自动从百度网盘下载文件夹并上传到SFTP服务器。

### ✨ 主要功能

- ✅ **自动下载**: 从百度网盘自动下载文件夹及子文件夹
- ✅ **目录结构保持**: 完整保持原始目录结构
- ✅ **SFTP上传**: 自动上传到指定SFTP服务器
- ✅ **错误处理**: 智能错误处理和重试机制
- ✅ **流式处理**: 下载一个文件后立即上传，节省磁盘空间
- ✅ **详细报告**: 提供成功/失败文件的详细报告
- ✅ **进度显示**: 实时显示下载和上传进度
- ✅ **无依赖部署**: 打包为独立exe，无需Python环境

## 📦 文件说明

- `pan-download.exe` - 主程序（双击运行或命令行调用）
- `.env.example` - 配置文件模板
- `使用说明.txt` - 详细使用说明
- `README.md` - 本文件
- `版本说明.txt` - 版本更新记录

## 🚀 快速开始

### 1. 配置设置

复制配置文件模板：
```bash
copy .env.example .env
```

编辑 `.env` 文件，填入实际的配置信息：
```bash
# SFTP服务器配置（如需上传功能）
SFTP_HOST=sftp.example.com
SFTP_PORT=22
SFTP_USERNAME=your_username
SFTP_PASSWORD=your_password
SFTP_REMOTE_PATH=/remote/path

# 重试和超时配置（可选）
MAX_RETRIES=3
CONNECT_TIMEOUT=30
TRANSFER_TIMEOUT=300
```

### 2. 百度网盘认证

本工具使用 **bypy** 库进行百度网盘下载，采用 OAuth 认证方式：

```bash
# 运行认证向导
pan-download.exe --setup-bypy

# 或直接使用bypy命令（需要在有Python环境的电脑上）
bypy info
```

认证信息会自动保存在 `~/.bypi/` 目录中，无需在 `.env` 文件中配置。

**认证配置说明：**
由于本程序是打包版本，bypi认证文件需要手动配置。最简单的方法是在一台有Python环境的电脑上完成认证，然后将认证文件复制到目标机器。

### 3. 使用方法

#### 基本用法

```bash
# 传统模式：直接指定百度网盘路径
pan-download.exe apps/bypi/test_pdf
pan-download.exe apps/bypi/test_pdf --upload-sftp

# 转存模式：分享链接 + 提取码（推荐）
pan-download.exe https://pan.baidu.com/s/1Fi2LAxr441x57Kk4B6ws2Q 0409 --upload-sftp --streaming
```

#### 流式处理模式

```bash
# 流式处理：下载一个文件后立即上传
pan-download.exe apps/bypi/260701 --upload-sftp --streaming
```

流式处理优势：
- 下载一个文件后立即上传
- 自动跳过已存在的文件
- 自动创建SFTP子目录
- 节省磁盘空间

#### 其他选项

```bash
# 保留临时文件用于调试
pan-download.exe apps/bypi/260701 --keep-temp

# 指定临时目录
pan-download.exe apps/bypi/260701 --temp-dir "D:/temp"

# 详细输出模式
pan-download.exe apps/bypi/260701 --verbose
```

## 🔧 命令选项

| 选项 | 说明 |
|------|------|
| `--upload-sftp` | 下载后自动上传到SFTP服务器 |
| `--keep-temp` | 保留临时文件，不自动清理 |
| `--temp-dir PATH` | 指定临时文件存储位置 |
| `--streaming` | 启用流式处理模式 |
| `--verbose` | 启用详细输出模式 |
| `--setup-bypi` | 启动bypi认证向导 |
| `--test-config` | 测试配置是否正确 |
| `--help` | 显示帮助信息 |

## 📋 配置测试

使用前可以测试配置是否正确：

```bash
pan-download.exe --test-config
```

这将测试：
- bypi认证状态
- SFTP连接配置

## ⚠️ 注意事项

1. **认证配置**: 确保bypi认证文件正确配置
2. **网络连接**: 需要稳定的网络连接
3. **磁盘空间**: 流式处理模式下磁盘空间需求较小
4. **SFTP权限**: 确保SFTP用户有足够权限
5. **路径长度**: 工具自动处理长文件名问题

## 🔍 故障排除

### 配置相关
- **问题**: 提示"缺少必需的配置"
- **解决**: 检查 `.env` 文件是否存在且包含所有必需的配置项

### 网络相关
- **问题**: 连接超时
- **解决**: 增加 `CONNECT_TIMEOUT` 和 `TRANSFER_TIMEOUT` 值

### 权限相关
- **问题**: 文件上传失败
- **解决**: 验证SFTP用户权限，检查目标目录是否存在

## 📞 技术支持

如有问题，请查看：
- 详细使用说明：`使用说明.txt`
- 版本更新记录：`版本说明.txt`
- 项目GitHub页面

## 📜 版本信息

- **当前版本**: v2.1.5
- **发布日期**: 2024-07-10
- **Python版本**: 3.12.10
- **打包工具**: PyInstaller 6.21.0

## ⚖️ 许可证

MIT License

---

**享受自动化的文件传输体验！** 🚀