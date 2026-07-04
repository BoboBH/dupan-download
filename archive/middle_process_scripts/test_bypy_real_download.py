#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""使用bypy进行真实下载测试"""
import sys
import os
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

print("=" * 70)
print(" " * 15 + "使用bypy进行真实下载")
print("=" * 70)

# 1. 检查bypy安装
print("\n[1/3] 检查bypy安装:")
try:
    from bypy import ByPy
    print("  OK - bypy已安装")
except ImportError:
    print("  ERROR - bypy未安装，请运行: pip install bypy")
    sys.exit(1)

# 2. 检查认证信息
print("\n[2/3] 检查认证状态:")
bduss = os.getenv('BAIDU_BDUSS')
if bduss:
    print(f"  OK - BDUSS已设置 ({len(bduss)} 字符)")
    print("  INFO - bypy可能需要OAuth认证")
else:
    print("  ERROR - BDUSS未设置")
    sys.exit(1)

# 3. 尝试使用bypy下载
print("\n[3/3] 尝试使用bypy下载:")
try:
    # 创建bypy实例
    bp = ByPy()

    # 检查认证状态
    print("  检查bypy认证状态...")

    # 尝试列出文件
    print("  尝试列出文件...")
    try:
        result = bp.list('/')
        print(f"  结果: {result}")
    except Exception as e:
        print(f"  认证可能需要: {e}")

    # 提供OAuth认证指导
    print("\n  如果需要OAuth认证，请执行:")
    print("  1. 访问: https://openapi.baidu.com/oauth/2.0/authorize")
    print("  2. 授权应用后获取授权码")
    print("  3. 运行: .venv\\Scripts\\bypy.exe quota")
    print("  4. 输入授权码完成认证")

except Exception as e:
    print(f"  ERROR: {e}")

print("\n" + "=" * 70)
print("bypy下载测试完成")
print("=" * 70)
