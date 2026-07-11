# 百度网盘PDF文件自动传输系统设计文档

**项目名称**: baidu-download  
**设计日期**: 2026-07-11  
**设计类型**: 模块化架构  
**版本**: 1.0

---

## 1. 项目概述

### 1.1 项目背景
供应商每天通过百度网盘分享PDF文件，需要自动化处理流程：从百度网盘分享链接下载所有PDF文件，并上传到指定SFTP服务器，同时保持目录结构不变。

### 1.2 核心需求
- 自动下载百度网盘分享链接中的所有PDF文件
- 上传到指定SFTP服务器
- 记录详细的文件传输日志到MySQL数据库
- 支持Windows 11环境，打包为免安装exe程序
- 提供完整的测试用例

### 1.3 关键约束
- 使用Python 3.8实现
- 使用BaiduPCS-Go作为百度网盘下载工具
- 必须支持失败跳过，不中断整体流程
- 上传成功后删除本地临时文件
- 详细的审计日志记录

---

## 2. 架构设计

### 2.1 项目结构

```
baidu-download/
├── src/                           # 源代码目录
│   ├── __init__.py
│   ├── config/                    # 配置管理模块
│   │   ├── __init__.py
│   │   └── settings.py           # 环境变量加载和验证
│   ├── database/                  # 数据库模块
│   │   ├── __init__.py
│   │   ├── models.py             # 数据模型定义
│   │   └── repository.py         # 数据库操作封装
│   ├── downloader/                # 下载模块
│   │   ├── __init__.py
│   │   └── baidu_client.py       # 百度网盘操作封装
│   ├── uploader/                  # 上传模块
│   │   ├── __init__.py
│   │   └── sftp_client.py        # SFTP操作封装
│   ├── processor/                 # 核心处理模块
│   │   ├── __init__.py
│   │   └── file_processor.py     # 文件处理协调器
│   └── utils/                      # 工具模块
│       ├── __init__.py
│       └── logger.py             # 日志工具
├── test/                          # 测试目录
│   ├── unit/                      # 单元测试
│   ├── integration/               # 集成测试
│   └── fixtures/                  # 测试数据
├── middle/                        # 中间验证和脚本
│   ├── db_init.sql                # 数据库初始化脚本
│   └── verify_env.py             # 环境验证脚本
├── logs/                          # 日志目录
├── temp/                          # 临时文件目录
├── main.py                        # 程序入口
├── requirements.txt               # Python依赖
├── .env.example                   # 配置模板
├── .env                           # 实际配置（不提交）
├── README.md                      # 项目文档
└── db_init.sql                    # 数据库初始化脚本
```

### 2.2 模块职责划分

#### config/settings.py
- 负责从.env文件加载所有配置
- 验证配置的完整性和正确性
- 提供配置访问接口
- 配置项包括：SFTP连接信息、MySQL连接信息、BaiduPCS-Go路径、临时目录等

#### database/models.py
- 定义数据库表结构
- 提供数据模型类
- 包含表创建逻辑

#### database/repository.py
- 封装所有数据库操作
- 提供CRUD接口
- 处理数据库连接和事务

#### downloader/baidu_client.py
- 封装BaiduPCS-Go命令行调用
- 实现登录、转存、下载等操作
- 处理百度网盘特有的错误

#### uploader/sftp_client.py
- 封装SFTP连接和文件操作
- 实现文件上传、目录创建等功能
- 处理网络错误和重试逻辑

#### processor/file_processor.py
- 核心业务逻辑协调器
- 编排完整的文件传输流程
- 处理错误状态和异常情况

#### utils/logger.py
- 提供统一的日志接口
- 支持多级别日志输出
- 同时输出到文件和终端

---

## 3. 数据流程设计

### 3.1 完整执行流程

```
用户输入：分享链接 + 提取码 + 目录名称
         ↓
1. 参数验证和配置加载
         ↓
2. 记录初始状态到数据库（pending）
         ↓
3. 百度网盘操作
   - 检查是否存在同名目录 → 删除
   - 转存分享链接到网盘目录
   - 获取PDF文件列表
         ↓
4. 文件处理循环（每个PDF文件）
   ├─ 记录状态：downloading
   ├─ 下载到本地临时目录
   ├─ 记录状态：uploading  
   ├─ 上传到SFTP服务器
   ├─ 记录状态：success
   ├─ 删除本地临时文件
   └─ 如果失败：记录错误，跳过继续
         ↓
5. 生成处理报告
         ↓
6. 清理临时目录
         ↓
输出：处理报告 + 详细日志
```

