#!/usr/bin/env python
"""测试长文件名修复效果"""
import sys
import os
from pathlib import Path
import tempfile
import shutil

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from dupan_download.utils import sanitize_filename, ensure_path_safe, create_temp_dir

def test_bypy_scenario():
    """测试模拟bypy下载长文件名的场景"""
    print("=" * 60)
    print("测试BYPY长文件名处理")
    print("=" * 60)

    # 模拟用户的具体问题
    long_filename = "Goldman Sachs-ASIA~PACIFIC WEEKLY KICKSTART：MXAPJ closed 1% higher in a volatile week， marked by sharp momentum reversals in memory semis and another week of significant foreign outflows from Korea and Taiwan-260703.pdf"

    print(f"\n原始文件名长度: {len(long_filename)} 字符")
    print(f"文件名: {long_filename[:50]}...")

    # 测试1: 使用新的临时目录创建方法
    print("\n" + "=" * 60)
    print("测试1: 新的临时目录创建方法")
    print("=" * 60)

    temp_dir = create_temp_dir()
    print(f"临时目录: {temp_dir}")
    print(f"临时目录名称长度: {len(str(temp_dir.name))} 字符")

    # 模拟bypy创建长文件名
    simulated_file = temp_dir / long_filename
    full_path_length = len(str(simulated_file))

    print(f"完整路径长度: {full_path_length} 字符")

    if full_path_length > 260:
        print(f"⚠️  路径超过MAX_PATH限制 ({full_path_length} > 260)")

        # 测试我们的清理功能
        safe_path = ensure_path_safe(simulated_file)
        print(f"安全路径: {safe_path}")
        print(f"安全路径长度: {len(str(safe_path))} 字符")

        if len(str(safe_path)) <= 260:
            print(f"✅ 路径已缩短到安全范围内")
        else:
            print(f"❌ 路径仍然过长")

    # 测试2: 尝试创建文件（模拟bypy行为）
    print("\n" + "=" * 60)
    print("测试2: 模拟文件创建")
    print("=" * 60)

    try:
        # 首先尝试创建原始长文件名（会失败）
        temp_dir.mkdir(parents=True, exist_ok=True)
        simulated_file.write_text("test content")
        print(f"✅ 意外成功创建长文件名: {simulated_file.name[:50]}...")
        simulated_file.unlink()

    except Exception as e:
        print(f"❌ 创建长文件名失败（预期）: {e}")

        # 现在尝试使用清理后的文件名
        safe_filename = sanitize_filename(long_filename)
        safe_file = temp_dir / safe_filename

        print(f"\n尝试创建清理后的文件名...")
        print(f"清理后文件名: {safe_filename[:50]}...")
        print(f"清理后长度: {len(safe_filename)} 字符")

        try:
            safe_file.write_text("test content")
            print(f"✅ 成功创建清理后的文件")
            print(f"文件大小: {safe_file.stat().st_size} bytes")

            # 清理
            safe_file.unlink()
            shutil.rmtree(temp_dir)

        except Exception as e2:
            print(f"❌ 创建清理后文件也失败: {e2}")

    # 测试3: 完整工作流程模拟
    print("\n" + "=" * 60)
    print("测试3: 完整工作流程模拟")
    print("=" * 60)

    # 模拟bypy下载过程
    temp_dir_for_bypy = create_temp_dir()
    print(f"为bypy创建临时目录: {temp_dir_for_bypy}")

    # 模拟bypy下载后立即清理
    print("\n模拟bypy下载完成，开始清理文件名...")

    try:
        # 创建一个长文件名文件（模拟bypy下载）
        temp_dir_for_bypy.mkdir(parents=True, exist_ok=True)
        long_file = temp_dir_for_bypy / long_filename

        # 这会失败，所以bypy会报错
        try:
            long_file.write_text("content")
            print(f"bypy成功创建文件: {long_file.name[:50]}...")
        except:
            print(f"bypy创建长文件名失败（这是预期情况）")

            # 我们的修复：在bypy下载后立即检查并清理
            print("\n执行我们的修复逻辑...")

            # 检查目录中的文件
            files_in_dir = list(temp_dir_for_bypy.rglob('*'))
            files_in_dir = [f for f in files_in_dir if f.is_file()]

            print(f"目录中的文件数量: {len(files_in_dir)}")

            # 由于文件创建失败，我们直接测试清理逻辑
            safe_filename = sanitize_filename(long_filename)
            print(f"清理后的文件名: {safe_filename[:50]}...")
            print(f"清理后长度: {len(safe_filename)} 字符")

            # 计算安全路径
            safe_path = temp_dir_for_bypy / safe_filename
            if len(str(safe_path)) <= 260:
                print(f"✅ 清理后的路径在安全范围内: {len(str(safe_path))} 字符")
            else:
                print(f"❌ 清理后的路径仍然过长: {len(str(safe_path))} 字符")

    finally:
        # 清理
        try:
            shutil.rmtree(temp_dir_for_bypy)
        except:
            pass

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == '__main__':
    try:
        test_bypy_scenario()
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)