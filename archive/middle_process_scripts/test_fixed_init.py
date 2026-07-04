#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试修复后的BaiduPCS初始化"""
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
print("测试修复后的BaiduPCS初始化")
print("=" * 60)

# 测试下载器初始化
print("\n1. 创建下载器并初始化BaiduPCS-Py:")
try:
    from dupan_download.downloader import BaiduDownloader
    downloader = BaiduDownloader()
    print("✓ 下载器创建成功")

    # 尝试初始化BaiduPCS
    result = downloader._init_baidupcs()
    if result:
        print("✓ BaiduPCS-Py初始化成功")
        print(f"  BaiduPCS对象类型: {type(downloader.baidupcs)}")
    else:
        print("✗ BaiduPCS-Py初始化失败")
        sys.exit(1)

except Exception as e:
    print(f"✗ 初始化异常: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试真实下载
print("\n2. 测试真实下载功能:")
test_link = "https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg"
test_code = "0409"

try:
    import tempfile
    temp_dir = Path(tempfile.mkdtemp())
    print(f"  临时目录: {temp_dir}")

    # 先验证链接
    valid = downloader.validate_link(test_link, test_code)
    if not valid:
        print("✗ 链接验证失败")
        sys.exit(1)

    print("✓ 链接验证通过")

    # 获取文件列表
    files = downloader.list_files(test_link)
    print(f"✓ 获取到 {len(files)} 个文件")

    # 下载文件
    results = downloader.download_folder(test_link, temp_dir)
    print(f"✓ 下载完成，共 {len(results)} 个文件")

    # 检查下载的文件
    for result in results:
        if result.success:
            file_path = Path(result.local_path)
            if file_path.exists():
                size = file_path.stat().st_size
                print(f"  ✓ {file_path.name} - {size} bytes")

                # 检查是否是模拟文件
                content = file_path.read_text(errors='ignore')
                if content.startswith("模拟下载"):
                    print("    ⚠️  这是模拟文件，真实下载仍未启用")
                else:
                    print("    ✓ 这是真实下载的文件")
            else:
                print(f"  ✗ 文件不存在: {file_path}")
        else:
            print(f"  ✗ 下载失败: {result.error}")

    print(f"\n临时文件保存在: {temp_dir}")

except Exception as e:
    print(f"✗ 下载测试异常: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
