# 百度网盘自动下载SFTP上传工具 - 设计文档

**创建日期：** 2026-07-02
**状态：** 待审查

## 项目概述

开发一个Python命令行工具，用于自动从百度网盘下载文件夹并上传到SFTP服务器。该工具设计为手动触发，支持保持完整目录结构，并提供灵活的错误处理和配置管理。

### 核心需求
- 每天接收一个百度网盘文件夹链接和固定提取码
- 文件夹包含多个PDF文件
- 保持原始目录结构上传到SFTP
- 手动触发执行
- 下载和上传分为两个逻辑步骤

## 用户需求澄清

通过问答方式确认的关键需求：

1. **触发方式**：手动触发命令行工具
2. **目录结构**：保持网盘文件夹的完整目录结构
3. **临时文件处理**：默认清理临时文件，可通过`--keep-temp`参数保留
4. **错误处理**：跳过失败的文件继续处理，完成后提供成功/失败报告
5. **文件冲突**：直接覆盖SFTP上的同名文件

## 技术方案选择

### 方案对比
- **方案A**：基于百度网盘官方API ✅ *已选择*
- **方案B**：基于第三方爬虫库
- **方案C**：混合方案

### 选择理由
采用方案A（官方API）的原因：
1. 长期稳定性：官方API不会轻易变更
2. 账号安全：不违反服务条款，避免封号风险
3. 功能完整：支持文件夹遍历、断点续传
4. 错误处理：API提供更好的错误信息和重试机制

### 技术栈
- **Python版本**：3.8+
- **核心库**：
  - `click` - 命令行接口
  - `python-dotenv` - 环境变量管理
  - `paramiko` - SFTP连接
  - `requests` - HTTP请求
  - `tqdm` - 进度显示
  - `pytest` - 单元测试

## 项目结构

```
dupan-download/
├── dupan_download/
│   ├── __init__.py
│   ├── cli.py              # 命令行入口
│   ├── downloader.py       # 百度网盘下载逻辑
│   ├── uploader.py         # SFTP上传逻辑
│   ├── config.py           # 配置管理
│   └── utils.py            # 工具函数
├── tests/
│   ├── __init__.py
│   ├── test_downloader.py
│   ├── test_uploader.py
│   └── test_integration.py
├── .env.example            # 环境变量模板
├── .gitignore
├── requirements.txt        # 依赖包
├── setup.py               # 安装配置
└── README.md              # 使用说明
```

## 核心组件设计

### 1. CLI模块 (`cli.py`)
**职责：** 提供用户友好的命令行接口

**功能：**
- 使用`click`库定义命令和参数
- 参数验证和错误提示
- 协调下载和上传流程
- 生成执行报告

**接口定义：**
```bash
dupan-download <share_link> <extract_code> [OPTIONS]

Options:
  --keep-temp    保留临时文件，默认自动清理
  --temp-dir PATH 指定临时目录路径
  --verbose      详细输出模式
  --help         显示帮助信息
```

### 2. 下载模块 (`downloader.py`)
**职责：** 封装百度网盘API调用和文件下载逻辑

**功能：**
- 链接验证和提取码确认
- 递归遍历文件夹结构
- 保持目录结构下载到临时目录
- 断点续传支持
- 下载进度跟踪

**关键方法：**
- `validate_link(share_link, extract_code)` - 验证链接有效性
- `list_folder(path)` - 获取文件夹内容列表
- `download_file(remote_path, local_path)` - 下载单个文件
- `download_folder(remote_path, local_path)` - 递归下载文件夹

### 3. 上传模块 (`uploader.py`)
**职责：** 封装SFTP操作和文件上传逻辑

**功能：**
- 建立和管理SFTP连接
- 递归创建远程目录结构
- 文件上传（支持覆盖和断点续传）
- 连接失败重试机制

**关键方法：**
- `connect()` - 建立SFTP连接
- `create_remote_path(path)` - 递归创建远程目录
- `upload_file(local_path, remote_path)` - 上传单个文件
- `upload_folder(local_path, remote_path)` - 递归上传文件夹

### 4. 配置模块 (`config.py`)
**职责：** 管理配置加载和验证

**功能：**
- 从`.env`文件和环境变量读取配置
- 配置验证和默认值处理
- 提供配置访问接口

**配置项：**
```python
# 百度网盘API
BAIDU_APP_ID
BAIDU_APP_KEY
BAIDU_SECRET_KEY
BAIDU_ACCESS_TOKEN

# SFTP连接
SFTP_HOST
SFTP_PORT
SFTP_USERNAME
SFTP_PASSWORD
SFTP_REMOTE_PATH

# 重试配置
MAX_RETRIES = 3
CONNECT_TIMEOUT = 30
TRANSFER_TIMEOUT = 300
```

### 5. 工具模块 (`utils.py`)
**职责：** 提供通用工具函数

**功能：**
- 临时目录管理
- 路径处理和规范化
- 进度条显示
- 日志记录

## 数据流设计

### 执行流程
```
1. 用户输入命令
   └─> dupan-download <链接> <提取码> [选项]

2. CLI解析和配置加载
   ├─> 读取.env配置
   ├─> 验证必要参数
   ├─> 创建临时目录
   └─> 初始化日志和进度显示

3. 下载阶段
   ├─> 验证网盘链接和提取码
   ├─> 获取文件列表和目录结构
   ├─> 递归下载到临时目录
   ├─> 记录成功/失败文件
   └─> 显示下载进度

4. 上传阶段
   ├─> 建立SFTP连接
   ├─> 递归创建目录结构
   ├─> 上传文件（覆盖已存在文件）
   ├─> 记录成功/失败文件
   └─> 显示上传进度

5. 清理和报告
   ├─> 除非指定--keep-temp，否则删除临时目录
   ├─> 关闭所有连接
   └─> 输出执行报告
```

