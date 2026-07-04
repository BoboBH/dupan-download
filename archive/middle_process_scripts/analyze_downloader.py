#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""分析当前downloader的BaiduPCS使用方式"""
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
print("分析当前downloader的BaiduPCS使用方式")
print("=" * 60)

# 读取当前的downloader代码
downloader_path = Path(__file__).parent / "dupan_download" / "downloader.py"
with open(downloader_path, 'r', encoding='utf-8') as f:
    content = f.read()

print("\n1. 当前的_init_baidupcs方法:")
# 提取_init_baidupcs方法
import re
init_method = re.search(r'def _init_baidupcs\(self\):.*?(?=\n    def |\Z)', content, re.DOTALL)
if init_method:
    print(init_method.group(0)[:500])
    print("...")

print("\n2. 检查环境变量:")
bduss = os.getenv('BAIDU_BDUSS')
cookies = os.getenv('BAIDU_COOKIES')

if bduss:
    print(f"  BDUSS: {bduss[:30]}... (总长度: {len(bduss)})")
else:
    print("  BDUSS: 未设置")

if cookies:
    # 解析cookies查看关键内容
    cookies_dict = {}
    for item in cookies.split(';'):
        item = item.strip()
        if '=' in item:
            key, value = item.split('=', 1)
            cookies_dict[key.strip()] = value.strip()

    print(f"  COOKIES: 包含以下关键字段:")
    for key in ['BDUSS', 'STOKEN', 'PANWEB']:
        if key in cookies_dict:
            value = cookies_dict[key]
            print(f"    - {key}: {value[:30]}... (总长度: {len(value)})")
else:
    print("  COOKIES: 未设置")

print("\n3. 可能的初始化方式:")
print("  方式1: BaiduPCS(bduss=bduss_value)")
print("  方式2: BaiduPCS(bduss=bduss_value, cookies=cookies_dict)")
print("  方式3: BaiduPCS.from_cookies(cookies)")

print("\n4. 分析问题:")
print("  - BaiduPCS-Py可能需要特定的认证格式")
print("  - Cookie中的BDUSS可能需要URL编码")
print("  - 可能需要其他认证参数（如STOKEN）")

print("\n" + "=" * 60)
