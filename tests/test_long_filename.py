#!/usr/bin/env python
"""测试长文件名处理"""
import os
import sys
import tempfile
import shutil
from pathlib import Path

# 模拟用户提供的长文件名
LONG_FILENAME = "Goldman Sachs-ASIA~PACIFIC WEEKLY KICKSTART：MXAPJ closed 1% higher in a volatile week， marked by sharp momentum reversals in memory semis and another week of significant foreign outflows from Korea and Taiwan-260703.pdf"

def test_filename_length():
    """测试文件名长度"""
    print("=" * 60)
    print("文件名长度测试")
    print("=" * 60)

    print(f"\n原始文件名长度: {len(LONG_FILENAME)} 字符")
    print(f"文件名内容: {LONG_FILENAME}")

    # 测试1：检查文件名是否超过限制
    print("\n1. 检查文件名限制...")

    # Windows文件名最大长度（不含路径）
    max_filename_length = 255

    # Windows完整路径最大长度（MAX_PATH）
    max_path_length = 260

    if len(LONG_FILENAME) > max_filename_length:
        print(f"   [X] 文件名超过 {max_filename_length} 字符限制")
        print(f"   超过: {len(LONG_FILENAME) - max_filename_length} 字符")
    else:
        print(f"   [OK] 文件名在 {max_filename_length} 字符限制内")

    # 测试2：尝试创建文件
    print("\n2. 尝试在不同场景下创建文件...")

    scenarios = [
        ("临时目录", tempfile.gettempdir()),
        ("当前目录", os.getcwd()),
        ("长路径子目录", "test_" + "x" * 100)  # 创建一个长路径
    ]

    for scenario_name, base_path in scenarios:
        print(f"\n   场景: {scenario_name}")
        print(f"   基础路径: {base_path}")

        try:
            # 创建测试目录
            test_dir = Path(base_path) / "long_filename_test"
            test_dir.mkdir(parents=True, exist_ok=True)

            # 尝试创建长文件名
            test_file = test_dir / LONG_FILENAME

            full_path_str = str(test_file)
            full_path_length = len(full_path_str)

            print(f"   完整路径长度: {full_path_length} 字符")

            if full_path_length > max_path_length:
                print(f"   [WARNING] 完整路径超过 {max_path_length} 字符限制")

            # 尝试创建文件
            try:
                test_file.write_text("test content")
                print(f"   [OK] 成功创建文件: {test_file.name[:50]}...")

                # 验证文件是否真的存在
                if test_file.exists():
                    print(f"   [OK] 文件确实存在")
                    size = test_file.stat().st_size
                    print(f"   文件大小: {size} bytes")
                else:
                    print(f"   [X] 文件创建成功但无法访问")

                # 清理
                test_file.unlink()

            except FileNotFoundError as e:
                print(f"   [X] FileNotFoundError: {e}")
                print(f"   可能原因：路径太长或文件名无效")

            except OSError as e:
                print(f"   [X] OSError: {e}")
                print(f"   可能原因：文件名或路径超过系统限制")

            except Exception as e:
                print(f"   [X] 其他错误: {type(e).__name__}: {e}")

            # 清理目录
            try:
                shutil.rmtree(test_dir)
            except:
                pass

        except Exception as e:
            print(f"   [X] 设置测试环境失败: {e}")

    # 测试3：测试各种文件名处理策略
    print("\n3. 测试文件名处理策略...")

    strategies = [
        ("原始", LONG_FILENAME),
        ("截断到100字符", LONG_FILENAME[:100] + ".pdf"),
        ("截断到150字符", LONG_FILENAME[:150] + ".pdf"),
        ("截断到200字符", LONG_FILENAME[:200] + ".pdf"),
        ("保留文件扩展名", LONG_FILENAME[:200] + ".pdf"),
    ]

    for strategy_name, modified_filename in strategies:
        print(f"\n   策略: {strategy_name}")
        print(f"   长度: {len(modified_filename)} 字符")

        # 创建测试目录
        test_dir = Path(tempfile.gettempdir()) / "long_filename_strategy_test"
        test_dir.mkdir(exist_ok=True)

        try:
            test_file = test_dir / modified_filename
            test_file.write_text("test")
            print(f"   [OK] 成功: {modified_filename[:50]}...")
            test_file.unlink()
        except Exception as e:
            print(f"   [X] 失败: {e}")

    # 清理
    try:
        shutil.rmtree(test_dir)
    except:
        pass

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == '__main__':
    try:
        test_filename_length()
    except Exception as e:
        print(f"测试脚本执行失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)