#!/usr/bin/env python
"""使用真实CLI测试百度网盘下载"""
import os
import sys
from pathlib import Path
from click.testing import CliRunner

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("使用真实链接测试CLI下载功能")
print("=" * 60)

# 导入CLI主函数
from dupan_download.cli import main

# 创建临时目录用于测试
import tempfile
temp_dir = tempfile.mkdtemp()

print(f"\n临时目录: {temp_dir}")
print(f"测试链接: https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg")
print(f"提取码: 0409")

# 使用Click的测试运行器
runner = CliRunner()

print("\n开始执行下载...")

result = runner.invoke(main, [
    'https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg',
    '0409',
    '--keep-temp',
    '--temp-dir', temp_dir,
    '--verbose'
])

print("\n" + "=" * 60)
print("执行结果")
print("=" * 60)

print(f"\n退出码: {result.exit_code}")
print(f"\n输出:\n{result.output}")

if result.exception:
    print(f"\n异常信息:")
    import traceback
    traceback.print_exception(type(result.exception), result.exception, result.exception.__traceback__)

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)

print(f"\n临时文件保留在: {temp_dir}")
print("如需清理，请手动删除该目录")