### 关键设计点
- **解耦设计**：下载和上传模块独立，便于测试和维护
- **状态跟踪**：每个阶段记录详细状态，支持部分失败场景
- **隔离性**：使用临时目录，不影响本地文件系统
- **可观测性**：提供进度显示和详细日志

## 错误处理策略

### 1. 网络错误处理
- **自动重试**：每个文件下载/上传失败时重试3次
- **超时控制**：连接超时30秒，传输超时5分钟
- **网络恢复**：网络中断时自动重新连接

### 2. 文件错误处理
- **非致命错误**：跳过无法访问的文件，记录到错误列表
- **继续执行**：继续处理其他文件，不中断整体流程
- **致命错误**：权限错误、磁盘空间不足等立即中止执行

### 3. API错误处理
- **友好提示**：百度网盘API调用失败时显示具体错误信息
- **诊断信息**：SFTP连接失败时提供连接参数诊断
- **输入验证**：提取码错误时明确提示用户检查

### 4. 最终报告格式
```
执行完成
✓ 成功处理: 15 个文件
✗ 失败: 2 个文件
  - folder1/large.pdf: 网络超时
  - folder2/locked.pdf: 无访问权限
```

## 配置管理

### 环境变量配置

创建`.env`文件（基于`.env.example`模板）：

```bash
# 百度网盘API配置
BAIDU_APP_ID=your_app_id
BAIDU_APP_KEY=your_app_key
BAIDU_SECRET_KEY=your_secret_key
BAIDU_ACCESS_TOKEN=your_access_token

# SFTP服务器配置
SFTP_HOST=sftp.example.com
SFTP_PORT=22
SFTP_USERNAME=your_username
SFTP_PASSWORD=your_password
SFTP_REMOTE_PATH=/remote/path

# 重试和超时配置
MAX_RETRIES=3
CONNECT_TIMEOUT=30
TRANSFER_TIMEOUT=300
```

### 配置加载优先级
1. 环境变量（最高优先级）
2. `.env`文件
3. 代码中的默认值（最低优先级）

### 配置验证
- 启动时验证必要配置项存在
- 提供友好的错误提示，指出缺失的配置
- 支持配置项类型自动转换

## 安全性考虑

### 1. 敏感信息保护
- **凭证管理**：API密钥和SFTP凭证通过环境变量传递
- **版本控制**：`.env`文件加入`.gitignore`
- **日志安全**：日志输出中自动屏蔽敏感信息

### 2. 临时文件安全
- **权限控制**：临时目录设置适当权限
- **及时清理**：执行完毕后立即清理临时文件
- **加密传输**：使用加密连接（SFTP/HTTPS）

### 3. 输入验证
- **链接格式**：验证百度网盘链接格式
- **提取码检查**：验证提取码长度和格式
- **路径安全**：防止路径遍历攻击

## 测试策略

### 单元测试
- **test_downloader.py**：测试下载模块的各种场景
- **test_uploader.py**：测试上传模块的各种场景
- **test_config.py**：测试配置加载和验证

### 集成测试
- **test_integration.py**：测试完整的下载-上传流程
- 使用Mock对象模拟外部服务

### 测试覆盖场景
- 正常下载和上传流程
- 网络错误和重试机制
- 部分文件失败场景
- 配置缺失和错误配置
- 临时文件清理验证

## 使用示例

### 典型使用场景

```bash
# 1. 基本使用（下载并上传，完成后清理临时文件）
dupan-download https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg 0409

# 2. 保留临时文件用于调试
dupan-download https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg 0409 --keep-temp

# 3. 指定临时目录
dupan-download https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg 0409 --temp-dir "D:/temp"

# 4. 详细输出模式
dupan-download https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg 0409 --verbose
```

### 预期输出示例

```
$ dupan-download https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg 0409

✓ 验证链接成功
✓ 发现文件夹: 共享文档 (18 个文件)
✓ 下载中: [######################] 100% 18/18
✓ 上传中: [######################] 100% 18/18
✓ 清理临时文件

执行完成
✓ 成功处理: 18 个文件
✗ 失败: 0 个文件
```

## 实施注意事项

### 百度网盘API集成
- 需要申请百度网盘开放平台账号
- 获取应用凭证（APP_ID, APP_KEY, SECRET_KEY）
- 处理OAuth认证流程获取ACCESS_TOKEN
- 参考官方文档：https://pan.baidu.com/union/doc/0ksg0sbig

### SFTP连接优化
- 使用SSH密钥认证（可选，更安全）
- 实现连接池重用机制
- 大文件分块上传避免内存溢出

### 性能考虑
- 支持并发下载/上传（可选的优化点）
- 大文件进度显示更新频率控制
- 临时文件使用磁盘空间监控

## 依赖包版本

```
click>=8.0.0
python-dotenv>=0.19.0
paramiko>=2.11.0
requests>=2.27.0
tqdm>=4.62.0
pytest>=7.0.0
```

## 环境要求

- **Python版本**：3.8+
- **操作系统**：Windows 10+, Linux, macOS
- **网络要求**：能够访问百度网盘API和SFTP服务器
- **磁盘空间**：临时目录需要足够空间存储下载文件

## 项目里程碑

1. **阶段一**：基础框架搭建
   - 项目结构创建
   - 配置管理实现
   - CLI基础接口

2. **阶段二**：核心功能实现
   - 百度网盘下载模块
   - SFTP上传模块
   - 错误处理机制

3. **阶段三**：测试和优化
   - 单元测试编写
   - 集成测试验证
   - 性能优化

4. **阶段四**：文档和部署
   - 使用文档完善
   - 安装配置说明
   - 示例和最佳实践
