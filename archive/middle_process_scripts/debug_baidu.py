#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""调试BaiduPCS-Py初始化"""
import os
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

# 设置控制台输出编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("调试BaiduPCS-Py初始化")
print("=" * 60)

# 检查环境变量
bduss = os.getenv('BAIDU_BDUSS')
cookies = os.getenv('BAIDU_COOKIES')

print(f"\n环境变量:")
print(f"BDUSS长度: {len(bduss) if bduss else 0}")
print(f"COOKIES长度: {len(cookies) if cookies else 0}")

# 检查BaiduPCS-Py
print(f"\n导入BaiduPCS-Py:")
try:
    from baidupcs_py import BaiduPCS
    print(f"✓ 导入成功")

    # 创建实例
    print(f"\n创建BaiduPCS实例:")
    baidupcs = BaiduPCS()
    print(f"✓ 实例创建成功")
    print(f"类型: {type(baidupcs)}")

    # 查看可用方法
    print(f"\n可用方法:")
    methods = [m for m in dir(baidupcs) if not m.startswith('_')]
    for method in methods[:10]:
        print(f"  - {method}")

    # 尝试列出分享文件
    print(f"\n测试分享链接:")
    share_link = "https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg"
    extract_code = "0409"

    print(f"链接: {share_link}")
    print(f"提取码: {extract_code}")

    try:
        # 查找正确的方法
        if hasattr(baidupcs, 'listsharedpaths'):
            print(f"\n尝试使用 listsharedpaths:")
            result = baidupcs.listsharedpaths(share_link, extract_code)
            print(f"结果: {result}")
        else:
            print(f"没有 listsharedpaths 方法")

        if hasattr(baidupcs, 'list'):
            print(f"\n尝试使用 list:")
            result = baidupcs.list(share_link)
            print(f"结果: {result}")

    except Exception as e:
        print(f"调用失败: {e}")
        import traceback
        traceback.print_exc()

except ImportError as e:
    print(f"✗ 导入失败: {e}")
except Exception as e:
    print(f"✗ 创建失败: {e}")
    import traceback
    traceback.print_exc()

print(f"\n" + "=" * 60)
