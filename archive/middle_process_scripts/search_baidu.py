#!/usr/bin/env python3
"""搜索百度网盘中包含260701的文件夹"""
import subprocess
import sys
import os

def run_bypy_command(command):
    """运行bypy命令"""
    full_command = f".venv/Scripts/bypy.exe {command}"
    result = subprocess.run(full_command, shell=True, capture_output=True, text=True, encoding='gbk', errors='ignore')
    return result.stdout + result.stderr

def list_directory(path=""):
    """列出目录内容"""
    if path:
        command = f'list "{path}"'
    else:
        command = 'list'
    return run_bypy_command(command)

def search_recursive(keyword, path="", max_depth=5, current_depth=0):
    """递归搜索包含关键词的文件夹"""
    if current_depth >= max_depth:
        return []

    print(f"正在搜索: {path if path else '根目录'} (深度: {current_depth})")

    # 列出当前目录
    output = list_directory(path)
    lines = output.split('\n')

    found_folders = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith('<') or line.startswith('='):
            continue

        # 解析行内容: "D folder_name size date" 或 "F file_name size date hash"
        parts = line.split()
        if len(parts) >= 2:
            file_type = parts[0]
            name = parts[1]

            # 检查是否包含关键词
            if keyword in name:
                full_path = f"{path}/{name}" if path else name
                found_folders.append(full_path)
                print(f"✓ 找到: {full_path}")

            # 如果是目录，递归搜索
            if file_type == 'D' or file_type == 'd':
                full_path = f"{path}/{name}" if path else name
                sub_results = search_recursive(keyword, full_path, max_depth, current_depth + 1)
                found_folders.extend(sub_results)

    return found_folders

def main():
    print("开始搜索百度网盘中包含 '260701' 的文件夹...")
    print("=" * 60)

    # 先列出根目录
    print("\n根目录内容:")
    root_output = list_directory()
    print(root_output)

    # 开始递归搜索
    print("\n开始递归搜索...")
    found = search_recursive('260701', max_depth=4)

    if found:
        print(f"\n找到 {len(found)} 个包含 '260701' 的文件夹:")
        for folder in found:
            print(f"  - {folder}")

        # 详细查看每个找到的文件夹内容
        print("\n" + "=" * 60)
        print("详细文件夹内容:")
        for folder in found:
            print(f"\n文件夹: {folder}")
            print("-" * 40)
            contents = list_directory(folder)
            print(contents)
    else:
        print("\n未找到包含 '260701' 的文件夹")

if __name__ == '__main__':
    main()