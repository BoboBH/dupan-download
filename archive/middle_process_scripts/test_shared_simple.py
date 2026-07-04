#!/usr/bin/env python
"""测试分享链接处理"""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

project_root = Path(__file__).parent
load_dotenv(project_root / '.env')

from baidupcs_py import BaiduPCS

# 获取环境变量
bduss = os.getenv('BAIDU_BDUSS')
cookies = os.getenv('BAIDU_COOKIES')

# 解析cookies
cookies_dict = {}
if cookies:
    for item in cookies.split(';'):
        item = item.strip()
        if '=' in item:
            key, value = item.split('=', 1)
            cookies_dict[key.strip()] = value.strip()

# 初始化BaiduPCS
pcs = BaiduPCS(bduss=bduss, cookies=cookies_dict)

# 测试分享链接
share_link = "https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg"
extract_code = "0409"

print("=== 测试分享链接处理 ===")
print(f"分享链接: {share_link}")
print(f"提取码: {extract_code}")
print()

# 提取分享ID
import re
share_id_match = re.search(r'/s/([a-zA-Z0-9_-]+)', share_link)
if share_id_match:
    share_id = share_id_match.group(1)
    print(f"提取的分享ID: {share_id}")

    print("\n=== 测试 shared_init_url 方法 ===")
    try:
        result = pcs.shared_init_url(share_id)
        print(f"结果类型: {type(result)}")
        print(f"结果内容: {result}")
    except Exception as e:
        print(f"错误: {e}")

    print("\n=== 测试 shared_password 方法 ===")
    try:
        result = pcs.shared_password(share_id, extract_code)
        print(f"结果类型: {type(result)}")
        print(f"结果内容: {result}")
    except Exception as e:
        print(f"错误: {e}")

else:
    print("无法提取分享ID")
