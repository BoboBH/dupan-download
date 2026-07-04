# bypy 百度网盘 OAuth 认证指南

## 授权链接
```
https://openapi.baidu.com/oauth/2.0/authorize?client_id=q8WE4EpCsau1oS0MplgMKNBn&response_type=code&redirect_uri=oob&scope=basic+netdisk
```

## 认证步骤

### 方法 1：使用认证脚本（推荐）

1. 在浏览器中打开上面的授权链接
2. 登录您的百度账号并点击"授权"
3. 复制页面显示的授权码
4. 将授权码保存到文件 `auth_code.txt`（放在项目根目录）
5. 运行认证脚本：
   ```bash
   python bypy_manual_auth.py
   ```

### 方法 2：手动交互式认证

1. 打开 PowerShell 或 CMD
2. 激活虚拟环境：
   ```bash
   .venv\Scripts\activate
   ```
3. 运行认证命令：
   ```bash
   .venv\Scripts\bypy.exe quota
   ```
4. 浏览器中会自动打开授权链接（或手动打开上面的链接）
5. 完成授权后复制授权码
6. 粘贴授权码到命令行并按回车

### 方法 3：修改 bypy 源代码（临时方案）

如果以上方法都失败，可以临时修改 bypy 源代码：

1. 打开文件：`.venv\Lib\site-packages\bypy\bypy.py`
2. 找到第 1058 行左右的代码：
   ```python
   auth_code = ask(msg).strip()
   ```
3. 将其修改为：
   ```python
   # auth_code = ask(msg).strip()
   auth_code = "YOUR_AUTH_CODE_HERE"  # 粘贴您的授权码
   ```
4. 保存文件后运行：
   ```bash
   .venv\Scripts\bypy.exe quota
   ```

## 验证认证

认证成功后，运行以下命令验证：

```bash
# 查看配额信息
.venv\Scripts\bypy.exe quota

# 列出网盘文件
.venv\Scripts\bypy.exe list

# 查看用户信息
.venv\Scripts\bypy.exe whoami
```

## 常见问题

### Q: 授权链接打不开怎么办？
A: 可能是网络问题，请确保能够访问百度服务。

### Q: 授权码在哪里？
A: 完成授权后，页面会显示一个授权码，通常是一串较长的字符串。

### Q: 授权码有时效性吗？
A: 是的，授权码在 10 分钟内有效，请尽快完成认证。

### Q: 认证失败怎么办？
A: 请检查：
1. 授权码是否复制完整
2. 网络连接是否正常
3. 百度账号是否正常

### Q: 如何重新认证？
A: 运行以下命令清除旧的认证信息：
```bash
.venv\Scripts\bypy.exe -c
.venv\Scripts\bypy.exe quota
```

## 配置文件位置

认证成功后，配置信息保存在：
```
C:\Users\bobo\.bypy\bypy.setting.json
```

## 完成认证后的常用命令

```bash
# 列出根目录文件
.venv\Scripts\bypy.exe list

# 上传文件
.venv\Scripts\bypy.exe upload localfile remotefile

# 下载文件
.venv\Scripts\bypy.exe download remotefile localfile

# 同步目录
.venv\Scripts\bypy.exe syncdown remotedir localdir
.venv\Scripts\bypy.exe syncup localdir remotedir
```
