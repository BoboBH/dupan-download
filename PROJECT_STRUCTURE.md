# 项目结构说明

## 📁 项目根目录结构

```
dupan-download/
├── dupan_download/           # 主程序包
│   ├── __init__.py
│   ├── __main__.py          # PyInstaller 入口点
│   ├── cli.py               # 命令行接口
│   ├── config.py            # 配置管理
│   ├── downloader.py        # 下载器
│   ├── uploader.py          # SFTP 上传器
│   └── utils.py             # 工具函数
│
├── setup/                   # ⭐ 打包构建脚本
│   ├── setup.bat            # 🔧 主打包脚本（推荐使用）
│   ├── auto_build.bat       # 自动构建脚本
│   ├── build.bat            # 基础构建脚本
│   ├── build.spec           # PyInstaller 配置文件
│   ├── quick_build.bat      # 快速构建脚本
│   ├── create_deployment_package.bat  # 创建部署包
│   ├── create_release.bat   # 创建发布包
│   ├── create_release_zip.bat       # 创建 ZIP 分发包
│   ├── deploy_setup.bat     # 部署设置脚本
│   └── cleanup.bat          # 清理脚本
│
├── docs/                    # 📚 文档目录
│   ├── guides/              # 使用指南
│   │   ├── BYPY_AUTHENTICATION_GUIDE.md
│   │   ├── COMPLETE_INSTALL_GUIDE.md
│   │   ├── INSTALL_FIX_GUIDE.md
│   │   ├── PACKAGING_GUIDE.md
│   │   └── PYTHON_EXPLANATION.md
│   │
│   ├── reports/             # 技术报告
│   │   ├── DEPLOYMENT_VERIFICATION_REPORT.md
│   │   ├── DEPLOYMENT_ZIP_VERIFICATION_REPORT.md
│   │   └── PACKAGING_FIX_REPORT.md
│   │
│   ├── AUTH_FILES_README.md
│   ├── docs_restructure_complete.md
│   ├── docs_restructure_plan.md
│   └── PACKAGE_COMPLETE.md
│
├── delete/                  # 🗑️ 已删除/不需要的文件
│   ├── .env.backup
│   ├── .env.clean
│   ├── .env.simple
│   ├── pan-download-mock.exe
│   ├── test_flow.bat
│   ├── test_install.bat
│   ├── release_1.0.0_20260702.zip
│   └── test_deployment/
│
├── archive/                 # 📦 归档的旧代码
├── examples/                # 📝 示例代码
├── test/                    # 🧪 测试文件
│
├── .venv/                   # Python 虚拟环境
├── build/                   # PyInstaller 构建输出（临时）
├── dist/                    # 打包的可执行文件（临时）
├── release_*/               # 发布包（临时）
│
├── .env                     # 本地配置（不提交）
├── .env.example             # 配置模板
├── .gitignore               # Git 忽略规则
├── requirements.txt         # Python 依赖
├── setup.py                 # 包安装配置
├── README.md                # ⭐ 项目说明
└── dupan-download-windows-2.0.0.zip  # 最终分发包
```

## 🚀 快速开始

### 开发环境设置

```bash
# 1. 创建虚拟环境
python -m venv .venv

# 2. 激活虚拟环境
.venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行程序
python -m dupan_download --help
```

### 打包构建

```bash
# 方法一：使用主打包脚本（推荐）
cd setup
setup.bat all

# 方法二：分步构建
setup.bat build      # 构建可执行文件
setup.bat package    # 创建部署包
setup.bat zip        # 创建 ZIP 分发包

# 方法三：使用原始脚本
cd setup
auto_build.bat        # 完整自动构建
quick_build.bat       # 快速构建
```

### 清理构建文件

```bash
cd setup
cleanup.bat
```

## 📦 打包流程

### 完整打包流程

```
1. setup.bat build
   ↓
   检查虚拟环境
   ↓
   安装 PyInstaller
   ↓
   清理旧构建
   ↓
   执行 PyInstaller (build.spec)
   ↓
   生成: dist\pan-download.exe
```

### 部署包创建流程

```
2. setup.bat package
   ↓
   创建 release_2.0.0_20260703\dupan-download-windows\
   ↓
   复制文件:
   - pan-download.exe
   - .env.example
   - README.md
   - INSTALL_GUIDE.md
   - 快速开始.bat
   - 验证安装.bat
```

### ZIP 分发包创建流程

