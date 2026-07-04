#!/usr/bin/env python
"""调试BaiduPCS初始化问题"""
import os
import traceback
from pathlib import Path
from baidupcs_py import BaiduPCS

# 加载环境变量
try:
    from dotenv import load_dotenv
    project_root = Path(__file__).parent
    env_path = project_root / '.env'
    load_dotenv(dotenv_path=env_path)
    print(f"已加载环境配置: {env_path}")
except ImportError:
    print("警告: python-dotenv未安装，使用系统环境变量")

print("=== BaiduPCS初始化调试 ===")
print()

# 获取环境变量
bduss = os.getenv('BAIDU_BDUSS')
cookies = os.getenv('BAIDU_COOKIES')

print(f"BDUSS长度: {len(bduss) if bduss else 0}")
print(f"COOKIES长度: {len(cookies) if cookies else 0}")
print()

# 解析cookies
cookies_dict = {}
if cookies:
    print("解析COOKIES:")
    for item in cookies.split(';'):
        item = item.strip()
        if '=' in item:
            key, value = item.split('=', 1)
            cookies_dict[key.strip()] = value.strip()
            print(f"  {key}: {value[:20]}...")

print()
print("尝试初始化BaiduPCS...")

try:
    # 获取BDUSS值
    bduss_value = bduss if bduss else cookies_dict.get('BDUSS')
    stoken_value = cookies_dict.get('STOKEN')

    print(f"使用BDUSS: {bduss_value[:20] if bduss_value else None}...")
    print(f"使用STOKEN: {stoken_value[:20] if stoken_value else None}...")

    # 初始化BaiduPCS
    baidupcs = BaiduPCS(
        bduss=bduss_value,
        stoken=stoken_value,
        cookies=cookies_dict
    )

    print("[OK] BaiduPCS初始化成功!")
    print(f"  BaiduPCS对象: {type(baidupcs)}")

except Exception as e:
    print(f"[FAIL] BaiduPCS初始化失败: {e}")
    print()
    print("详细错误信息:")
    traceback.print_exc()
