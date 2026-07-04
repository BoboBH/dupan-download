#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试真实百度网盘下载的可能性"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

print("=" * 70)
print(" " * 15 + "百度网盘真实下载可行性测试")
print("=" * 70)

# 1. 检查BaiduPCS-Py
print("\n[1/3] 检查BaiduPCS-Py安装状态:")
try:
    from baidupcs_py import BaiduPCS
    print("  OK - BaiduPCS-Py已安装")
    BAIDUPCS_AVAILABLE = True
except ImportError:
    print("  INFO - BaiduPCS-Py未安装，将检查替代方案")
    BAIDUPCS_AVAILABLE = False

# 2. 检查requests
print("\n[2/3] 检查requests库:")
try:
    import requests
    print(f"  OK - requests已安装 (版本: {requests.__version__})")
    REQUESTS_AVAILABLE = True
except ImportError:
    print("  ERROR - requests未安装")
    REQUESTS_AVAILABLE = False

# 3. 检查认证信息
print("\n[3/3] 检查百度网盘认证信息:")
import os
bduss = os.getenv('BAIDU_BDUSS')
cookies = os.getenv('BAIDU_COOKIES')

if bduss:
    print(f"  OK - BDUSS已设置 ({len(bduss)} 字符)")
else:
    print("  WARN - BDUSS未设置")

if cookies:
    print(f"  OK - COOKIES已设置 ({len(cookies)} 字符)")
    # 检查关键字段
    if 'STOKEN' in cookies:
        print("  OK - COOKIES包含STOKEN")
    if 'PANWEB' in cookies:
        print("  OK - COOKIES包含PANWEB")
else:
    print("  WARN - COOKIES未设置")

print("\n" + "=" * 70)
print("解决方案建议:")
print("=" * 70)

if BAIDUPCS_AVAILABLE:
    print("方案1: 使用现有的BaiduPCS-Py进行真实下载")
    print("  - 可以立即使用")
    print("  - 功能完整")
elif REQUESTS_AVAILABLE and (bduss or cookies):
    print("方案2: 使用requests库实现真实下载")
    print("  - 需要实现下载逻辑")
    print("  - 可以使用现有的认证信息")
else:
    print("方案3: 需要安装必要的依赖")
    print("  - pip install requests")
    print("  - 配置百度网盘认证信息")

print("\n推荐的解决方案:")
if REQUESTS_AVAILABLE:
    print("  可以创建基于requests的真实下载实现")
    print("  不需要C++编译工具")
    print("  使用现有的百度网盘认证信息")
else:
    print("  需要先安装requests库")

print("=" * 70)
