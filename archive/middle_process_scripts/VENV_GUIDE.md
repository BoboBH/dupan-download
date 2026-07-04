# Python虚拟环境使用指南

## 🐍 虚拟环境说明

本项目使用Python虚拟环境(`.venv`)来隔离项目依赖，避免与系统Python环境冲突。

## 📋 虚拟环境信息

- **路径**: `d:\git\dupan-download\.venv`
- **Python版本**: 与创建虚拟环境时使用的Python版本相同
- **目的**: 隔离项目依赖，确保开发和部署环境一致

## 🚀 激活虚拟环境

### Windows (CMD)
```cmd
.venv\Scripts\activate
```

### Windows (PowerShell)
```powershell
.venv\Scripts\Activate.ps1
```

### Git Bash / Linux / macOS
```bash
source .venv/bin/activate
```

## 📦 已安装的依赖

根据 `requirements.txt`，虚拟环境将包含以下依赖：

```
click>=8.0.0              # CLI框架
python-dotenv>=0.19.0     # 环境变量管理
paramiko>=2.11.0          # SFTP上传
requests>=2.27.0           # HTTP请求
tqdm>=4.62.0              # 进度条显示
pytest>=7.0.0             # 测试框架
BaiduPCS-Py>=0.7.4        # 百度网盘API
```

## 🔧 常用命令

### 查看已安装的包
```bash
pip list
```

### 查看包的详细信息
```bash
pip show <package-name>
```

### 安装新的包
```bash
pip install <package-name>
```

### 卸载包
```bash
pip uninstall <package-name>
```

### 导出当前依赖
```bash
pip freeze > requirements.txt
```

### 升级pip
```bash
python -m pip install --upgrade pip
```

## 🏃 运行项目

### 激活虚拟环境后运行
```bash
# 1. 激活虚拟环境
.venv\Scripts\activate

# 2. 运行下载工具
python -m dupan_download.cli <分享链接> <提取码>

# 3. 运行测试
pytest tests/ -v

# 4. 退出虚拟环境
deactivate
```

### 直接使用虚拟环境Python（无需激活）
```bash
# Windows
.venv\Scripts\python.exe -m dupan_download.cli <分享链接> <提取码>

# Linux/macOS
.venv/bin/python -m dupan_download.cli <分享链接> <提取码>
```

## 🛠️ 故障排除

### 问题1: 虚拟环境激活失败
**症状**: 执行 `activate` 脚本时报错
**解决**:
```cmd
# Windows CMD，确保执行策略允许
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

### 问题2: pip命令找不到
**症状**: 激活虚拟环境后 `pip` 命令不可用
**解决**:
```bash
# 使用python -m pip代替pip
python -m pip install <package>
```

### 问题3: 依赖安装失败
**症状**: `pip install -r requirements.txt` 失败
**解决**:
```bash
# 1. 升级pip
python -m pip install --upgrade pip

# 2. 清除pip缓存
pip cache purge

# 3. 使用国内镜像源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 问题4: BaiduPCS-Py安装失败
**症状**: 编译错误或依赖冲突
**解决**:
```bash
# 方法1: 安装预编译版本
pip install BaiduPCS-Py --only-binary=:all:

# 方法2: 使用conda环境
conda create -n dupan python=3.10
conda activate dupan
pip install -r requirements.txt
```

## 📝 开发建议

### 1. 始终在虚拟环境中工作
```bash
# 进入项目目录后首先激活虚拟环境
cd d:\git\dupan-download
.venv\Scripts\activate
```

### 2. IDE配置
#### VSCode
- 会自动检测虚拟环境
- 确保右下角显示的是 `.venv` 解释器

#### PyCharm
- File → Settings → Project → Python Interpreter
- 选择 `.venv` 目录中的Python解释器

### 3. Git配置
将 `.venv` 目录添加到 `.gitignore`:
```
.venv/
__pycache__/
*.pyc
```

## 🔄 重建虚拟环境

如果虚拟环境出现问题，可以删除并重建：

```bash
# Windows
rmdir /s .venv
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

# Linux/macOS
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 📚 更多信息

- [Python虚拟环境文档](https://docs.python.org/3/library/venv.html)
- [pip用户指南](https://pip.pypa.io/en/stable/user_guide/)
