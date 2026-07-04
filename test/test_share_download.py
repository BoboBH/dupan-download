#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""测试分享链接下载功能"""
import sys
from pathlib import Path
import tempfile

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from dupan_download.share_downloader import ShareLinkDownloader

print("=" * 70)
print(" " * 15 + "分享链接下载测试")
print("=" * 70)

# 测试参数
share_link = "https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg"
extract_code = "0409"

try:
    # 1. 创建下载器
    print("\n[1/5] 创建分享链接下载器:")
    downloader = ShareLinkDownloader()
    print("  OK - 下载器创建成功")

    # 2. 验证链接
    print(f"\n[2/5] 验证分享链接:")
    print(f"  链接: {share_link}")
    print(f"  提取码: {extract_code}")

    is_valid = downloader.validate_link(share_link, extract_code)
    if is_valid:
        print("  OK - 链接验证通过")
    else:
        print("  FAIL - 链接验证失败")
        sys.exit(1)

    # 3. 提取分享ID
    print(f"\n[3/5] 提取分享ID:")
    share_id = downloader.get_share_id(share_link)
    if share_id:
        print(f"  OK - 分享ID: {share_id}")
    else:
        print("  FAIL - 无法提取分享ID")
        sys.exit(1)

    # 4. 获取文件列表
    print(f"\n[4/5] 获取文件列表:")
    files = downloader.get_file_list(share_link, extract_code)

    if files:
        print(f"  OK - 获取到 {len(files)} 个文件:")
        for i, file in enumerate(files[:10], 1):  # 只显示前10个
            filename = file.get('filename')
            size = file.get('size', 0)
            is_dir = file.get('is_dir', False)
            file_type = "目录" if is_dir else "文件"
            print(f"    {i}. [{file_type}] {filename} ({size} bytes)")

        if len(files) > 10:
            print(f"    ... 还有 {len(files) - 10} 个文件")
    else:
        print("  FAIL - 未获取到文件列表")
        sys.exit(1)

    # 5. 尝试下载测试
    print(f"\n[5/5] 尝试下载测试:")
    temp_dir = Path(tempfile.mkdtemp())
    print(f"  临时目录: {temp_dir}")

    results = downloader.download_folder(share_link, extract_code, temp_dir)

    if results:
        success_count = sum(1 for r in results if r.success)
        fail_count = len(results) - success_count

        print(f"  下载结果: {success_count} 成功, {fail_count} 失败")

        if success_count > 0:
            print(f"  成功下载的文件:")
            for result in results[:5]:
                if result.success:
                    print(f"    - {Path(result.local_path).name} ({result.size} bytes)")
        else:
            print(f"  说明: 当前实现需要进一步完善下载链接获取")
    else:
        print("  未返回下载结果")

    print(f"\n临时文件目录: {temp_dir}")

except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("测试完成")
print("=" * 70)