### 3.2 数据流转图

```
分享链接 → 百度网盘 → 本地临时 → SFTP服务器
              ↓              ↓
         文件列表      临时文件
              ↓              ↓
         数据库记录 ←  删除文件
```

### 3.3 状态机设计

文件传输状态转换：
```
pending → downloading → uploading → success
                    ↓                   ↓
                  failed              skipped
```

---

## 4. 数据库设计

### 4.1 数据库配置

```sql
数据库名称: baidu_download
字符集: utf8mb4
排序规则: utf8mb4_unicode_ci
```

### 4.2 表结构设计

#### file_transfer_log - 文件传输记录表

```sql
CREATE TABLE file_transfer_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    share_link VARCHAR(500) NOT NULL COMMENT '分享链接',
    extraction_code VARCHAR(20) NOT NULL COMMENT '提取码',
    folder_name VARCHAR(255) NOT NULL COMMENT '目录名称',
    file_name VARCHAR(255) NOT NULL COMMENT '文件名',
    file_path VARCHAR(500) COMMENT '文件路径',
    transfer_status ENUM('pending', 'downloading', 'uploading', 'success', 'failed', 'skipped') 
        DEFAULT 'pending' COMMENT '传输状态',
    error_message TEXT COMMENT '错误信息',
    start_time DATETIME COMMENT '开始时间',
    download_time DATETIME COMMENT '下载完成时间',
    upload_time DATETIME COMMENT '上传完成时间',
    file_size BIGINT COMMENT '文件大小(字节)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
    
    INDEX idx_share_link (share_link(255)),
    INDEX idx_folder_name (folder_name),
    INDEX idx_status (transfer_status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='文件传输记录表';
```

#### execution_summary - 执行摘要表

```sql
CREATE TABLE execution_summary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    share_link VARCHAR(500) NOT NULL,
    folder_name VARCHAR(255) NOT NULL,
    total_files INT DEFAULT 0 COMMENT '总文件数',
    success_count INT DEFAULT 0 COMMENT '成功数量',
    failed_count INT DEFAULT 0 COMMENT '失败数量',
    skipped_count INT DEFAULT 0 COMMENT '跳过数量',
    start_time DATETIME COMMENT '执行开始时间',
    end_time DATETIME COMMENT '执行结束时间',
    total_size BIGINT COMMENT '总文件大小(字节)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci 
COMMENT='执行摘要表';
```

### 4.3 索引设计

- 分享链接索引：支持按链接查询历史记录
- 目录名索引：支持按目录分组查询
- 状态索引：支持按状态筛选（失败、成功等）
- 创建时间索引：支持时间范围查询

---

## 5. 接口设计

### 5.1 命令行接口

```bash
# 基本用法
python main.py <分享链接> <提取码> <目录名称>

# 示例
python main.py "https://pan.baidu.com/s/1ir_5mHA5jNIHAstbyEZN-g" "0409" "2026-07-11-vendor"

# 完整参数
python main.py [OPTIONS]
  --link          分享链接（必需）
  --code          提取码（必需）  
  --folder        目标目录名（必需）
  --config        配置文件路径（可选，默认.env）
  --dry-run       仅测试，不实际下载和上传
  --verbose       显示详细日志
```

### 5.2 输出格式

```
[INFO] [2026-07-11 14:30:00] 开始处理文件传输任务
[INFO] [2026-07-11 14:30:00] 分享链接: https://pan.baidu.com/s/xxx
[INFO] [2026-07-11 14:30:00] 目标目录: test-vendor
[INFO] [2026-07-11 14:30:01] 正在清理百度网盘旧目录...
[INFO] [2026-07-11 14:30:02] 正在转存分享链接...
[INFO] [2026-07-11 14:30:05] 发现PDF文件: 5个
[INFO] [2026-07-11 14:30:06] 正在下载文件 (1/5): report.pdf...
[INFO] [2026-07-11 14:30:15] 下载完成: report.pdf (2.3MB)
[INFO] [2026-07-11 14:30:16] 正在上传文件 (1/5): report.pdf...
[INFO] [2026-07-11 14:30:20] 上传完成: report.pdf
[SUCCESS] [2026-07-11 14:31:00] 处理完成！成功: 5, 失败: 0
```

