# bypy 认证文件结构详解

## 文件位置和结构

### 目录位置

**Linux/Mac:** `~/.bypy/`
**Windows:** `C:\Users\<用户名>\.bypy\`

### 文件列表

```
~/.bypy/
├── bypy.json              # OAuth 认证令牌（最重要）
├── bypy.setting.json      # 程序设置（自动生成）
├── bypy.hashcache.json    # 文件哈希缓存（自动生成）
├── bypy.parts.json        # 上传进度（上传时生成）
└── bypy.pickle            # 旧版缓存（可能不存在）
```

## 各文件详解

### 1. bypy.json（认证令牌文件）⭐

**作用：** 存储 OAuth 认证令牌
**重要性：** ⭐⭐⭐⭐⭐（必需，没有则无法使用）
**创建时机：** 运行认证向导时

**文件内容示例：**
```json
{
  "access_token": "121.0b9afdb6ab722375df272f820fe3ecd8...",
  "expires_in": 2592000,
  "refresh_token": "122.cdd799b17209ee296a98f72b3f6d82ce...",
  "scope": "basic netdisk",
  "session_key": "",
  "session_secret": ""
}
```

**如何创建：**
```bash
# 方法一：使用本程序的向导
pan-download.exe --setup-bypy

# 方法二：使用 bypy 命令（需要 Python 环境）
bypy info
```

### 2. bypy.setting.json（设置文件）

**作用：** 存储程序设置信息
**重要性：** ⭐⭐（可选，程序会自动创建）
**创建时机：** 第一次运行时自动创建

**文件内容示例：**
```json
{
  "lastUpdateCheck": 1782979827
}
```

**特点：**
- 如果不存在，程序会使用默认设置
- 在程序退出时自动保存
- 通常不需要手动编辑

### 3. bypy.hashcache.json（哈希缓存）

**作用：** 缓存已下载文件的哈希值
**重要性：** ⭐（可选，性能优化）
**创建时机：** 下载文件时自动创建

**特点：**
- 用于避免重复下载相同文件
- 可以安全删除（会影响性能）
- 程序会自动重建

### 4. bypy.parts.json（上传进度）

**作用：** 存储分片上传的进度
**重要性：** ⭐（可选，仅上传时需要）
**创建时机：** 上传大文件时创建

**特点：**
- 用于断点续传
- 上传完成后可删除

## 认证流程详解

### 完整认证过程

#### 阶段 1：首次运行（无认证文件）

```bash
# 用户运行程序
pan-download.exe apps/bypy/test_folder

# 程序检查 ~/.bypy/bypy.json
# 文件不存在 → 提示用户认证
```

**程序行为：**
- 检查 `~/.bypy/` 目录
- 检查 `bypy.json` 文件
- 如果不存在，显示错误：`"未找到认证文件，请运行 --setup-bypy"`

#### 阶段 2：认证向导

```bash
# 用户运行认证向导
pan-download.exe --setup-bypy
```

**程序行为：**
1. **创建 `~/.bypy/` 目录**（如果不存在）
2. **显示认证说明**
3. **等待用户完成 OAuth 认证**

#### 阶段 3：OAuth 认证（外部）

**方式一：在目标机器上直接认证**
```bash
# 程序会提示访问网址
# 用户在浏览器中完成授权
# 程序自动保存认证令牌到 bypy.json
```

**方式二：在已有 Python 的机器上认证**
```bash
# 在有 Python 的机器上
pip install bypy
bypy info
# 按提示完成认证

# 复制认证文件到目标机器
# 从：~/.bypy/
# 到：目标机器的 ~/.bypy/
```

#### 阶段 4：认证成功

```bash
# 程序检查认证文件
pan-download.exe --test-config

# 输出：
# ✅ bypy 认证验证成功
# ✅ 配额信息：已用空间 / 总空间
```

**创建的文件：**
- ✅ `~/.bypy/bypy.json`（认证令牌）
- ✅ `~/.bypy/bypy.setting.json`（设置文件，自动创建）

## 部署时的认证处理

### 情况一：个人使用（已有认证）

**如果已经在当前机器认证过：**

```bash
# 认证文件已存在
$ ls ~/.bypy/
bypy.json              # 认证令牌
bypy.setting.json      # 设置文件
bypy.hashcache.json    # 缓存文件

