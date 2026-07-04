#!/usr/bin/env python
"""
快速测试脚本 - 使用真实百度网盘链接
"""
import sys
from pathlib import Path

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

print("=" * 60)
print("百度网盘下载功能 - 快速测试")
print("=" * 60)

# 1. 检查环境变量
print("\n1. 检查配置...")
bduss = os.getenv('BAIDU_BDUSS')
cookies = os.getenv('BAIDU_COOKIES')

if bduss:
    print(f"✓ BDUSS已设置 (长度: {len(bduss)})")
else:
    print("✗ BDUSS未设置")

if cookies:
    print(f"✓ COOKIES已设置 (长度: {len(cookies)})")
else:
    print("✗ COOKIES未设置")

# 2. 检查BaiduPCS-Py
print("\n2. 检查BaiduPCS-Py...")
try:
    from baidupcs_py import BaiduPCS
    print("✓ BaiduPCS-Py已安装")
except ImportError as e:
    print(f"✗ BaiduPCS-Py未安装: {e}")

# 3. 初始化下载器
print("\n3. 初始化下载器...")
try:
    from dupan_download.downloader import BaiduDownloader
    downloader = BaiduDownloader()
    print("✓ 下载器初始化成功")
except Exception as e:
    print(f"✗ 下载器初始化失败: {e}")
    sys.exit(1)

# 4. 测试链接验证
print("\n4. 测试链接验证...")
test_link = "https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg"
test_code = "0409"

print(f"链接: {test_link}")
print(f"提取码: {test_code}")

try:
    result = downloader.validate_link(test_link, test_code)
    if result:
        print("✓ 链接验证通过")
    else:
        print("✗ 链接验证失败")
except Exception as e:
    print(f"✗ 链接验证异常: {e}")
    import traceback
    traceback.print_exc()

# 5. 尝试获取文件列表
print("\n5. 尝试获取文件列表...")
try:
    files = downloader.list_files(test_link)
    if files:
        print(f"✓ 获取到 {len(files)} 个文件:")
        for i, file in enumerate(files, 1):
            print(f"  {i}. {file.get('filename')} ({file.get('size', 0)} bytes)")
    else:
        print("✗ 未获取到文件列表")
except Exception as e:
    print(f"✗ 获取文件列表异常: {e}")
    import traceback
    traceback.print_exc()

# 6. 测试下载功能
print("\n6. 测试下载功能...")
try:
    import tempfile
    temp_dir = Path(tempfile.gettempdir()) / "dupan_test"
    temp_dir.mkdir(exist_ok=True)

    print(f"临时目录: {temp_dir}")

    results = downloader.download_folder(test_link, temp_dir)

    if results:
        print(f"✓ 下载完成，共 {len(results)} 个文件:")
        for i, result in enumerate(results, 1):
            if result.success:
                print(f"  {i}. ✓ {result.local_path}")
            else:
                print(f"  {i}. ✗ {result.remote_path}: {result.error}")
    else:
        print("✗ 下载失败")

except Exception as e:
    print(f"✗ 下载异常: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
