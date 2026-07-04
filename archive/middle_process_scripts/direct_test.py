#!/usr/bin/env python
"""直接测试百度网盘下载 - 简化版本"""
import os
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

print("开始测试...")

# 1. 测试环境变量
print("\n1. 环境变量:")
bduss = os.getenv('BAIDU_BDUSS')
cookies = os.getenv('BAIDU_COOKIES')
print(f"BDUSS: {len(bduss) if bduss else 0} chars")
print(f"COOKIES: {len(cookies) if cookies else 0} chars")

# 2. 测试导入
print("\n2. 导入模块:")
try:
    from baidupcs_py import BaiduPCS
    print("BaiduPCS-Py: OK")
except Exception as e:
    print(f"BaiduPCS-Py: {e}")

try:
    from dupan_download.downloader import BaiduDownloader
    print("BaiduDownloader: OK")
except Exception as e:
    print(f"BaiduDownloader: {e}")
    sys.exit(1)

# 3. 测试下载器
print("\n3. 创建下载器:")
try:
    downloader = BaiduDownloader()
    print("下载器创建成功")
    print(f"max_retries: {downloader.max_retries}")
except Exception as e:
    print(f"创建失败: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. 测试链接验证
print("\n4. 链接验证:")
test_link = "https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg"
test_code = "0409"
print(f"链接: {test_link}")
print(f"提取码: {test_code}")

try:
    valid = downloader.validate_link(test_link, test_code)
    print(f"验证结果: {valid}")
except Exception as e:
    print(f"验证失败: {e}")
    import traceback
    traceback.print_exc()

# 5. 测试获取文件列表
print("\n5. 获取文件列表:")
try:
    files = downloader.list_files(test_link)
    print(f"文件数量: {len(files)}")
    for i, f in enumerate(files[:3], 1):
        print(f"  {i}. {f.get('filename')} - {f.get('size')} bytes")
except Exception as e:
    print(f"获取失败: {e}")
    import traceback
    traceback.print_exc()

# 6. 测试下载
print("\n6. 测试下载:")
try:
    import tempfile
    temp = Path(tempfile.mkdtemp())
    print(f"临时目录: {temp}")

    results = downloader.download_folder(test_link, temp)
    print(f"下载结果数量: {len(results)}")

    for r in results[:3]:
        status = "成功" if r.success else "失败"
        print(f"  [{status}] {r.local_path or r.remote_path}")
        if not r.success:
            print(f"    错误: {r.error}")

except Exception as e:
    print(f"下载失败: {e}")
    import traceback
    traceback.print_exc()

print("\n测试完成！")