# 直接使用即可
pan-download.exe apps/bypy/test_folder --keep-temp
```

### 情况二：分发部署（无认证）

**在目标机器上首次使用时：**

```bash
# 1. 解压部署包
解压到：C:\Program Files\dupan-download\

# 2. 运行程序
pan-download.exe apps/bypy/test_folder

# 3. 程序提示需要认证
# "未找到认证文件，请运行 --setup-bypy"

# 4. 运行认证向导
pan-download.exe --setup-bypy

# 5. 完成认证后即可使用
```

### 情况三：批量部署（预配置认证）

**如果要在多台机器上部署：**

**方案一：每台机器单独认证**
```bash
# 每台机器运行
pan-download.exe --setup-bypy
```

**方案二：共享认证令牌（不推荐）**
```bash
# 在一台机器上认证
pan-download.exe --setup-bypy

# 复制认证文件
# 从：~/.bypy/bypy.json
# 到：其他机器的 ~/.bypy/bypy.json

# ⚠️ 注意：共享认证令牌可能有安全风险
```

## 文件创建时机总结

### 自动创建的文件

| 文件 | 创建时机 | 必需性 | 备注 |
|------|---------|--------|------|
| `~/.bypy/` 目录 | 首次运行 | 自动 | 如果不存在会创建 |
| `bypy.setting.json` | 首次运行 | 自动 | 程序退出时保存 |
| `bypy.hashcache.json` | 下载文件时 | 自动 | 性能优化 |
| `bypy.parts.json` | 上传文件时 | 自动 | 断点续传 |

### 需要手动创建的文件

| 文件 | 创建时机 | 必需性 | 备注 |
|------|---------|--------|------|
| **`bypy.json`** | **运行认证向导** | **必需** | **没有则无法使用** |

## 部署建议

### 对于个人使用

1. **在开发机器上完成认证**
   ```bash
   pan-download.exe --setup-bypy
   ```

2. **直接使用 D:\baidu-download**
   - 认证文件已存在
   - 无需重新配置

### 对于分发部署

1. **不包含认证文件**（安全考虑）
   - ZIP 包中不包含 `~/.bypy/` 目录
   - 不包含 `bypy.json`

2. **目标机器首次使用时**
   - 运行 `快速开始.bat`
   - 程序会提示认证
   - 完成认证后即可使用

3. **提供清晰的认证说明**
   - 在文档中说明认证步骤
   - 提供认证向导脚本

## 故障排除

### 问题：认证文件不存在

**症状：**
```
FileNotFoundError: [Errno 2] No such file or directory: '.../.bypy/bypy.json'
```

**解决方案：**
```bash
# 运行认证向导
pan-download.exe --setup-bypy
```

### 问题：认证过期

**症状：**
```
认证验证失败: Token expired
```

**解决方案：**
```bash
# 重新认证
pan-download.exe --setup-bypy
```

### 问题：权限错误

**症状：**
```
PermissionError: [Errno 13] Permission denied: '.bypy'
```

**解决方案：**
```bash
# 检查目录权限
# 或以管理员身份运行
```

## 总结

### 关键点

1. **`bypy.json` 是唯一必需的认证文件**
   - 必须通过认证向导创建
   - 包含 OAuth 认证令牌
   - 不会自动创建

2. **其他文件都会自动创建**
   - `bypy.setting.json`：程序退出时保存
   - `bypy.hashcache.json`：下载时创建
   - `bypy.parts.json`：上传时创建

3. **部署时不需要包含认证文件**
   - 出于安全考虑
   - 目标机器首次使用时认证
   - 认证是一次性的过程

### 用户操作流程

```
首次使用 → 运行 --setup-bypy → 完成 OAuth 认证 → bypy.json 创建 → 可以使用
   ↑
只需一次，之后自动使用已保存的认证
```

---

**文档版本：** 1.0
**最后更新：** 2026-07-03
**适用版本：** bypy 1.8.9
