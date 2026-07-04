# 开发相关文档

开发相关文档包含项目开发、测试、功能实现的技术文档。

## 📚 文档列表

### 测试
- **[测试计划](testing/README.md)** - 测试策略、计划和验证方法

### 项目管理
- **[项目状态](project/status.md)** - 开发进度、TODO和里程碑

### 功能开发
- **[SFTP上传功能](features/sftp-upload.md)** - SFTP上传实现详情和修复记录

## 🎯 开发资源

### 核心功能开发
- **下载功能** - 百度网盘文件下载
- **上传功能** - SFTP文件上传
- **认证管理** - bypy认证处理
- **配置管理** - 环境配置和验证

### 技术栈
- **Python 3.8+** - 开发语言
- **Click** - 命令行框架
- **Paramiko** - SFTP客户端
- **bypy** - 百度网盘API
- **PyInstaller** - 打包工具

## 🔧 开发工具

### 代码结构
```
dupan_download/
├── cli.py              # 命令行接口
├── integrated_cli.py   # 整合CLI
├── config.py           # 配置管理
├── downloader.py       # 下载模块
├── uploader.py         # 上传模块
└── utils.py            # 工具函数
```

### 测试结构
```
tests/
├── test_config.py      # 配置测试
├── test_downloader.py  # 下载测试
├── test_uploader.py    # 上传测试
└── test_integration.py # 集成测试
```

## 📋 开发流程

### 1. 功能开发
- 编写功能代码
- 添加单元测试
- 更新相关文档

### 2. 测试验证
```bash
# 运行测试
pytest tests/ -v

# 运行特定测试
pytest tests/test_uploader.py -v
```

### 3. 打包发布
```bash
# 创建发布包
create_release.bat

# 本地测试
dist\pan-download.exe --test-config
```

## 🚀 待开发功能

- [ ] 支持SFTP密钥认证
- [ ] 添加进度条显示
- [ ] 支持断点续传
- [ ] 多线程上传下载
- [ ] Web界面
- [ ] Docker支持

## 🔗 相关文档

- **[部署指南](../deployment/README.md)** - 打包和发布
- **[用户指南](../guides/README.md)** - 功能说明
- **[文档中心](../README.md)** - 文档导航

---

返回：[文档中心](../README.md) | [项目主页](../../README.md)