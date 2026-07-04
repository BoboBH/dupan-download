# 文档整理计划

## 📁 当前文档分析

### 根目录文档（需要整理）
- `README.md` - 保持根目录（项目主页）
- `CONFIG_CLEAN.md` - 配置说明
- `DEPLOYMENT_GUIDE.md` - 部署指南
- `NO_PYTHON_DEPLOYMENT.md` - 无Python部署指南
- `PROJECT_STATUS.md` - 项目状态
- `QUICK_SUMMARY.md` - 快速总结
- `RELEASE_GUIDE.md` - 发布指南
- `SFTP_CONFIG_GUIDE.md` - SFTP配置指南
- `SFTP_UPLOAD_FIX.md` - SFTP上传修复说明
- `SOLUTION_COMPLETE.md` - 解决方案完整说明
- `TEMP_FILES_GUIDE.md` - 临时文件指南
- `TEST_PLAN.md` - 测试计划
- `USAGE_GUIDE.md` - 使用指南

### 现有docs目录
- `docs/SETUP_GUIDE.md` - 设置指南
- `docs/superpowers/` - 设计和规划文档

## 🗂️ 新的文档结构

```
docs/
├── guides/              # 用户指南
│   ├── usage/          # 使用指南
│   ├── config/         # 配置指南
│   └── troubleshooting/ # 故障排除
├── deployment/         # 部署相关
│   ├── installation/   # 安装指南
│   ├── packaging/      # 打包发布
│   └── no-python/      # 无Python部署
├── development/        # 开发相关
│   ├── testing/        # 测试
│   ├── project/        # 项目管理
│   └── features/       # 功能开发
├── reference/         # 参考文档
│   ├── api/           # API参考
│   ├── commands/      # 命令参考
│   └── config/        # 配置参考
└── archive/           # 归档文档
```

## 📋 文档分类映射

### guides/ - 用户指南
- `USAGE_GUIDE.md` → `guides/usage/README.md`
- `TEMP_FILES_GUIDE.md` → `guides/usage/temp-files.md`
- `SFTP_CONFIG_GUIDE.md` → `guides/config/sftp.md`
- `CONFIG_CLEAN.md` → `guides/config/overview.md`

### deployment/ - 部署相关
- `DEPLOYMENT_GUIDE.md` → `deployment/installation/README.md`
- `NO_PYTHON_DEPLOYMENT.md` → `deployment/no-python/README.md`
- `RELEASE_GUIDE.md` → `deployment/packaging/release.md`
- `SETUP_GUIDE.md` → `deployment/installation/setup.md`

### development/ - 开发相关
- `TEST_PLAN.md` → `development/testing/README.md`
- `PROJECT_STATUS.md` → `development/project/status.md`
- `SFTP_UPLOAD_FIX.md` → `development/features/sftp-upload.md`

### reference/ - 参考文档
- `QUICK_SUMMARY.md` → `reference/quick-start.md`
- `SOLUTION_COMPLETE.md` → `reference/solution.md`
- 新建 `reference/commands.md` - 命令参考
- 新建 `reference/config.md` - 配置参数参考

### 根目录保持
- `README.md` - 保持（项目主页）

## 🚀 执行步骤

1. 创建新的目录结构
2. 移动现有文档
3. 创建文档索引
4. 更新README中的链接
5. 创建docs/README.md导航

## 📝 新建文档

- `docs/README.md` - 文档导航主页
- `docs/reference/commands.md` - 命令行参考
- `docs/reference/config.md` - 配置参数详解
- `docs/guides/troubleshooting/common-issues.md` - 常见问题解答

## 🔗 链接更新

需要更新以下文件中的链接：
- `README.md` - 主要文档链接
- 各文档之间的相互引用
- 代码注释中的文档链接