# 临时文件保留功能使用指南

## 🎯 功能说明

现在支持多种方式来控制临时文件的处理，让你可以更灵活地管理下载的文件。

## 📋 参数说明

### 1. `--keep-temp`
**作用**: 保留下载的临时文件，不自动清理

### 2. `--temp-dir PATH`
**作用**: 指定临时文件的存储位置

**特性**:
- 当使用 `--temp-dir` 时，会自动启用 `--keep-temp`
- 可以指定任意目录来存储下载的文件
- 程序会自动创建不存在的目录

## 🚀 使用示例

### 示例1: 保留临时文件（默认位置）

```bash
# 下载后保留文件在系统临时目录
pan-download 260701 --keep-temp
```

**输出示例**:
```
📁 临时文件已保留: C:\Users\YourName\AppData\Local\Temp\dupan_download_12345
📂 正在打开文件位置...
✅ 已自动打开文件位置

🎉 任务完成！
📥 下载位置: C:\Users\YourName\AppData\Local\Temp\dupan_download_12345
💾 临时文件: 已保留
📊 文件大小: 125.50 MB
```

### 示例2: 保留到指定目录

```bash
# 保留文件到指定目录
pan-download 260701 --keep-temp --temp-dir "C:\MyDownloads"
```

**输出示例**:
```
使用指定的临时目录: C:\MyDownloads
📁 临时文件已保留: C:\MyDownloads
📂 正在打开文件位置...
✅ 已自动打开文件位置

🎉 任务完成！
📥 下载位置: C:\MyDownloads
💾 临时文件: 已保留 (C:\MyDownloads)
📊 文件大小: 125.50 MB

💡 下一步操作:
   - 查看文件: C:\MyDownloads
   - 手动上传到其他位置
   - 完成后手动删除此文件夹
```

### 示例3: 只使用 --temp-dir（自动保留）

```bash
# 只指定目录，自动保留文件
pan-download 260701 --temp-dir "D:\Data\Backup"
```

**说明**: 当使用 `--temp-dir` 时，会自动启用 `--keep-temp`，无需重复指定。

### 示例4: 下载并上传 + 保留临时文件

```bash
# 下载、上传到SFTP，同时保留本地副本
pan-download 260701 --upload-sftp --keep-temp --temp-dir "C:\LocalBackup"
```

**适用场景**:
- 需要上传到SFTP服务器
- 同时保留本地备份
- 用于数据迁移或备份

### 示例5: 下载后不保留（默认行为）

```bash
# 下载后自动清理临时文件
pan-download 260701
```

**输出示例**:
```
✅ 已清理临时文件
🗑️ 临时文件: 已清理
```

## 🎯 使用场景

### 场景1: 数据备份
```bash
# 下载网盘数据到本地备份
pan-download backup_folder --keep-temp --temp-dir "D:\Backups\2026-07-02"
```

### 场景2: 数据迁移
```bash
# 下载并上传到新服务器，同时保留本地副本
pan-download data_folder --upload-sftp --keep-temp --temp-dir "C:\Migration"
```

### 场景3: 临时查看
```bash
# 下载后查看，确认无误后手动删除
pan-download temp_files --keep-temp
```

### 场景4: 批量处理
```bash
# 下载后进行其他处理
pan-download processing_input --keep-temp --temp-dir "C:\Processing"

# 然后可以处理下载的文件
cd C:\Processing
# 运行其他处理脚本...
```

## 🔧 参数对比

| 参数组合 | 行为 | 适用场景 |
|---------|------|----------|
| 无额外参数 | 自动清理临时文件 | 常规下载上传 |
| `--keep-temp` | 保留在系统临时目录 | 临时查看或调试 |
| `--temp-dir PATH` | 保留到指定目录 | 长期存储或备份 |
| `--local-dir PATH` | 直接下载到指定目录 | 直接使用，不经过临时目录 |

## ⚠️ 注意事项

### 1. 磁盘空间
- 保留临时文件会占用磁盘空间
- 大文件下载时注意磁盘容量
- 定期清理不需要的文件

### 2. 权限要求
- 确保对目标目录有写入权限
- 某些系统目录可能需要管理员权限

### 3. 路径格式
- Windows: 使用反斜杠 `\` 或正斜杠 `/`
- 建议使用引号包含路径（特别是包含空格的路径）

### 4. 文件覆盖
- 如果目标目录已存在同名文件，可能会被覆盖
- 建议使用唯一的目录名称

## 💡 最佳实践

### 1. 定期清理
```bash
# 定期清理旧的临时文件
# Windows
dir %TEMP%\dupan_download_*

# 手动删除不需要的文件夹
```

### 2. 有意义的目录名
```bash
# 使用有意义的目录名
pan-download project_data --keep-temp --temp-dir "C:\Projects\2026-07-02"
```

### 3. 结合其他参数
```bash
# 完整的参数组合
pan-download data_folder \
  --upload-sftp \
  --keep-temp \
  --temp-dir "C:\Backup" \
  --verbose
```

## 🎨 用户体验增强

### 自动打开文件夹
- 在Windows上，程序会自动打开文件位置
- 如果自动打开失败，会提供手动路径

### 文件大小显示
- 程序会计算并显示临时文件的总大小
- 帮助你了解磁盘占用情况

### 操作建议
- 程序会提供后续操作的建议
- 帮助你更好地处理下载的文件

## 📝 命令参考

```bash
# 完整命令格式
pan-download <远程文件夹> [选项]

# 选项说明：
--local-dir PATH          # 直接指定本地下载目录
--upload-sftp            # 下载后上传到SFTP
--keep-temp              # 保留临时文件
--temp-dir PATH          # 指定临时文件位置
--verbose                # 详细输出模式
--setup-bypy            # 启动认证向导
--test-config           # 测试配置
```

---

现在你有更灵活的控制方式来管理下载的临时文件了！🎉