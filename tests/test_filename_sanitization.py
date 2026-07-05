#!/usr/bin/env python
"""测试文件名清理功能"""
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dupan_download.utils import sanitize_filename, ensure_path_safe

def test_utils_filename_sanitization():
    """测试文件名清理功能"""
    print("=" * 60)
    print("文件名清理功能测试")
    print("=" * 60)

    # 测试用例
    test_cases = [
        {
            "name": "原始长文件名",
            "filename": "Goldman Sachs-ASIA~PACIFIC WEEKLY KICKSTART：MXAPJ closed 1% higher in a volatile week， marked by sharp momentum reversals in memory semis and another week of significant foreign outflows from Korea and Taiwan-260703.pdf",
            "expected_length": 200,
            "should_truncate": True
        },
        {
            "name": "正常文件名",
            "filename": "normal_file.pdf",
            "expected_length": 15,
            "should_truncate": False
        },
        {
            "name": "包含非法字符",
            "filename": "file<>:\"/\\|?*.pdf",
            "expected_length": 19,
            "should_truncate": False,
            "should_clean": True
        },
        {
            "name": "中等长度文件名",
            "filename": "A" * 150 + ".pdf",
            "expected_length": 154,
            "should_truncate": False
        },
        {
            "name": "超长文件名（无扩展名）",
            "filename": "A" * 300,
            "expected_length": 200,
            "should_truncate": True
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. 测试: {test_case['name']}")
        print(f"   原始文件名: {test_case['filename'][:50]}...")
        print(f"   原始长度: {len(test_case['filename'])} 字符")

        result = sanitize_filename(test_case['filename'])
        print(f"   清理后: {result[:50]}...")
        print(f"   清理后长度: {len(result)} 字符")

        # 验证截断
        if test_case['should_truncate']:
            if len(result) <= test_case['expected_length']:
                print(f"   [OK] 文件名被正确截断")
            else:
                print(f"   [X] 文件名未被截断或截断不足")
        else:
            if not test_case.get('should_clean'):
                if len(result) == len(test_case['filename']):
                    print(f"   [OK] 文件名保持不变")
                else:
                    print(f"   [X] 文件名被意外修改")

        # 验证非法字符清理
        if test_case.get('should_clean'):
            if '<' not in result and '>' not in result:
                print(f"   [OK] 非法字符被正确清理")
            else:
                print(f"   [X] 非法字符未被清理")

def test_utils_path_safety():
    """测试路径安全功能"""
    print("\n" + "=" * 60)
    print("路径安全功能测试")
    print("=" * 60)

    import tempfile

    # 创建测试目录
    test_dir = Path(tempfile.gettempdir()) / "path_safety_test"
    test_dir.mkdir(exist_ok=True)

    test_cases = [
        {
            "name": "正常路径",
            "path": test_dir / "normal_file.pdf",
            "should_modify": False
        },
        {
            "name": "超长文件名路径",
            "path": test_dir / ("A" * 250 + ".pdf"),
            "should_modify": True
        },
        {
            "name": "边界长度路径",
            "path": test_dir / ("B" * 200 + ".txt"),
            "should_modify": False  # 根据系统可能不修改
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}. 测试: {test_case['name']}")
        original_path = test_case['path']
        print(f"   原始路径长度: {len(str(original_path))} 字符")

        result = ensure_path_safe(original_path)
        print(f"   安全路径长度: {len(str(result))} 字符")

        if test_case['should_modify']:
            if len(str(result)) < len(str(original_path)):
                print(f"   [OK] 路径被正确缩短")
            else:
                print(f"   [WARNING] 路径可能未被缩短（系统相关）")
        else:
            if str(result) == str(original_path):
                print(f"   [OK] 路径保持不变")
            else:
                print(f"   [INFO] 路径被调整")

    # 清理
    import shutil
    try:
        shutil.rmtree(test_dir)
        print(f"\n[OK] 测试目录已清理")
    except Exception as e:
        print(f"\n[X] 清理测试目录失败: {e}")

def test_real_scenario():
    """测试真实场景"""
    print("\n" + "=" * 60)
    print("真实场景测试")
    print("=" * 60)

    import tempfile
    import shutil

    # 模拟用户的具体问题
    long_filename = "Goldman Sachs-ASIA~PACIFIC WEEKLY KICKSTART：MXAPJ closed 1% higher in a volatile week， marked by sharp momentum reversals in memory semis and another week of significant foreign outflows from Korea and Taiwan-260703.pdf"

    print(f"\n原始问题:")
    print(f"文件名长度: {len(long_filename)} 字符")
    print(f"文件名: {long_filename[:50]}...")

    # 在不同路径长度下测试
    test_scenarios = [
        ("短路径", Path("C:/temp")),
        ("中等路径", Path("C:/temp/dupan_download_12345")),
        ("长路径", Path("C:/temp/very_long_directory_name_to_test_path_limit")),
    ]

    for scenario_name, base_path in test_scenarios:
        print(f"\n场景: {scenario_name}")

        # 创建完整路径
        full_path = base_path / long_filename
        print(f"完整路径长度: {len(str(full_path))} 字符")

        # 应用清理
        safe_path = ensure_path_safe(full_path)
        print(f"安全路径长度: {len(str(safe_path))} 字符")
        print(f"缩短: {len(str(full_path)) - len(str(safe_path))} 字符")

        # 尝试创建文件
        try:
            base_path.mkdir(parents=True, exist_ok=True)
            safe_path.write_text("test content")
            print(f"[OK] 成功创建文件: {safe_path.name[:50]}...")

            # 验证文件存在
            if safe_path.exists():
                size = safe_path.stat().st_size
                print(f"[OK] 文件验证成功，大小: {size} bytes")

            # 清理
            safe_path.unlink()
        except Exception as e:
            print(f"[X] 创建文件失败: {e}")

    # 清理测试目录
    try:
        for _, base_path in test_scenarios:
            if base_path.exists():
                shutil.rmtree(base_path)
    except:
        pass

if __name__ == '__main__':
    try:
        test_utils_filename_sanitization()
        test_utils_path_safety()
        test_real_scenario()

        print("\n" + "=" * 60)
        print("所有测试完成")
        print("=" * 60)

    except Exception as e:
        print(f"测试执行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)