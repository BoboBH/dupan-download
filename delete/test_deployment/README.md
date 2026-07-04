# 百度网盘自动下载SFTP上传工具

一个强大的命令行工具，用于自动从百度网盘下载文件夹并保持目录结构上传到SFTP服务器。

## 功能特性

- ✅ **自动下载**: 从百度网盘自动下载文件夹及子文件夹
- ✅ **目录结构保持**: 完整保持原始目录结构
- ✅ **SFTP上传**: 自动上传到指定SFTP服务器
- ✅ **错误处理**: 智能错误处理和重试机制
- ✅ **详细报告**: 提供成功/失败文件的详细报告
- ✅ **灵活配置**: 支持环境变量和配置文件
- ✅ **进度显示**: 实时显示下载和上传进度
- ✅ **无依赖部署**: 支持打包为独立exe，无需Python环境（NEW!）

## 系统要求

### 开发环境
- Python 3.8 或更高版本
- 稳定的网络连接
- 百度网盘账号
- SFTP服务器访问权限（可选）

### 部署环境（无Python模式）
- Windows 7/8/10/11
- **无需Python环境**
- **无需安装bypy**
- 稳定的网络连接

## 安装

### 方式一：无Python部署（推荐）

适用于没有Python环境的Windows电脑，或者需要快速部署的场景。

```bash
# 开发机：创建发布包
create_release.bat

# 目标机：运行安装
install.bat

# 配置认证和SFTP后即可使用
pan-download --test-config
pan-download 260701 --upload-sftp
```

详细说明请查看：[无依赖部署指南](docs/deployment/no-python/README.md)

### 方式二：Python环境安装

适用于有Python环境的开发机器。

#### 1. 克隆项目

```bash
git clone <repository-url>
cd dupan-download
```

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

#### 3. 安装工具

```bash
python setup.py install
```

## 配置

### 1. 创建配置文件

复制配置模板：

```bash
cp .env.example .env
```

### 2. 填写配置信息

编辑 `.env` 文件，填入实际的配置信息：

```bash
# SFTP服务器配置（必需，如需上传功能）
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

### 3. 配置百度网盘认证

本项目使用 **bypy** 库进行百度网盘下载，采用 OAuth 认证方式：

```bash
# 运行认证向导
pan-download --setup-bypy

# 或直接使用bypy命令
bypy info
```

认证信息会自动保存在 `~/.bypy/` 目录中，无需在 `.env` 文件中配置。

## 使用方法

### 基本用法

```bash
dupan-download <网盘链接> <提取码>
```

### 示例

```bash
# 下载并上传，完成后自动清理临时文件
dupan-download https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg 0409

# 保留临时文件用于调试
dupan-download https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg 0409 --keep-temp

# 指定临时目录
dupan-download https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg 0409 --temp-dir "D:/temp"

# 详细输出模式
dupan-download https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg 0409 --verbose
```

### 输出说明

```
$ dupan-download https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg 0409

2026-07-02 10:00:00 - dupan_download - INFO - 配置加载成功
2026-07-02 10:00:00 - dupan_download - INFO - 临时目录: /tmp/dupan_download_12345
2026-07-02 10:00:01 - dupan_download - INFO - 验证链接: https://pan.baidu.com/s/...?pwd=****
2026-07-02 10:00:02 - dupan_download - INFO - ✓ 链接验证成功
2026-07-02 10:00:03 - dupan_download - INFO - 开始下载文件...
2026-07-02 10:00:30 - dupan_download - INFO - ✓ 下载完成: 18 成功, 0 失败
2026-07-02 10:00:31 - dupan_download - INFO - 开始上传文件...
2026-07-02 10:01:00 - dupan_download - INFO - ✓ 上传完成: 18 成功, 0 失败
2026-07-02 10:01:01 - dupan_download - INFO - ✓ 清理临时文件

