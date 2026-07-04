#!/usr/bin/env python
"""调试BaiduPCS初始化问题"""
import sys
import os
import logging
from pathlib import Path
import traceback

# 添加项目路径到sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)

# 加载环境变量
try:
    from dotenv import load_dotenv
    env_path = project_root / '.env'
    load_dotenv(dotenv_path=env_path)
    print(f"已加载环境配置: {env_path}")
except ImportError:
    print("警告: python-dotenv未安装")

print("\n=== 导入BaiduDownloader ===")
from dupan_download.downloader import BaiduDownloader, BAIDUPCS_AVAILABLE
print(f"BAIDUPCS_AVAILABLE: {BAIDUPCS_AVAILABLE}")

print("\n=== 初始化BaiduDownloader ===")
downloader = BaiduDownloader()

print("\n=== 调用_init_baidupcs() ===")
print("开始调试BaiduPCS初始化...")

# 检查环境变量
bduss = os.getenv('BAIDU_BDUSS')
cookies = os.getenv('BAIDU_COOKIES')
print(f"BDUSS环境变量: {bduss[:20] if bduss else None}...")
print(f"COOKIES环境变量: {cookies[:50] if cookies else None}...")

# 手动执行初始化步骤
try:
    from baidupcs_py import BaiduPCS
    print("BaiduPCS导入成功")

    # 解析cookies
    cookies_dict = {}
    if cookies:
        print("解析cookies...")
        for item in cookies.split(';'):
            item = item.strip()
            if '=' in item:
                key, value = item.split('=', 1)
                cookies_dict[key.strip()] = value.strip()

    print(f"找到 {len(cookies_dict)} 个cookie字段")
    print(f"BDUSS in cookies: {'BDUSS' in cookies_dict}")
    print(f"STOKEN in cookies: {'STOKEN' in cookies_dict}")

    # 获取值
    bduss_value = bduss if bduss else cookies_dict.get('BDUSS')
    stoken_value = cookies_dict.get('STOKEN')

    print(f"bduss_value: {bduss_value[:20] if bduss_value else None}...")
    print(f"stoken_value: {stoken_value[:20] if stoken_value else None}...")

    # 初始化BaiduPCS
    print("初始化BaiduPCS...")
    baidupcs = BaiduPCS(
        bduss=bduss_value,
        stoken=stoken_value,
        cookies=cookies_dict
    )

    print(f"[OK] BaiduPCS初始化成功: {type(baidupcs)}")

except Exception as e:
    print(f"[FAIL] BaiduPCS初始化失败: {e}")
    traceback.print_exc()

print("\n=== 调用downloader._init_baidupcs() ===")
try:
    result = downloader._init_baidupcs()
    print(f"返回结果: {result}")
    print(f"downloader.baidupcs: {downloader.baidupcs}")
except Exception as e:
    print(f"异常: {e}")
    traceback.print_exc()
