#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""分析下载结果"""
import os
import sys
from pathlib import Path
import tempfile

def find_download_directories():
    """查找最近的下载目录"""
    temp_base = Path(tempfile.gettempdir())

    # 查找所有dupan_download开头的目录
    download_dirs = []
    for item in temp_base.iterdir():
        if item.is_dir() and item.name.startswith('dupan_download_'):
            download_dirs.append(item)

    # 按修改时间排序，最新的在前
    download_dirs.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return download_dirs

def analyze_directory(directory):
    """分析目录中的文件"""
    if not directory.exists():
        return None

    files = list(directory.rglob('*'))
    files = [f for f in files if f.is_file()]

    total_size = sum(f.stat().st_size for f in files)
    file_count = len(files)

    return {
        'path': directory,
        'file_count': file_count,
        'total_size': total_size,
        'files': files
    }

def format_size(size_bytes):
    """格式化文件大小"""
    if size_bytes == 0:
        return "0 B"
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def main():
    print("=" * 70)
    print(" " * 20 + "下载结果分析")
    print("=" * 70)

    # 查找下载目录
    print("\n[1/3] 查找下载目录...")
    download_dirs = find_download_directories()

    if not download_dirs:
        print("  未找到任何下载目录")
        print("\n可能的原因:")
        print("  - 下载尚未执行")
        print("  - 临时文件已被清理")
        print("  - 使用了自定义目录")
        return

    print(f"  找到 {len(download_dirs)} 个下载目录")

    # 分析最新的下载目录
    print("\n[2/3] 分析最新的下载...")
    latest_dir = download_dirs[0]
    print(f"  目录: {latest_dir}")
    print(f"  创建时间: {latest_dir.stat().st_mtime}")

    result = analyze_directory(latest_dir)
    if not result:
        print("  目录分析失败")
        return

    # 显示结果
    print("\n[3/3] 下载结果:")
    print(f"  总文件数: {result['file_count']} 个")
    print(f"  总大小: {format_size(result['total_size'])}")

    if result['file_count'] > 0:
        print("\n文件列表:")
        for i, file in enumerate(result['files'], 1):
            size = file.stat().st_size
            size_str = format_size(size)
            rel_path = file.relative_to(latest_dir)

            # 检查是否为模拟文件
            is_simulated = False
            try:
                if size < 100:  # 小文件可能是模拟文件
                    content = file.read_text(errors='ignore')
                    if content.startswith("模拟下载"):
                        is_simulated = True
            except:
                pass

            status = "[模拟]" if is_simulated else "[真实]"
            print(f"  {i:2d}. {status} {rel_path} ({size_str})")

    print("\n" + "=" * 70)
    print(f"分析完成！文件保存在: {latest_dir}")
    print("=" * 70)

    # 提示清理
    print(f"\n如需清理临时文件，请手动删除该目录")
    print(f"或者运行: rmdir /s /q \"{latest_dir}\"")

if __name__ == "__main__":
    main()
