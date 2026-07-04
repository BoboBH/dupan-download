# 部署相关文档

部署相关文档涵盖了安装、打包、发布和各种部署场景的详细指南。

## 📚 文档列表

### 安装指南
- **[部署指南](installation/README.md)** - 完整的部署步骤和配置
- **[设置指南](installation/setup.md)** - 开发环境设置

### 打包发布
- **[发布指南](packaging/release.md)** - 创建发布包和版本管理
- **[测试计划](../development/testing/README.md)** - 发布前测试验证

### 无Python部署
- **[无依赖部署](no-python/README.md)** - 在没有Python环境的目标机器上部署

## 🎯 按场景查找

### 我想...
- **在生产环境部署** → [部署指南](installation/README.md)
- **创建发布包** → [发布指南](packaging/release.md)
- **部署到无Python环境** → [无依赖部署](no-python/README.md)
- **设置开发环境** → [设置指南](installation/setup.md)

## 🚀 部署场景

### 场景1：开发机部署
```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境
python setup.py install
```
详见：[设置指南](installation/setup.md)

### 场景2：生产环境部署（有Python）
```bash
# 使用标准部署流程
# 详见部署指南
```
详见：[部署指南](installation/README.md)

### 场景3：无Python环境部署
```bash
# 创建发布包
create_release.bat

# 目标机运行
install.bat
```
详见：[无依赖部署](no-python/README.md)

## 📋 部署检查清单

### 部署前准备
- [ ] 确认系统要求
- [ ] 准备配置文件
- [ ] 检查网络连接
- [ ] 验证依赖项

### 部署步骤
- [ ] 安装程序
- [ ] 配置环境变量
- [ ] 设置认证信息
- [ ] 测试配置

### 部署后验证
- [ ] 运行配置测试
- [ ] 测试基本功能
- [ ] 验证SFTP连接
- [ ] 检查日志输出

## 🔗 相关文档

- **[用户指南](../guides/README.md)** - 使用说明
- **[项目状态](../development/project/status.md)** - 开发进度
- **[测试计划](../development/testing/README.md)** - 测试策略

---

返回：[文档中心](../README.md) | [项目主页](../../README.md)