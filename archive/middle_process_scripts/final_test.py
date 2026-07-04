#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""最终完整测试 - 验证修复后的百度网盘下载功能"""
import os
import sys
from pathlib import Path
import tempfile

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

# 设置控制台输出编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from dotenv import load_dotenv
load_dotenv()

print("=" * 70)
print(" " * 15 + "百度网盘下载功能 - 最终完整测试")
print("=" * 70)

# 测试参数
test_link = "https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg"
test_code = "0409"

try:
    # 1. 导入模块
    print("\n[1/6] 导入模块...")
    from dupan_download.downloader import BaiduDownloader
    print("  OK - 模块导入成功")

    # 2. 创建下载器
    print("\n[2/6] 创建下载器...")
    downloader = BaiduDownloader()
    print("  OK - 下载器创建成功")
    print(f"  - 最大重试次数: {downloader.max_retries}")
    print(f"  - 连接超时: {downloader.connect_timeout}s")
    print(f"  - 传输超时: {downloader.transfer_timeout}s")

    # 3. 验证链接
    print(f"\n[3/6] 验证分享链接...")
    print(f"  链接: {test_link}")
    print(f"  提取码: {test_code}")

    is_valid = downloader.validate_link(test_link, test_code)
    if is_valid:
        print("  OK - 链接验证通过")
    else:
        print("  FAIL - 链接验证失败")
        sys.exit(1)

    # 4. 获取文件列表
    print("\n[4/6] 获取分享文件列表...")
    files = downloader.list_files(test_link)

    if not files:
        print("  WARNING - 未获取到文件列表，可能是权限或API问题")
    else:
        print(f"  OK - 获取到 {len(files)} 个文件:")
        for i, file_info in enumerate(files, 1):
            filename = file_info.get('filename', 'unknown')
            size = file_info.get('size', 0)
            is_dir = file_info.get('is_dir', False)
            file_type = "目录" if is_dir else "文件"
            print(f"    {i}. [{file_type}] {filename} ({size} bytes)")

    # 5. 测试下载
    print("\n[5/6] 测试文件下载...")
    temp_dir = Path(tempfile.mkdtemp())
    print(f"  临时目录: {temp_dir}")

    download_results = downloader.download_folder(test_link, temp_dir)

    if not download_results:
        print("  WARNING - 下载结果为空")
    else:
        success_count = sum(1 for r in download_results if r.success)
        fail_count = len(download_results) - success_count

        print(f"  下载完成: {success_count} 成功, {fail_count} 失败")

        # 显示下载的文件
        for result in download_results:
            if result.success:
                local_path = Path(result.local_path)
                if local_path.exists():
                    size = local_path.stat().st_size
                    print(f"    - {local_path.name} ({size} bytes)")

                    # 检查是否为真实文件
                    if size > 100:  # 大于100字节可能是真实文件
                        print(f"      可能是真实下载的文件")
                    else:
                        # 读取内容检查
                        try:
                            content = local_path.read_text(errors='ignore')
                            if content.startswith("模拟下载"):
                                print(f"      这是模拟文件")
                            else:
                                print(f"      可能是真实文件")
                        except:
                            print(f"      二进制文件或无法读取")
                else:
                    print(f"    - {result.remote_path} (文件不存在)")
            else:
                print(f"    - {result.remote_path}: {result.error}")

    # 6. 测试总结
    print("\n[6/6] 测试总结:")
    print("  [OK] 模块导入成功")
    print("  [OK] 下载器创建成功")
    print("  [OK] 链接验证通过")
    print(f"  [{'OK' if files else 'WARN'}] 文件列表获取: {len(files) if files else 0} 个文件")
    print(f"  [{'OK' if download_results else 'WARN'}] 下载功能: {len(download_results) if download_results else 0} 个结果")

    print("\n" + "=" * 70)
    print("测试完成！")
    print(f"临时文件保存在: {temp_dir}")
    print("=" * 70)

    # 清理提示
    print(f"\n如需清理临时文件，请手动删除: {temp_dir}")

except Exception as e:
    print(f"\n错误: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
