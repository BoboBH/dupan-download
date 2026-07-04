# bypy OAuth认证完整指南

## 🚀 快速认证流程

### 第一步：激活虚拟环境
```bash
cd d:\git\dupan-download
.venv\Scripts\activate
```

### 第二步：启动bypy认证
```bash
.venv\Scripts\bypy.exe quota
```

### 第三步：浏览器授权
1. 复制终端显示的授权链接
2. 在浏览器中打开链接
3. 登录你的百度账号
4. 点击"同意授权"
5. 复制显示的授权码

### 第四步：完成认证
1. 将授权码粘贴回终端
2. 按Enter确认
3. 看到成功信息即可

## 📋 详细认证过程

### 认证URL格式
```
https://openapi.baidu.com/oauth/2.0/authorize
?client_id=q8WE4EpCsau1oS0MplgMKNBn
&response_type=code
&redirect_uri=oob
&scope=basic+netdisk
```

### 预期输出示例
```
$ bypy quota
Please visit:
https://openapi.baidu.com/oauth/2.0/authorize?client_id=q8WE4EpCsau1oS0MplgMKNBn&response_type=code&redirect_uri=oob&scope=basic+netdisk

And authorize this app
Paste the authorization code here: [粘贴授权码]
Authorized successfully! Now you can use bypy commands.
```

### 认证成功后的配置文件
认证完成后，会在以下位置创建配置文件：
- Windows: `C:\Users\<用户名>\.bypy\`
- 配置文件: `bypy.setting.json`
- Token文件: `bypy.tokens.json`

## 🔍 认证问题解决

### 问题1: 授权链接无法打开
**解决**: 确保网络连接正常，尝试手动复制链接到浏览器

### 问题2: 授权码过期
**解决**: 授权码有效期为10分钟，需要在获取后立即使用

### 问题3: 认证失败
**解决**:
1. 确保使用正确的百度账号
2. 检查网络连接
3. 尝试重新认证

## 📊 认证成功验证

### 验证命令
```bash
# 查看配额信息
.venv\Scripts\bypy.exe quota

# 列出根目录文件
.venv\Scripts\bypy.exe list

# 查看帮助
.venv\Scripts\bypy.exe help
```

### 预期成功输出
```
Disk quota: 100GB used, 2TB total (5% used)
```

## 🎯 认证后使用

### 基本命令
```bash
# 列出文件
.venv\Scripts\bypy.exe list <路径>

# 下载文件
.venv\Scripts\bypy.exe download <远程路径> <本地路径>

# 上传文件
.venv\Scripts\bypy.exe upload <本地路径> <远程路径>

# 同步目录
.venv\Scripts\bypy.exe syncdown <远程路径> <本地路径>
```

## 🔐 安全说明

1. **授权范围**: 仅限basic和netdisk权限
2. **数据安全**: 认证信息存储在本地
3. **应用信息**: bypy是开源的百度网盘Python客户端

## 📞 需要帮助？

如果在认证过程中遇到问题：
1. 检查网络连接
2. 确保使用最新的bypy版本
3. 查看bypy的GitHub问题页面
4. 尝试删除认证文件重新认证

## ⏱️ 预计时间

整个认证过程大约需要2-3分钟：
1. 启动认证: 10秒
2. 浏览器授权: 30秒
3. 粘贴授权码: 10秒
4. 完成认证: 即时

认证完成后，你就可以使用bypy进行真实的百度网盘文件下载了！
