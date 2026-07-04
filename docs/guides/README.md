# 用户指南

用户指南提供了使用百度网盘下载工具的完整说明。无论你是新手还是高级用户，都能在这里找到所需的信息。

## 📚 文档列表

### 使用指南
- **[使用指南总览](usage/README.md)** - 基本使用方法和命令
- **[临时文件处理](usage/temp-files.md)** - 如何保留和管理下载的文件

### 配置指南
- **[配置总览](config/overview.md)** - 配置文件和参数说明
- **[SFTP配置](config/sftp.md)** - SFTP服务器详细配置指南

## 🎯 按需查找

### 我想了解...
- **基本使用** → [使用指南总览](usage/README.md)
- **配置SFTP** → [SFTP配置](config/sftp.md)
- **保留下载文件** → [临时文件处理](usage/temp-files.md)
- **配置参数说明** → [配置总览](config/overview.md)

## 🔧 常用配置场景

### 场景1：基本下载
```bash
pan-download apps/bypy/folder_name
```

### 场景2：下载并上传到SFTP
```bash
pan-download apps/bypy/folder_name --upload-sftp
```

### 场景3：保留本地副本
```bash
pan-download apps/bypy/folder_name --upload-sftp --keep-temp
```

### 场景4：指定存储位置
```bash
pan-download apps/bypy/folder_name --temp-dir "C:\MyDownloads"
```

## 📖 相关文档

- **[快速入门](../reference/quick-start.md)** - 5分钟快速上手
- **[故障排除](../development/features/sftp-upload.md)** - 解决常见问题
- **[部署指南](../deployment/installation/README.md)** - 安装和部署

---

返回：[文档中心](../README.md) | [项目主页](../../README.md)