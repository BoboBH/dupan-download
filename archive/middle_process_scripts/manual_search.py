#!/usr/bin/env python3
"""手动搜索百度网盘中的260701文件夹"""
import subprocess
import os

def run_command(cmd):
    """运行命令并返回输出"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='gbk', errors='ignore')
    return result.stdout + result.stderr, result.returncode

def try_path(path):
    """尝试访问路径"""
    print(f"\n尝试路径: {path}")
    output, code = run_command(f".venv/Scripts/bypy.exe list \"{path}\"")
    print(f"返回码: {code}")
    if "Error" not in output and code == 0:
        print("✓ 成功访问!")
        print(output)
        return True
    else:
        print("✗ 无法访问")
        return False

def main():
    print("=== 手动搜索百度网盘中的260701文件夹 ===")
    print("=" * 60)

    # 先检查当前可访问的目录
    print("\n1. 检查当前默认目录:")
    output, _ = run_command(".venv/Scripts/bypy.exe list")
    print(output)

    # 尝试不同的路径格式
    paths_to_try = [
        "/",                    # 根目录
        "/apps",               # 应用目录
        "/apps/bypy",          # bypy应用目录
        "/apps/bypy/260701",   # 260701文件夹
        "/我的网盘",           # 我的网盘 (中文)
        "/NetDisk",            # NetDisk (英文)
        "/Documents",          # 文档
        "/我的网盘/260701",    # 我的网盘下的260701
        "/260701",             # 根目录下的260701
    ]

    print("\n2. 尝试不同的路径:")
    successful_paths = []
    for path in paths_to_try:
        if try_path(path):
            successful_paths.append(path)

    print("\n3. 成功访问的路径:")
    for path in successful_paths:
        print(f"  ✓ {path}")

    # 尝试搜索功能
    print("\n4. 尝试搜索功能:")
    output, _ = run_command(".venv/Scripts/bypy.exe search 260701")
    print(output)

if __name__ == "__main__":
    main()