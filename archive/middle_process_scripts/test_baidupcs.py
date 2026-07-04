#!/usr/bin/env python
"""
测试BaiduPCS-Py的基本功能
"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

print("=" * 60)
print("BaiduPCS-Py 功能测试")
print("=" * 60)

# 1. 检查认证信息
bduss = os.getenv('BAIDU_BDUSS')
cookies = os.getenv('BAIDU_COOKIES')

print(f"\n1. 认证信息检查:")
print(f"   BDUSS: {'已设置' if bduss else '未设置'}")
print(f"   COOKIES: {'已设置' if cookies else '未设置'}")

# 2. 导入BaiduPCS-Py
print(f"\n2. 导入BaiduPCS-Py:")
try:
    from baidupcs_py import BaiduPCS
    print("   ✓ 导入成功")
except ImportError as e:
    print(f"   ✗ 导入失败: {e}")
    exit(1)

# 3. 初始化BaiduPCS
print(f"\n3. 初始化BaiduPCS:")
try:
    baidupcs = BaiduPCS()
    print("   ✓ 初始化成功")
    print(f"   对象类型: {type(baidupcs)}")
except Exception as e:
    print(f"   ✗ 初始化失败: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

# 4. 测试分享链接
share_link = "https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg"
extract_code = "0409"

print(f"\n4. 测试分享链接:")
print(f"   链接: {share_link}")
print(f"   提取码: {extract_code}")

# 查看可用的方法
print(f"\n5. BaiduPCS可用的方法:")
methods = [method for method in dir(baidupcs) if not method.startswith('_')]
for i, method in enumerate(methods, 1):
    print(f"   {i}. {method}")

# 尝试列出分享文件
print(f"\n6. 尝试列出分享文件:")
try:
    # 尝试不同的方法
    if hasattr(baidupcs, 'list'):
        print("   尝试使用 list 方法...")
        result = baidupcs.list(share_link)
        print(f"   结果: {result}")
    elif hasattr(baidupcs, 'listsharedpaths'):
        print("   尝试使用 listsharedpaths 方法...")
        result = baidupcs.listsharedpaths(share_link, extract_code)
        print(f"   结果: {result}")
    elif hasattr(baidupcs, 'shared'):
        print("   尝试使用 shared 方法...")
        result = baidupcs.shared(share_link, extract_code)
        print(f"   结果: {result}")
    else:
        print("   没有找到合适的方法")

except Exception as e:
    print(f"   ✗ 调用失败: {e}")
    import traceback
    traceback.print_exc()

print(f"\n" + "=" * 60)
print("测试完成")
print("=" * 60)
