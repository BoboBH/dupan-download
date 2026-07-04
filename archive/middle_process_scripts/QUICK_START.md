# 百度网盘下载工具 - 快速开始

## 🚀 快速启动

### 1. 激活虚拟环境

**Windows CMD:**
```cmd
activate_venv.bat
```

**Windows PowerShell:**
```powershell
.\activate_venv.ps1
```

**或者手动激活:**
```cmd
.venv\Scripts\activate
```

### 2. 使用下载工具

```bash
# 基本用法
python -m dupan_download.cli <分享链接> <提取码>

# 示例
python -m dupan_download.cli https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg 0409

# 保留临时文件
python -m dupan_download.cli <链接> <提取码> --keep-temp

# 指定临时目录
python -m dupan_download.cli <链接> <提取码> --temp-dir "D:\我的下载"

# 详细日志
python -m dupan_download.cli <链接> <提取码> --verbose
```

### 3. 运行测试

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_config.py -v

# 查看测试覆盖率
pytest tests/ --cov=dupan_download --cov-report=html
```

### 4. 退出虚拟环境

```bash
deactivate
```

## 📋 项目结构

```
dupan-download/
├── .venv/                      # 虚拟环境（刚刚创建）
├── dupan_download/             # 主要代码
│   ├── __init__.py
│   ├── cli.py                  # 命令行接口
│   ├── config.py               # 配置管理
│   ├── downloader.py           # 下载模块
│   ├── uploader.py             # SFTP上传模块
│   └── utils.py                # 工具函数
├── tests/                      # 测试文件
├── .env                        # 环境变量配置
├── requirements.txt             # 项目依赖
├── activate_venv.bat            # Windows CMD激活脚本
├── activate_venv.ps1            # PowerShell激活脚本
└── README.md                   # 项目文档
```

## 🔧 配置说明

### 环境变量配置 (.env)

```bash
# 百度网盘API配置
BAIDU_APP_ID=your_app_id
BAIDU_APP_KEY=your_app_key
BAIDU_SECRET_KEY=your_secret_key
BAIDU_ACCESS_TOKEN=your_access_token
BAIDU_BDUSS=your_bduss_value
BAIDU_COOKIES=your_cookies_value

# SFTP服务器配置（可选）
SFTP_HOST=sftp.example.com
SFTP_PORT=22
SFTP_USERNAME=your_username
SFTP_PASSWORD=your_password
SFTP_REMOTE_PATH=/remote/path

# 重试和超时配置
MAX_RETRIES=3
CONNECT_TIMEOUT=30
TRANSFER_TIMEOUT=300
```

## 🎯 常用命令

### 虚拟环境管理
```bash
# 查看已安装的包
pip list

# 安装新的包
pip install <package-name>

# 升级pip
python -m pip install --upgrade pip

# 导出依赖
pip freeze > requirements.txt
```

### 开发和测试
```bash
# 运行特定测试文件
pytest tests/test_downloader.py -v

# 运行测试并查看覆盖率
pytest tests/ --cov=dupan_download --cov-report=html

# 查看详细日志
python -m dupan_download.cli <链接> <提取码> --verbose
```

## 📊 功能特性

- ✅ **自动下载**: 从百度网盘自动下载文件夹
- ✅ **目录结构保持**: 完整保持原始目录结构
- ✅ **SFTP上传**: 自动上传到指定SFTP服务器
- ✅ **错误处理**: 智能错误处理和重试机制
- ✅ **详细报告**: 提供成功/失败文件的详细报告
- ✅ **灵活配置**: 支持环境变量和配置文件
- ✅ **进度显示**: 实时显示下载和上传进度

## 🛠️ 故障排除

### 问题1: 虚拟环境激活失败
```cmd
# Windows PowerShell执行策略问题
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

### 问题2: 依赖安装失败
```bash
# 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题3: 权限错误
```bash
# 以管理员身份运行CMD或PowerShell
```

## 📚 更多文档

- [README.md](README.md) - 完整项目文档
- [VENV_GUIDE.md](VENV_GUIDE.md) - 虚拟环境详细指南
- [INSTALL_FIX.md](INSTALL_FIX.md) - 依赖问题解决方案

## 🎉 开始使用

1. **激活虚拟环境**: 运行 `activate_venv.bat` 或 `activate_venv.ps1`
2. **测试下载**: 使用上面的示例命令测试下载功能
3. **查看结果**: 检查下载的文件和日志输出

祝你使用愉快！
