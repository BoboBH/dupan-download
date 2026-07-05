# 项目开发规则

本文档定义了本项目的基本开发规则和标准，确保代码质量和项目一致性。

## 🎯 核心原则

1. **质量优先**：代码质量和可维护性优先于开发速度
2. **测试驱动**：所有新功能必须有相应的测试
3. **文档同步**：代码变更必须同步更新文档
4. **系统性调试**：遇到问题必须使用系统性调试方法

## 📁 项目结构规则

### 测试文件规则

**重要规则：所有测试代码必须写入到 `tests/` 目录**

```
tests/
├── test_config.py              # 配置测试
├── test_downloader.py          # 下载测试
├── test_uploader.py            # 上传测试
├── test_utils.py               # 工具函数测试
├── test_cli.py                 # 命令行接口测试
├── test_integration.py         # 集成测试
├── test_filename_sanitization.py  # 文件名清理测试
└── test_long_filename.py       # 长文件名测试
```

**规则详情：**
- ✅ 所有新测试文件必须放在 `tests/` 目录
- ✅ 测试文件命名必须以 `test_` 开头
- ✅ 每个功能模块必须有对应的测试文件
- ❌ 不允许在项目根目录创建测试文件
- ❌ 不允许在 `dupan_download/` 目录混入测试文件

### 源代码规则

```
dupan_download/
├── __init__.py
├── cli.py                     # 命令行接口
├── integrated_cli.py          # 整合CLI
├── config.py                  # 配置管理
├── downloader.py              # 下载模块
├── uploader.py                # 上传模块
├── utils.py                   # 工具函数
├── streaming_processor.py     # 流式处理器
├── share_downloader.py        # 分享链接下载
└── transfer.py                # 转存模块
```

**规则详情：**
- ✅ 功能代码必须放在 `dupan_download/` 目录
- ✅ 每个模块文件应该有单一明确的职责
- ✅ 使用清晰的模块命名
- ❌ 不允许创建功能不明的工具文件

### 文档规则

```
docs/
├── development/               # 开发文档
│   ├── project/              # 项目管理
│   ├── testing/              # 测试文档
│   └── features/             # 功能说明
├── guides/                   # 用户指南
├── deployment/               # 部署文档
└── reports/                  # 技术报告
```

## 🔧 开发流程规则

### 1. 功能开发流程

```bash
# 1. 创建功能分支
git checkout -b feature/your-feature-name

# 2. 编写功能代码
# 在 dupan_download/ 中编写功能

# 3. 编写测试代码
# 在 tests/ 中编写测试文件

# 4. 更新文档
# 在 docs/ 中更新相关文档

# 5. 运行测试验证
pytest tests/ -v

# 6. 提交代码
git add .
git commit -m "feat: add your feature description"
```

### 2. 调试修复流程

当遇到bug或问题时，必须使用系统性调试方法：

**Phase 1: 根本原因调查**
- 重现问题
- 收集错误信息
- 分析根本原因

**Phase 2: 模式分析**
- 找到工作示例
- 对比差异
- 识别问题模式

**Phase 3: 假设测试**
- 形成单一假设
- 最小化测试
- 验证假设

**Phase 4: 实施修复**
- 创建失败测试
- 实施单一修复
- 验证修复效果

### 3. 测试编写规则

**基本要求：**
- ✅ 所有测试文件必须放在 `tests/` 目录
- ✅ 测试函数必须以 `test_` 开头
- ✅ 使用描述性的测试名称
- ✅ 每个测试应该独立运行
- ✅ 包含正常和异常情况测试

**测试结构：**
```python
def test_feature_normal_case():
    """测试功能的正常情况"""
    # Arrange
    input_data = setup_test_data()
    
    # Act
    result = function_to_test(input_data)
    
    # Assert
    assert result.success == True
    assert result.value == expected_value

def test_feature_edge_case():
    """测试功能的边界情况"""
    # Test edge cases
    pass

def test_feature_error_case():
    """测试功能的错误处理"""
    # Test error handling
    pass
```

## 📝 代码规范

### Python代码规范

**基本规则：**
- 遵循 PEP 8 风格指南
- 使用有意义的变量和函数名
- 添加必要的注释和文档字符串
- 保持函数简短专注（< 50行）
- 避免深层嵌套（< 4层）

**文档字符串：**
```python
def function_name(param1: str, param2: int) -> bool:
    """
    函数简短描述
    
    Args:
        param1: 参数1描述
        param2: 参数2描述
    
    Returns:
        返回值描述
    
    Examples:
        >>> function_name("test", 123)
        True
    """
    pass
```

