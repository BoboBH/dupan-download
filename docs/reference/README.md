# 参考文档

参考文档提供详细的命令、配置和API参考资料，适合快速查询和深入了解。

## 📚 文档列表

### 快速参考
- **[快速入门](quick-start.md)** - 5分钟快速上手指南
- **[解决方案](solution.md)** - 完整功能说明和技术实现

### 命令参考
- **[命令行参考](commands.md)** - 所有命令和参数详解（待创建）
- **[配置参数参考](config.md)** - 详细配置参数说明（待创建）

### API参考
- API文档（待创建）

## 🎯 快速查找

### 常用命令
```bash
# 下载文件
pan-download <远程路径>

# 下载并上传
pan-download <远程路径> --upload-sftp

# 保留文件
pan-download <远程路径> --keep-temp

# 详细日志
pan-download <远程路径> --verbose

# 测试配置
pan-download --test-config

# 认证向导
pan-download --setup-bypy
```

### 常用参数
| 参数 | 说明 | 示例 |
|------|------|------|
| `--upload-sftp` | 上传到SFTP | `pan-download path --upload-sftp` |
| `--keep-temp` | 保留临时文件 | `pan-download path --keep-temp` |
| `--temp-dir PATH` | 指定临时目录 | `pan-download path --temp-dir "C:\Temp"` |
| `--local-dir PATH` | 指定本地目录 | `pan-download path --local-dir "D:\Files"` |
| `--verbose` | 详细输出 | `pan-download path --verbose` |
| `--setup-bypy` | 认证向导 | `pan-download --setup-bypy` |
| `--test-config` | 测试配置 | `pan-download --test-config` |

### 配置参数
```env
# SFTP服务器配置
SFTP_HOST=192.168.0.122
SFTP_PORT=22
SFTP_USERNAME=username
SFTP_PASSWORD=password
SFTP_REMOTE_PATH=/remote/path

# 性能配置
MAX_RETRIES=3
CONNECT_TIMEOUT=30
TRANSFER_TIMEOUT=300
```

## 📋 完整参考

### 命令完整语法
```bash
pan-download [OPTIONS] REMOTE_FOLDER

选项:
  --local-dir PATH          指定本地下载目录
  --upload-sftp            下载后上传到SFTP
  --keep-temp              保留临时文件
  --temp-dir PATH          指定临时文件位置
  --verbose                详细输出模式
  --setup-bypy            启动认证向导
  --test-config           测试配置
  --help                  显示帮助信息
```

### 环境变量
| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SFTP_HOST` | SFTP服务器地址 | 必需 |
| `SFTP_PORT` | SFTP端口 | 22 |
| `SFTP_USERNAME` | SFTP用户名 | 必需 |
| `SFTP_PASSWORD` | SFTP密码 | 必需 |
| `SFTP_REMOTE_PATH` | 远程基础路径 | 必需 |
| `MAX_RETRIES` | 最大重试次数 | 3 |
| `CONNECT_TIMEOUT` | 连接超时(秒) | 30 |
| `TRANSFER_TIMEOUT` | 传输超时(秒) | 300 |

## 🔍 按功能查找

### 下载相关
- [基本下载](../guides/usage/README.md#基本下载)
- [保留文件](../guides/usage/temp-files.md)

### 上传相关
- [SFTP配置](../guides/config/sftp.md)
- [SFTP功能](../development/features/sftp-upload.md)

### 配置相关
- [配置总览](../guides/config/overview.md)
- [测试配置](../deployment/installation/README.md#测试配置)

## 🔗 相关文档

- **[用户指南](../guides/README.md)** - 详细使用说明
- **[部署指南](../deployment/README.md)** - 安装和配置
- **[文档中心](../README.md)** - 文档导航

---

返回：[文档中心](../README.md) | [项目主页](../../README.md)