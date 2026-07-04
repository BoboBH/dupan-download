#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试bypy的API和功能"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

print("=" * 70)
print(" " * 20 + "bypy API功能测试")
print("=" * 70)

# 1. 导入bypy
print("\n[1/4] 导入bypy:")
try:
    from bypy import ByPy
    print("  OK - bypy导入成功")
    bp = ByPy()
    print(f"  OK - ByPy实例创建成功: {type(bp)}")
except Exception as e:
    print(f"  ERROR - 导入失败: {e}")
    sys.exit(1)

# 2. 查看可用的方法
print("\n[2/4] 查看bypy可用的方法:")
methods = [method for method in dir(bp) if not method.startswith('_')]
print(f"  总共 {len(methods)} 个方法")
download_methods = [m for m in methods if 'download' in m.lower() or 'get' in m.lower()]
print(f"  下载相关方法: {download_methods}")

share_methods = [m for m in methods if 'share' in m.lower() or 'link' in m.lower()]
print(f"  分享相关方法: {share_methods}")

# 3. 查看特定方法的帮助
print("\n[3/4] 查看关键方法的帮助信息:")
key_methods = ['list', 'download', 'get', 'help']
for method_name in key_methods:
    if hasattr(bp, method_name):
        method = getattr(bp, method_name)
        print(f"  - {method_name}: {method.__doc__[:100] if method.__doc__ else '无文档'}...")

# 4. 尝试基本操作
print("\n[4/4] 尝试基本操作:")
try:
    # 尝试列出文件
    print("  尝试列出文件...")
    # result = bp.list('/')  # 这个可能需要认证
    # print(f"  结果: {result}")

    # 尝试帮助信息
    print("  获取帮助信息...")
    help_text = bp.help()
    if help_text:
        print(f"  帮助信息获取成功 (长度: {len(str(help_text))})")
except Exception as e:
    print(f"  操作失败: {e}")

print("\n" + "=" * 70)
print("测试完成！")
print("=" * 70)