```
3. setup.bat zip
   ↓
   压缩部署包目录
   ↓
   生成: dupan-download-windows-2.0.0.zip
```

## 🎯 目录说明

### setup/ 目录 - 打包构建工具

**主要文件：**
- **setup.bat** - 🔧 主打包脚本（推荐使用）
- **build.spec** - PyInstaller 配置文件
- **cleanup.bat** - 清理构建文件

**辅助脚本：**
- auto_build.bat - 完整自动构建
- build.bat - 基础构建
- quick_build.bat - 快速构建
- create_*.bat - 各种创建脚本

### docs/ 目录 - 文档中心

**子目录：**
- **guides/** - 用户指南和教程
- **reports/** - 技术报告和验证文档

**主要文档：**
- BYPY_AUTHENTICATION_GUIDE.md - 认证配置指南
- PACKAGING_FIX_REPORT.md - 打包问题修复报告
- DEPLOYMENT_VERIFICATION_REPORT.md - 部署验证报告

### delete/ 目录 - 已删除文件

**包含：**
- 备份配置文件
- 测试文件
- 旧版本发布包
- 临时文件

**注意：** 此目录中的文件可以安全删除

## 🔧 常用命令

### 开发命令

```bash
# 安装依赖
pip install -r requirements.txt

# 运行程序
python -m dupan_download --help
python -m dupan_download apps/bypy/test_pdf --keep-temp

# 运行测试
pytest
```

### 打包命令

```bash
# 完整打包
cd setup && setup.bat all

# 仅构建
cd setup && setup.bat build

# 清理
cd setup && cleanup.bat
```

### 部署命令

```bash
# 目标机器上
pan-download.exe --help
pan-download.exe --setup-bypi
pan-download.exe --test-config
pan-download.exe apps/bypy/test_pdf --keep-temp
```

## 📊 文件大小参考

| 文件/目录 | 大小 | 说明 |
|----------|------|------|
| .venv/ | ~500 MB | 虚拟环境（仅开发） |
| dist/pan-download.exe | ~18 MB | 可执行文件（包含依赖） |
| dupan-download-windows-2.0.0.zip | ~17 MB | 最终分发包 |
| release_2.0.0_20260703/ | ~18 MB | 部署包目录 |

## 🎯 重要路径

### 开发环境
- **项目根目录：** `D:\git\dupan-download\`
- **虚拟环境：** `.venv\`
- **主程序包：** `dupan_download\`

### 构建输出
- **构建配置：** `setup\build.spec`
- **可执行文件：** `dist\pan-download.exe`
- **部署包：** `release_2.0.0_20260703\dupan-download-windows\`

### 分发
- **ZIP 分发包：** `dupan-download-windows-2.0.0.zip`
- **目标部署位置：** `D:\baidu-download\` 或其他位置

## 🔒 配置文件

### 开发配置
- **.env** - 本地开发配置（不提交）
- **.env.example** - 配置模板

### 认证配置
- **~/.bypy/bypy.json** - 百度网盘认证（用户机器）

## 📝 维护指南

### 添加新的打包脚本

1. 将脚本放置在 `setup/` 目录
2. 更新 `setup/setup.bat` 菜单
3. 更新本文档

### 添加新的文档

1. 用户指南 → `docs/guides/`
2. 技术报告 → `docs/reports/`
3. 更新 README.md 链接

### 清理项目

```bash
# 清理构建文件
cd setup && cleanup.bat

# 清理不需要的文件
# 手动移动到 delete/ 目录
```

## 🎉 总结

### 项目结构特点

✅ **清晰分离**
- 开发代码在 `dupan_download/`
- 打包脚本在 `setup/`
- 文档在 `docs/`
- 废弃文件在 `delete/`

✅ **易于维护**
- 统一的打包入口（setup.bat）
- 清晰的文档分类
- 适当的文件清理

✅ **便于分发**
- 独立的 ZIP 分发包
- 完整的部署文档
- 自动化的构建流程

### 快速参考

| 任务 | 命令/位置 |
|------|----------|
| **构建程序** | `cd setup && setup.bat build` |
| **创建分发包** | `cd setup && setup.bat all` |
| **清理构建** | `cd setup && cleanup.bat` |
| **查看文档** | `ls docs/guides/` |
| **查看报告** | `ls docs/reports/` |

---

**文档版本：** 2.0.0
**最后更新：** 2026-07-03
**项目状态：** ✅ 结构已整理完成