---

## 6. 错误处理机制

### 6.1 分层错误处理

#### Level 1: 参数验证错误
**错误类型**:
- 分享链接格式错误
- 提取码缺失
- 目录名称为空

**处理方式**: 立即终止，提示用户修正参数

#### Level 2: 配置错误
**错误类型**:
- .env文件缺失
- BaiduPCS-Go路径不存在
- SFTP/MySQL连接失败

**处理方式**: 立即终止，提示检查配置文件

#### Level 3: 文件操作错误
**错误类型**:
- 单个文件下载失败
- 单个文件上传失败
- 文件权限问题

**处理方式**: 记录错误，更新状态为failed/skipped，继续处理下一个文件

#### Level 4: 网络错误
**错误类型**:
- 网络连接超时
- SFTP连接断开

**处理方式**: 自动重试3次，仍失败则跳过

### 6.2 错误记录格式

```
[ERROR] [2026-07-11 14:30:45] 文件下载失败
文件: folder1/report.pdf
错误: Connection timeout
重试次数: 2/3
状态: skipped
```

### 6.3 处理结果报告

```markdown
处理完成！
总文件数: 10
成功: 8
失败: 2
跳过: 0
总大小: 45.6MB
总耗时: 2分30秒

失败文件列表:
1. report.pdf - 下载超时
2. summary.pdf - SFTP连接失败
```

---

## 7. 测试策略

### 7.1 测试目录结构

```
test/
├── unit/              # 单元测试
│   ├── test_config.py
│   ├── test_database.py
│   ├── test_downloader.py
│   ├── test_uploader.py
│   └── test_processor.py
├── integration/       # 集成测试
│   ├── test_full_flow.py
│   └── test_error_handling.py
└── fixtures/          # 测试数据
    ├── test_cookies.txt
    ├── test_share_links.txt
    └── mock_pdfs/
```

### 7.2 单元测试覆盖

#### config模块测试
- 配置加载测试
- 配置验证测试
- 缺失配置处理测试

#### database模块测试
- CRUD操作测试
- 状态更新测试
- 错误处理测试

#### downloader模块测试
- 命令构建测试
- 输出解析测试
- 错误识别测试

#### uploader模块测试
- SFTP连接测试
- 文件上传测试
- 重试机制测试

#### processor模块测试
- 流程控制测试
- 错误处理测试
- 文件过滤测试

### 7.3 集成测试场景

- 完整流程测试（从分享链接到SFTP上传）
- 网络错误恢复测试
- 大文件处理测试
- 并发文件处理测试
- 数据库记录完整性测试

### 7.4 Mock策略

- Mock BaiduPCS-Go命令输出
- Mock SFTP服务器响应
- Mock数据库连接
- 使用临时数据库进行集成测试

### 7.5 测试覆盖率目标

- 单元测试覆盖率 ≥ 80%
- 核心业务逻辑覆盖率 = 100%

---

## 8. 部署和打包

### 8.1 依赖管理

```
requirements.txt:
pysftp==0.2.9          # SFTP客户端
pymysql==1.1.0         # MySQL驱动
python-dotenv==1.0.0   # 环境变量管理
colorama==0.4.6        # 终端彩色输出
pytest==7.4.0          # 测试框架
pytest-mock==3.11.1    # Mock工具
```

### 8.2 打包结构

```
dist/baidu-download/
├── baidu-download.exe       # 主程序（PyInstaller打包）
├── BaiduPCS-Go.exe          # 百度网盘工具
├── .env                      # 配置文件（用户模板）
├── README.txt                # 使用说明
└── db_init.sql               # 数据库初始化脚本
```

### 8.3 打包步骤

1. 使用PyInstaller打包为单文件exe
2. 复制BaiduPCS-Go.exe到dist目录
3. 生成配置模板文件
4. 创建压缩包：`baidu-download-v1.0.zip`

### 8.4 免安装特性

- 用户无需安装Python环境
- 解压即可使用
- 首次运行自动创建必要目录
- 自动检查环境完整性

---

## 9. 配置文件设计

### 9.1 环境变量配置

