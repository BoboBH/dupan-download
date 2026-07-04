#!/usr/bin/env python
"""测试BaiduPCS初始化"""
import sys
import os
from pathlib import Path
import traceback

# 添加项目路径到sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 加载环境变量
try:
    from dotenv import load_dotenv
    env_path = project_root / '.env'
    load_dotenv(dotenv_path=env_path)
    print(f"已加载环境配置: {env_path}")
except ImportError:
    print("警告: python-dotenv未安装")

print("\n=== 检查环境变量 ===")
bduss = os.getenv('BAIDU_BDUSS')
cookies = os.getenv('BAIDU_COOKIES')
print(f"BAIDU_BDUSS: {bduss[:20] if bduss else None}... (长度: {len(bduss) if bduss else 0})")
print(f"BAIDU_COOKIES: {cookies[:50] if cookies else None}... (长度: {len(cookies) if cookies else 0})")

print("\n=== 测试BaiduPCS导入 ===")
try:
    from baidupcs_py import BaiduPCS
    print("[OK] BaiduPCS导入成功")
except ImportError as e:
    print(f"[FAIL] BaiduPCS导入失败: {e}")
    sys.exit(1)

print("\n=== 测试BaiduDownloader导入 ===")
try:
    from dupan_download.downloader import BaiduDownloader
    print("[OK] BaiduDownloader导入成功")
except ImportError as e:
    print(f"[FAIL] BaiduDownloader导入失败: {e}")
    sys.exit(1)

print("\n=== 测试BaiduDownloader初始化 ===")
try:
    downloader = BaiduDownloader()
    print("[OK] BaiduDownloader初始化成功")
    print(f"  - max_retries: {downloader.max_retries}")
    print(f"  - connect_timeout: {downloader.connect_timeout}")
    print(f"  - transfer_timeout: {downloader.transfer_timeout}")
except Exception as e:
    print(f"[FAIL] BaiduDownloader初始化失败: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n=== 测试BaiduPCS初始化 ===")
try:
    result = downloader._init_baidupcs()
    print(f"初始化结果: {result}")

    if result and downloader.baidupcs:
        print("[OK] BaiduPCS初始化成功")
        print(f"  - BaiduPCS对象: {type(downloader.baidupcs)}")
    else:
        print("[FAIL] BaiduPCS初始化失败")
        print("  - baidupcs属性为None")

except Exception as e:
    print(f"[FAIL] BaiduPCS初始化异常: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n=== 所有测试完成 ===")
