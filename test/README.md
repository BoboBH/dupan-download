# 测试脚本目录

此目录包含项目的各种测试脚本。

## 测试脚本分类

### 1. 集成测试
- `test_real_download.py` - 测试真实下载功能
- `test_share_link.py` - 测试分享链接下载

### 2. 单元测试
- `unit/` - 单元测试脚本
- `integration/` - 集成测试脚本

### 3. 性能测试
- `performance/` - 性能测试脚本

## 使用方法

```bash
# 运行集成测试
python test/test_real_download.py

# 运行单元测试
pytest tests/ -v
```
