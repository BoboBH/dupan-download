#!/usr/bin/env python3
"""搜索百度网盘中包含260701的文件夹"""
import sys
import os

# 尝试导入bypy
try:
    from bypy import bypy
    bp = bypy.ByPy()
    print("bypy库导入成功")
except ImportError as e:
    print(f"无法导入bypy: {e}")
    print("尝试使用命令行方式...")
    import subprocess

    def run_command(cmd):
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr

    # 列出根目录
    print("\n根目录:")
    output = run_command(".venv/Scripts/bypy.exe list")
    print(output)

    # 搜索
    print("\n搜索260701:")
    output = run_command(".venv/Scripts/bypy.exe search 260701")
    print(output)

    sys.exit(0)

# 使用bypy库
def search_files(keyword, path="/", depth=0, max_depth=3):
    """递归搜索文件"""
    if depth > max_depth:
        return []

    print(f"搜索: {path} (深度: {depth})")

    try:
        # 列出目录
        files = bp.list(path)
        if not files:
            return []

        results = []

        for file in files:
            if isinstance(file, dict):
                name = file.get('name', file.get('server_filename', ''))
                is_dir = file.get('is_dir', file.get('isdir', 0)) == 1
                full_path = file.get('path', f"{path}/{name}".replace('//', '/'))

                if keyword in name:
                    results.append({
                        'name': name,
                        'path': full_path,
                        'is_dir': is_dir
                    })
                    print(f"  找到: {full_path}")

                # 递归搜索子目录
                if is_dir:
                    sub_results = search_files(keyword, full_path, depth + 1, max_depth)
                    results.extend(sub_results)

        return results

    except Exception as e:
        print(f"搜索出错: {e}")
        return []

def main():
    print("开始搜索包含 '260701' 的文件...")
    print("=" * 60)

    results = search_files('260701', max_depth=4)

    if results:
        print(f"\n找到 {len(results)} 个结果:")
        for item in results:
            print(f"  {'[目录]' if item['is_dir'] else '[文件]'} {item['path']}")

        # 详细查看目录内容
        print("\n" + "=" * 60)
        for item in results:
            if item['is_dir']:
                print(f"\n目录内容: {item['path']}")
                print("-" * 40)
                try:
                    contents = bp.list(item['path'])
                    for file in contents:
                        if isinstance(file, dict):
                            name = file.get('name', file.get('server_filename', ''))
                            size = file.get('size', 0)
                            print(f"  {name}: {size} bytes")
                except Exception as e:
                    print(f"  无法列出内容: {e}")
    else:
        print("未找到包含 '260701' 的文件")

if __name__ == '__main__':
    main()