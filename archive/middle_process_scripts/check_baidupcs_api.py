#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查BaiduPCS-Py的API"""
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
print("检查BaiduPCS-Py的初始化API")
print("=" * 60)

try:
    from baidupcs_py import BaiduPCS
    print("✓ BaiduPCS-Py导入成功")

    # 查看初始化方法的签名
    import inspect
    sig = inspect.signature(BaiduPCS.__init__)
    print(f"\nBaiduPCS.__init__ 参数:")
    for param_name, param in sig.parameters.items():
        if param_name != 'self':
            default = param.default if param.default != inspect.Parameter.empty else "无默认值"
            print(f"  - {param_name}: {default}")

    # 检查环境变量
    bduss = os.getenv('BAIDU_BDUSS')
    cookies = os.getenv('BAIDU_COOKIES')

    print(f"\n环境变量状态:")
    print(f"  BDUSS: {'已设置' if bduss else '未设置'} ({len(bduss) if bduss else 0} 字符)")
    print(f"  COOKIES: {'已设置' if cookies else '未设置'} ({len(cookies) if cookies else 0} 字符)")

    # 尝试不同的初始化方式
    print(f"\n尝试初始化BaiduPCS:")

    # 方法1: 只传bduss
    try:
        print("\n1. 只传bduss参数:")
        baidupcs1 = BaiduPCS(bduss=bduss)
        print(f"  ✓ 成功 - {type(baidupcs1)}")
    except Exception as e:
        print(f"  ✗ 失败: {e}")

    # 方法2: 传bduss和cookies
    try:
        print("\n2. 传bduss和cookies参数:")
        # 解析cookies
        cookies_dict = {}
        if cookies:
            for item in cookies.split(';'):
                item = item.strip()
                if '=' in item:
                    key, value = item.split('=', 1)
                    cookies_dict[key.strip()] = value.strip()

        baidupcs2 = BaiduPCS(bduss=bduss, cookies=cookies_dict)
        print(f"  ✓ 成功 - {type(baidupcs2)}")
    except Exception as e:
        print(f"  ✗ 失败: {e}")

    # 方法3: 从cookies中提取BDUSS
    try:
        print("\n3. 从cookies中提取BDUSS:")
        cookies_dict = {}
        if cookies:
            for item in cookies.split(';'):
                item = item.strip()
                if '=' in item:
                    key, value = item.split('=', 1)
                    cookies_dict[key.strip()] = value.strip()

        cookies_bduss = cookies_dict.get('BDUSS')
        print(f"  cookies中的BDUSS: {cookies_bduss[:20] if cookies_bduss else '未找到'}...")

        baidupcs3 = BaiduPCS(bduss=cookies_bduss, cookies=cookies_dict)
        print(f"  ✓ 成功 - {type(baidupcs3)}")
    except Exception as e:
        print(f"  ✗ 失败: {e}")

    # 查看可用方法
    print(f"\n可用的下载相关方法:")
    test_methods = ['download', 'list', 'listsharedpaths', 'shared']
    for method in test_methods:
        if hasattr(BaiduPCS, method):
            print(f"  ✓ {method}")
        else:
            print(f"  ✗ {method} (不存在)")

except ImportError as e:
    print(f"✗ 导入失败: {e}")
except Exception as e:
    print(f"✗ 检查失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
