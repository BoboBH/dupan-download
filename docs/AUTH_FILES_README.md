# 认证文件说明

## 🎯 回答你的问题：settings.json 中的 token 是怎么生成的？

### 简短答案：
**token 是 bypy 自动生成的，你不需要手动创建！**

## 🚀 最简单的方法

### 在任意一台有 Python 的电脑上：

```bash
# 1. 安装 bypy
pip install bypy

# 2. 运行认证（会自动打开浏览器）
bypy info

# 3. 在浏览器中完成授权
#    - 登录百度账号
#    - 点击授权按钮
#    - 完成！

# 4. 验证认证
bypy quota
```

**就这么简单！** bypy 会自动在 `~/.bypy/` 目录下生成所有认证文件，包括：
- `settings.json`（包含 token）
- `token.json`
- `cookie.json`
- 等其他必要文件

## 📁 然后将认证文件复制到目标机器

### Windows
```bash
# 源机器（已认证）
源目录: C:\Users\YourName\.bypy\

# 目标机器
目标目录: C:\Users\TargetName\.bypy\

# 操作：
# 1. 在目标机创建目录
mkdir C:\Users\TargetName\.bypy

# 2. 复制整个 .bypy 目录的内容
#    复制源机器的所有文件到目标机
```

### Linux/Mac
```bash
# 源机器（已认证）
源目录: ~/.bypy/

# 目标机器
目标目录: ~/.bypy/

# 操作：
scp -r ~/.bypy/ user@target-machine:~/
```

## 🔍 关于 settings.json 和 token

### settings.json 文件结构
```json
{
    "appid": "266719",
    "webapp": "0",
    "auto": "1",
    "bduss": "你的百度会话信息",
    "token": "自动生成的访问令牌",
    "refresh_token": "自动生成的刷新令牌"
}
```

### Token 生成过程
1. **你运行** `bypy info`
2. **bypy 打开** 浏览器 → 百度 OAuth 页面
3. **你授权** 应用访问你的网盘
4. **百度返回** 授权码给 bypy
5. **bypy 使用** 授权码向百度服务器请求 token
6. **百度返回** access_token 和 refresh_token
7. **bypy 保存** 到 settings.json 文件

**全程自动！你只需要点击授权按钮。**

## ⚠️ 重要提醒

### ✅ 推荐做法
- **使用自动认证**：`bypy info` 最简单最安全
- **定期重新认证**：token 有有效期，建议定期更新
- **妥善保管**：认证文件包含你的账号权限

### ❌ 不推荐做法
- **手动创建** settings.json
- **编辑** token 字段
- **分享** 认证文件给他人
- **从不可信来源** 获取认证文件

## 🛠️ 故障排除

### 问题：token 过期
**解决**：重新运行 `bypy info`

### 问题：认证失败
**解决**：
1. 删除 `.bypy` 目录
2. 重新运行 `bypy info`

### 问题：无法打开浏览器
**解决**：
1. 检查默认浏览器设置
2. 手动访问显示的授权URL

## 📚 完整指南

详细认证指南请查看：**[BYPY_AUTH_GUIDE.md](BYPY_AUTH_GUIDE.md)**

## 🎯 总结

**你不需要手动生成 token！**

只需运行：
```bash
bypy info
```

然后在浏览器中完成授权，bypy 会自动生成所有必要的认证文件。

---

**记住**：settings.json 和其中的 token 都是 bypy 自动管理，你只需要运行认证命令！