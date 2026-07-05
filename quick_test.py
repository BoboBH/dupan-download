#!/usr/bin/env python
"""快速测试修复效果"""
import sys
import os
from pathlib import Path
import tempfile
import shutil

# 添加项目路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from dupan_download.utils import sanitize_filename, ensure_path_safe, create_temp_dir

    # 测试长文件名处理
    long_filename = "Goldman Sachs-ASIA~PACIFIC WEEKLY KICKSTART：MXAPJ closed 1% higher in a volatile week， marked by sharp momentum reversals in memory semis and another week of significant foreign outflows from Korea and Taiwan-260703.pdf"

    print("原始文件名长度:", len(long_filename))
    print("清理后长度:", len(sanitize_filename(long_filename)))

    # 测试临时目录创建
    temp_dir = create_temp_dir()
    print("临时目录:", temp_dir)
    print("临时目录名长度:", len(str(temp_dir.name)))

    # 模拟完整路径
    full_path = temp_dir / long_filename
    print("完整路径长度:", len(str(full_path)))

    # 测试安全路径
    safe_path = ensure_path_safe(full_path)
    print("安全路径长度:", len(str(safe_path)))

    # 清理
    try:
        shutil.rmtree(temp_dir)
    except:
        pass

    if len(str(safe_path)) <= 260:
        print("修复效果验证: ✅ 路径已缩短到安全范围内")
    else:
        print("修复效果验证: ❌ 路径仍然过长")

except Exception as e:
    print(f"测试出错: {e}")
    import traceback
    traceback.print_exc()