```bash
# ===== 百度网盘配置 =====
BAIDUPCS_GO_PATH=D:/tools/BaiduPCS-Go-v4.0.1-windows-x64/BaiduPCS-Go.exe
BAIDU_COOKIES_PATH=./baidu-cookies.txt
TEMP_DIR=./temp

# ===== SFTP服务器配置 =====
SFTP_HOST=192.168.0.122
SFTP_PORT=22
SFTP_USERNAME=sftp01
SFTP_PASSWORD=123456
SFTP_REMOTE_PATH=/sftp01/upload

# ===== MySQL数据库配置 =====
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=123456
DB_NAME=baidu_download

# ===== 日志配置 =====
LOG_LEVEL=INFO
LOG_FILE=./logs/transfer.log

# ===== 性能配置 =====
MAX_RETRIES=3
CONCURRENT_UPLOADS=1
```

### 9.2 配置验证规则

- BaiduPCS-Go路径必须存在且可执行
- SFTP连接信息必须完整
- MySQL连接信息必须完整
- 临时目录必须可写

---

## 10. 性能和可扩展性

### 10.1 性能考虑

- 单文件处理，避免并发冲突
- 网络操作超时控制
- 内存使用优化（大文件流式处理）
- 磁盘空间管理（及时清理临时文件）

### 10.2 可扩展性设计

#### 模块化扩展点
- 支持添加新的网盘类型（只需实现新的downloader）
- 支持添加新的上传目标（只需实现新的uploader）
- 支持添加新的存储后端（只需实现新的repository）

#### 配置驱动的扩展
- 通过配置文件控制重试次数
- 通过配置文件控制日志级别
- 通过配置文件控制性能参数

---

## 11. 技术栈

### 11.1 核心技术

- **语言**: Python 3.8
- **数据库**: MySQL 5.7+
- **外部工具**: BaiduPCS-Go v4.0.1

### 11.2 Python依赖

- pysftp: SFTP客户端
- pymysql: MySQL数据库驱动
- python-dotenv: 环境变量管理
- colorama: 终端彩色输出

### 11.3 开发工具

- PyInstaller: 打包工具
- pytest: 测试框架
- git: 版本控制

---

## 12. 安全考虑

### 12.1 敏感信息保护

- 数据库密码存储在.env文件中（不提交到git）
- SFTP密码使用环境变量
- 百度网盘cookies使用独立文件

### 12.2 输入验证

- 验证分享链接格式
- 验证提取码长度
- 验证目录名称安全性（防止路径穿越）

### 12.3 错误信息处理

- 避免在错误信息中暴露敏感信息
- 错误日志记录详细但不泄露密码
- 用户界面显示友好的错误提示

---

## 13. 监控和维护

### 13.1 日志监控

- 所有操作记录到日志文件
- 错误日志单独记录
- 支持日志轮转

### 13.2 数据库监控

- 通过执行摘要表监控整体运行情况
- 通过详细记录表追踪问题
- 定期清理历史数据

### 13.3 健康检查

- 启动时检查依赖工具
- 运行时检查磁盘空间
- 定期检查网络连接

---

## 14. 实施计划

实施计划将在下一步详细制定，包括：

1. 环境搭建和依赖安装
2. 数据库初始化
3. 核心模块开发（按模块顺序）
4. 单元测试编写
5. 集成测试编写
6. 打包和部署
7. 文档完善

---

## 15. 风险和挑战

### 15.1 已识别风险

1. **BaiduPCS-Go版本兼容性**
   - 风险：命令输出格式可能变化
   - 缓解：版本固定，添加版本检查

2. **网络不稳定性**
   - 风险：下载/上传可能失败
   - 缓解：实现重试机制，失败跳过

3. **大文件处理**
   - 风险：可能占用大量磁盘空间
   - 缓解：流式处理，及时清理临时文件

4. **SFTP连接限制**
   - 风险：并发连接可能被拒绝
   - 缓解：单文件处理，控制并发

### 15.2 缓解措施

- 完善的错误处理和日志记录
- 充分的测试覆盖
- 清晰的用户文档
- 健壮的配置验证

---

## 16. 总结

这个模块化设计具有以下核心优势：

- ✅ **模块化架构**: 职责分离，易于维护和扩展
- ✅ **完整的错误处理**: 分层错误处理，确保系统稳定性
- ✅ **详细的日志记录**: 支持问题追踪和审计
- ✅ **数据库持久化**: 完整的传输历史记录
- ✅ **可测试性**: 清晰的测试策略和高的测试覆盖率
- ✅ **用户友好**: 简单的部署和打包方式

该设计满足了所有项目需求，并为未来的扩展提供了良好的基础。