### 错误处理规范

**基本规则：**
- ✅ 使用具体的异常类型
- ✅ 提供详细的错误信息
- ✅ 在适当的地方捕获异常
- ✅ 记录异常日志
- ❌ 不使用裸except捕获所有异常

**错误处理模板：**
```python
try:
    # 操作代码
    result = perform_operation()
except SpecificException as e:
    logger.error(f"操作失败: {e}")
    return Result(success=False, error=str(e))
except Exception as e:
    logger.error(f"未预期的错误: {e}")
    raise
```

## 🧪 测试规范

### 单元测试

**要求：**
- ✅ 每个功能模块必须有单元测试
- ✅ 测试覆盖率目标：> 80%
- ✅ 包含正常、边界和错误情况
- ✅ 使用mock避免外部依赖

### 集成测试

**要求：**
- ✅ 测试模块间交互
- ✅ 测试完整工作流程
- ✅ 使用测试环境配置
- ✅ 清理测试数据

### 测试执行

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/test_utils.py -v

# 运行特定测试函数
pytest tests/test_utils.py::test_sanitize_filename -v

# 查看测试覆盖率
pytest tests/ --cov=dupan_download --cov-report=html
```

## 📚 文档规范

### 代码文档

**要求：**
- ✅ 所有公共函数必须有文档字符串
- ✅ 复杂逻辑必须有注释说明
- ✅ 模块级别必须有功能说明
- ✅ 重要算法必须有实现说明

### 用户文档

**要求：**
- ✅ 功能说明必须清晰易懂
- ✅ 包含使用示例
- ✅ 说明配置要求
- ✅ 提供故障排除指南

### 开发文档

**要求：**
- ✅ 记录重要决策和原因
- ✅ 维护API文档
- ✅ 更新架构设计文档
- ✅ 记录已知问题和限制

## 🚀 发布流程

### 版本发布步骤

```bash
# 1. 更新版本号
# 修改 setup.py 或 pyproject.toml 中的版本号

# 2. 更新CHANGELOG.md
# 记录新功能、修复和变更

# 3. 运行完整测试
pytest tests/ -v

# 4. 创建发布包
cd setup
create_release.bat

# 5. 测试发布包
dist\pan-download.exe --test-config

# 6. 提交发布
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 发布检查清单

- [ ] 所有测试通过
- [ ] 文档已更新
- [ ] 版本号已更新
- [ ] CHANGELOG已更新
- [ ] 发布包已测试
- [ ] 已备份重要数据

## 🎯 质量标准

### 代码质量指标

- **测试覆盖率**：> 80%
- **代码复杂度**：平均圈复杂度 < 10
- **代码重复率**：< 5%
- **文档完整性**：> 90%

### 性能标准

- **启动时间**：< 3秒
- **下载速度**：> 1MB/s（网络允许）
- **上传速度**：> 500KB/s（网络允许）
- **内存使用**：< 200MB（正常操作）

### 可靠性标准

- **错误处理**：所有已知错误都有处理
- **日志记录**：关键操作都有日志
- **配置验证**：启动时验证配置
- **资源清理**：正确释放资源

## 🔒 安全规范

### 敏感信息处理

- ❌ 不在代码中硬编码密码
- ❌ 不将敏感信息提交到版本控制
- ✅ 使用环境变量存储配置
- ✅ .env文件加入.gitignore

### 输入验证

- ✅ 验证所有用户输入
- ✅ 清理文件名和路径
- ✅ 限制资源使用
- ✅ 防止路径遍历攻击

## 📊 监控和维护

### 日志规范

- ✅ 使用统一的日志格式
- ✅ 记录重要操作和错误
- ✅ 避免记录敏感信息
- ✅ 使用适当的日志级别

### 问题跟踪

- ✅ 记录所有已知问题
- ✅ 分类问题严重程度
- ✅ 制定修复计划
- ✅ 验证修复效果

---

## 🎓 学习资源

### 推荐阅读

- **系统性调试**：参考项目中的调试指南
- **Python最佳实践**：PEP 8风格指南
- **测试驱动开发**：TDD方法论
- **文档写作**：技术文档写作指南

### 项目特定指南

- **[调试方法](../superpowers/README.md)** - 系统性调试方法
- **[测试指南](testing/README.md)** - 测试策略和工具
- **[打包发布](../deployment/packaging/release.md)** - 打包发布流程

---

*本文档是活的文档，随项目发展持续更新*

*最后更新：2026-07-05*