执行完成
✓ 成功处理: 18 个文件
✗ 失败: 0 个文件
```

## 命令选项

| 选项 | 说明 |
|------|------|
| `--keep-temp` | 保留临时文件，不自动清理 |
| `--temp-dir PATH` | 指定临时文件目录 |
| `--verbose` | 启用详细输出模式 |
| `--help` | 显示帮助信息 |

## 错误处理

工具具备智能错误处理机制：

### 网络错误
- 自动重试（默认3次）
- 连接超时控制
- 网络中断自动重连

### 文件错误
- 跳过无法访问的文件
- 继续处理其他文件
- 提供详细的错误报告

### 配置错误
- 启动时验证配置
- 友好的错误提示
- 指出缺失的配置项

## 故障排除

### 配置相关

**问题**: 提示"缺少必需的配置"
**解决**: 检查 `.env` 文件是否存在且包含所有必需的配置项

### 网络相关

**问题**: 连接超时
**解决**:
1. 检查网络连接
2. 增加 `CONNECT_TIMEOUT` 和 `TRANSFER_TIMEOUT` 值
3. 检查防火墙设置

### 权限相关

**问题**: 文件上传失败
**解决**:
1. 验证SFTP用户权限
2. 检查目标目录是否存在
3. 确保有足够的磁盘空间

## 开发

### 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_config.py -v

# 运行测试并查看覆盖率
pytest tests/ --cov=dupan_download --cov-report=html
```

### 项目结构

```
dupan-download/
├── dupan_download/          # 主要代码
│   ├── __init__.py
│   ├── cli.py              # 命令行接口
│   ├── config.py           # 配置管理
│   ├── downloader.py       # 下载模块
│   ├── uploader.py         # 上传模块
│   └── utils.py            # 工具函数
├── tests/                   # 测试文件
│   ├── test_config.py
│   ├── test_downloader.py
│   ├── test_uploader.py
│   ├── test_utils.py
│   └── test_integration.py
├── .env.example             # 配置模板
├── requirements.txt         # 依赖列表
└── README.md               # 项目文档
```

## 安全建议

1. **保护敏感信息**: 永远不要将 `.env` 文件提交到版本控制
2. **使用强密码**: 为SFTP账户使用强密码
3. **定期更新**: 定期更新依赖包以获取安全补丁
4. **日志安全**: 工具会自动遮蔽日志中的敏感信息

## 许可证

MIT License

## 贡献

欢迎提交问题报告和功能请求！

## 更新日志

### v1.0.0 (2026-07-02)
- ✨ **重大更新**: 支持无Python环境部署
- ✅ 打包为独立exe文件
- ✅ 内置所有依赖（包括bypy）
- ✅ 智能认证文件处理
- ✅ 一键安装脚本
- ✅ 用户友好的配置向导
- 🔧 改进的错误处理和日志

### v0.1.0 (2026-07-02)
- 初始版本发布
- 支持基本的下载和上传功能
- 错误处理和重试机制
- 详细的执行报告

## 🚀 快速开始指南

### 无Python环境部署（推荐）

```bash
# 开发机：一键创建发布包
create_release.bat

# 目标机：一键安装
install.bat

# 配置测试
pan-download --test-config

# 开始使用
pan-download 260701 --upload-sftp
```

### Python环境部署

```bash
# 安装依赖
pip install -r requirements.txt

# 认证bypy
bypy info

# 运行程序
python -m dupan_download.integrated_cli 260701 --upload-sftp
```

## 📚 详细文档

### 📖 文档中心
- **[文档导航](docs/README.md)** - 完整的文档索引和导航

### 🚀 快速开始
- **[快速入门](docs/reference/quick-start.md)** - 5分钟快速上手
- **[解决方案](docs/reference/solution.md)** - 完整功能说明

### 👥 用户指南
- **[使用指南](docs/guides/usage/README.md)** - 基本使用方法
- **[配置指南](docs/guides/config/overview.md)** - 配置文件说明
- **[SFTP配置](docs/guides/config/sftp.md)** - SFTP服务器配置
- **[临时文件处理](docs/guides/usage/temp-files.md)** - 文件保留和管理

### 🚀 部署相关
- **[无Python部署](docs/deployment/no-python/README.md)** - 无依赖部署
- **[部署指南](docs/deployment/installation/README.md)** - 完整部署步骤
- **[发布指南](docs/deployment/packaging/release.md)** - 打包发布流程

### 💻 开发相关
- **[项目状态](docs/development/project/status.md)** - 开发进度
- **[测试计划](docs/development/testing/README.md)** - 测试策略
- **[SFTP功能](docs/development/features/sftp-upload.md)** - 功能实现说明
