# 下载和上传整合流程使用指南

## 🎯 快速开始

### 基本用法

```bash
# 激活虚拟环境
cd d:\git\dupan-download
.venv\Scripts\activate

# 只下载文件
pan-download apps/bypy/260701

# 下载并自动上传到SFTP
pan-download apps/bypy/260701 --upload-sftp
```

## 📋 参数说明

### 必需参数
- `remote_folder`: 百度网盘文件夹路径
  - 格式: `apps/bypy/{folder_name}`
  - 示例: `apps/bypy/260701`

### 可选参数
- `--local-dir PATH`: 本地下载目录
  - 默认: 临时目录
  - 示例: `--local-dir "D:\我的文件"`

- `--upload-sftp`: 下载后自动上传到SFTP
  - 默认: 不上传
  - 需要配置.env中的SFTP信息

- `--keep-temp`: 保留临时文件
  - 默认: 自动清理
  - 用于调试或文件检查

- `--verbose`: 显示详细日志
  - 默认: 简洁模式

## 🚀 使用场景

### 场景1: 只下载文件

```bash
pan-download apps/bypy/260701 --local-dir "D:\我的PDF文件"
```

**流程**:
1. ✅ 下载网盘文件到 `D:\我的PDF文件\`
2. ✅ 显示下载统计
3. ✅ 自动清理临时文件

### 场景2: 下载并上传SFTP

```bash
# 首先配置.env中的SFTP信息
# 然后执行
pan-download apps/bypy/260701 --upload-sftp --local-dir "D:\工作文件"
```

**流程**:
1. ✅ 下载网盘文件到 `D:\工作文件\`
2. ✅ 连接SFTP服务器
3. ✅ 上传文件到SFTP服务器
4. ✅ 显示上传统计
5. ✅ 自动清理临时文件

### 场景3: 保留文件用于检查

```bash
pan-download apps/bypy/260701 --keep-temp --local-dir "D:\检查文件"
```

## 📊 配置要求

### .env配置（如果使用--upload-sftp）

```bash
# SFTP服务器配置
SFTP_HOST=sftp.example.com
SFTP_PORT=22
SFTP_USERNAME=your_username
SFTP_PASSWORD=your_password
SFTP_REMOTE_PATH=/remote/path
```

### bypy认证（自动管理）

bypy使用OAuth认证，无需在.env中配置：
- ✅ 首次使用会引导认证
- ✅ Token自动续期
- ✅ 长期有效

## 📈 执行过程

### 只下载模式
```
1. 验证路径格式
2. 创建本地目录
3. 下载文件 (bypy)
4. 显示下载统计
5. 清理临时文件
```

### 下载+上传模式
```
1. 验证路径格式
2. 创建本地目录
3. 下载文件 (bypy)
4. 连接SFTP服务器
5. 上传文件 (paramiko)
6. 显示上传统计
7. 清理临时文件
```

## 🎯 实际使用示例

### 下载单个文件夹
```bash
pan-download apps/bypy/260701 --local-dir "D:\投资研报"
```

### 批量处理
```bash
# 处理多个文件夹
pan-download apps/bypy/260701
pan-download apps/bypy/270702
pan-download apps/bypy/270703
```

### 自动化工作流
```bash
# 每日自动下载最新文件并上传
pan-download apps/bypy/每日研报 --upload-sftp --local-dir "D:\每日更新"
```

## 🔧 故障排除

### 常见问题

**问题1: 找不到pan-download命令**
```bash
# 重新安装项目
cd d:\git\dupan-download
.venv\Scripts\activate
pip install -e .
```

**问题2: SFTP连接失败**
```bash
# 检查.env配置
# 确保SFTP服务器信息正确
# 测试连接: telnet sftp.example.com 22
```

**问题3: 下载失败**
```bash
# 检查网盘路径格式
.venv\Scripts\bypy.exe list apps/bypy/
# 确认路径存在
```

## 📊 输出示例

### 成功输出
```
==================================================
开始下载阶段
==================================================
下载路径: /apps/bypy/260701
本地路径: D:\PDF下载\
下载完成: 93 成功, 0 失败

==================================================
开始SFTP上传阶段
==================================================
连接SFTP: sftp.example.com:22
上传完成: 93 成功, 0 失败
清理临时文件

==================================================
执行完成
==================================================
🎉 任务完成！
📁 下载位置: D:\PDF下载
📤 SFTP上传: /remote/path
```

## 🎉 快速开始

```bash
# 1. 激活环境
cd d:\git\dupan-download
.venv\Scripts\activate

# 2. 下载并上传
pan-download apps/bypy/260701 --upload-sftp
```
