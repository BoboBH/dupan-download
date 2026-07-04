# SFTP配置指南

## 📍 当前配置状态

你的 `.env` 文件已包含以下SFTP配置：

```env
SFTP_HOST=192.168.0.122
SFTP_PORT=22
SFTP_USERNAME=sftp01
SFTP_PASSWORD=123456
SFTP_REMOTE_PATH=/remote/path
```

## 🔧 配置说明

### 各参数含义

| 参数 | 当前值 | 说明 | 示例 |
|------|--------|------|------|
| `SFTP_HOST` | 192.168.0.122 | SFTP服务器地址 | 可以是IP或域名 |
| `SFTP_PORT` | 22 | SFTP端口号 | 默认22，自定义端口需修改 |
| `SFTP_USERNAME` | sftp01 | 登录用户名 | SFTP服务器用户名 |
| `SFTP_PASSWORD` | 123456 | 登录密码 | SFTP服务器密码 |
| `SFTP_REMOTE_PATH` | /remote/path | 远程目标路径 | 文件上传的目标目录 |

## ⚠️ 重要提醒

### 1. 修改远程路径
```env
# 需要修改：将 /remote/path 改为实际的上传目标目录
SFTP_REMOTE_PATH=/home/sftp01/uploads
# 或者
SFTP_REMOTE_PATH=/data/backup
```

### 2. 安全建议
```env
# ⚠️ 注意：.env文件包含敏感信息，请：
# 1. 不要提交到git仓库
# 2. 设置合适的文件权限
# 3. 定期更换密码
```

## 🚀 测试配置

### 方法1：使用程序测试
```bash
# 测试SFTP连接
pan-download --test-config
```

### 方法2：手动测试连接
```bash
# 使用Windows PowerShell测试SFTP连接
# 或者使用WinSCP、FileZilla等工具测试连接
```

## 📝 配置步骤

### 步骤1：编辑.env文件

打开 `.env` 文件，修改以下参数：

```env
# 1. 确认服务器地址正确
SFTP_HOST=192.168.0.122    # 你的SFTP服务器IP或域名

# 2. 确认端口（默认22，如果服务器使用其他端口需修改）
SFTP_PORT=22                # 你的SFTP端口

# 3. 确认用户名
SFTP_USERNAME=sftp01        # 你的SFTP用户名

# 4. 确认密码
SFTP_PASSWORD=123456        # 你的SFTP密码

# 5. ⭐ 重要：设置正确的远程路径
SFTP_REMOTE_PATH=/home/sftp01/uploads    # 修改为实际的上传目标目录
```

### 步骤2：验证配置

```bash
# 测试配置是否正确
pan-download --test-config
```

预期输出：
```
====================================
配置测试
====================================

1. 测试bypy配置...
✅ bypy配置正常

2. 测试SFTP配置...
✅ SFTP配置完整
✅ SFTP连接成功

====================================
🎉 所有配置检查通过！可以开始使用。
====================================
```

### 步骤3：开始使用

```bash
# 下载并上传到SFTP
pan-download 260701 --upload-sftp
```

## 🎯 常见SFTP配置场景

### 场景1：本地网络SFTP服务器
```env
SFTP_HOST=192.168.1.100
SFTP_PORT=22
SFTP_USERNAME=admin
SFTP_PASSWORD=admin123
SFTP_REMOTE_PATH=/home/admin/uploads
```

### 场景2：公网SFTP服务器
```env
SFTP_HOST=sftp.example.com
SFTP_PORT=22
SFTP_USERNAME=user
SFTP_PASSWORD=secure_password
SFTP_REMOTE_PATH=/var/uploads
```

### 场景3：非标准端口
```env
SFTP_HOST=192.168.0.122
SFTP_PORT=2222              # 自定义端口
SFTP_USERNAME=sftp01
SFTP_PASSWORD=123456
SFTP_REMOTE_PATH=/data/uploads
```

### 场景4：使用密钥认证（需要额外配置）
```env
# 注意：当前版本支持密码认证
# 如需密钥认证，需要修改代码支持
SFTP_HOST=192.168.0.122
SFTP_PORT=22
SFTP_USERNAME=sftp01
# 密钥文件路径需要在代码中配置
SFTP_REMOTE_PATH=/home/sftp01/uploads
```

## 🔍 故障排除

### 问题1：SFTP连接失败

**症状**：`--test-config` 显示SFTP连接失败

**解决方案**：
1. 检查服务器地址和端口是否正确
2. 确认服务器可达：`ping 192.168.0.122`
3. 确认端口开放：`telnet 192.168.0.122 22`
4. 验证用户名和密码
5. 检查防火墙设置

### 问题2：权限不足

**症状**：可以连接但上传失败

**解决方案**：
1. 确认用户对目标目录有写权限
2. 检查远程目录是否存在
3. 确认磁盘空间充足
4. 验证用户权限：`ls -la /remote/path`

### 问题3：路径错误

**症状**：上传到错误的位置

**解决方案**：
1. 检查 `SFTP_REMOTE_PATH` 设置
2. 确认路径是绝对路径（以 `/` 开头）
3. 测试路径：在服务器上 `ls -la /remote/path`

## 💡 高级配置

### 性能调优
```env
# 增加重试次数（网络不稳定时）
MAX_RETRIES=5

# 增加超时时间（大文件传输）
CONNECT_TIMEOUT=60
TRANSFER_TIMEOUT=600
```

### 环境分离
```env
# 开发环境
SFTP_HOST=192.168.0.122
SFTP_REMOTE_PATH=/dev/uploads

# 生产环境（需要手动切换）
# SFTP_HOST=prod.sftp.server
# SFTP_REMOTE_PATH=/prod/uploads
```

## 📋 快速检查清单

配置完成后，请确认：

- [ ] `SFTP_HOST` - 服务器地址正确
- [ ] `SFTP_PORT` - 端口号正确（默认22）
- [ ] `SFTP_USERNAME` - 用户名正确
- [ ] `SFTP_PASSWORD` - 密码正确
- [ ] `SFTP_REMOTE_PATH` - 远程路径正确 ⭐ 最重要
- [ ] 服务器可访问
- [ ] 用户有写权限
- [ ] 远程目录存在
- [ ] 通过 `--test-config` 验证

## 🎉 配置完成

配置正确后，你就可以：

```bash
# 1. 测试配置
pan-download --test-config

# 2. 下载文件
pan-download 260701

# 3. 下载并上传
pan-download 260701 --upload-sftp

# 4. 保留本地副本
pan-download 260701 --upload-sftp --keep-temp
```

---

**现在修改你的 `.env` 文件，主要是修改 `SFTP_REMOTE_PATH` 参数！**