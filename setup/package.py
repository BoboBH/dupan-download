#!/usr/bin/env python3
"""
自动化打包脚本

功能：
1. 自动升级版本号
2. 编译可执行文件
3. 创建包含所有必要文件的ZIP包
4. 生成使用说明

使用方法：
    python setup/package.py           # 自动执行完整打包流程
    python setup/package.py --version  # 只显示当前版本
    python setup/package.py --bump     # 只升级版本号
"""
import os
import sys
import re
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
import subprocess
import argparse

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
VERSION_FILE = PROJECT_ROOT / "dupan_download" / "__init__.py"
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"


def get_current_version():
    """获取当前版本号"""
    content = VERSION_FILE.read_text(encoding='utf-8')
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    return "未知版本"


def bump_version():
    """升级版本号（例如：2.1.0 -> 2.1.1）"""
    current = get_current_version()
    parts = current.split('.')

    if len(parts) >= 3:
        # 升级最后一位（修订版本）
        parts[-1] = str(int(parts[-1]) + 1)
        new_version = '.'.join(parts)
    else:
        # 如果版本号格式不标准，添加修订版本
        new_version = current + ".1"

    # 更新版本文件
    content = VERSION_FILE.read_text(encoding='utf-8')
    content = re.sub(
        r'(__version__\s*=\s*["\'])([^"\']+)(["\'])',
        rf'\g<1>{new_version}\g<3>',
        content
    )
    VERSION_FILE.write_text(content, encoding='utf-8')

    print(f"版本升级: {current} -> {new_version}")
    return new_version


def build_exe():
    """编译可执行文件"""
    print("开始编译可执行文件...")

    # 清理旧的构建文件
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)

    # 运行PyInstaller
    spec_file = PROJECT_ROOT / "setup" / "build.spec"
    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", str(spec_file), "--clean"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("编译失败！")
        print(result.stderr)
        return False

    print("[OK] 编译成功")
    return True


def create_usage_guide(version):
    """创建使用说明文档"""
    guide_content = f"""# 百度网盘下载工具 v{version} - 使用说明

## 快速开始

### 1. 环境准备
- Windows 10/11
- 无需安装Python或其他依赖

### 2. 配置文件
复制 `.env.example` 为 `.env` 并配置必要参数：

```bash
# 百度网盘配置（可选）
# BAIDU_BDUSS=your_bduss_here
# BAIDU_COOKIES=your_cookies_here

# SFTP服务器配置（必需）
SFTP_HOST=your_sftp_host
SFTP_PORT=22
SFTP_USERNAME=your_username
SFTP_PASSWORD=your_password
SFTP_REMOTE_PATH=/remote/path

# 其他配置
TIMEOUT=300
MAX_RETRIES=5
```

### 3. 百度网盘认证

#### 方法一：环境变量配置（推荐）
在 `.env` 文件中设置：
- `BAIDU_BDUSS`: 浏览器开发者工具中获取
- `BAIDU_COOKIES`: 完整的Cookie字符串

#### 方法二：使用认证向导
```bash
pan-download.exe --setup-bypi
```

### 4. 基本使用

#### 只下载文件
```bash
pan-download.exe apps/bypy/folder_name
```

#### 下载并上传到SFTP
```bash
pan-download.exe apps/bypy/folder_name --upload-sftp
```

#### 保留临时文件
```bash
pan-download.exe apps/bypy/folder_name --upload-sftp --keep-temp
```

#### 详细日志输出
```bash
pan-download.exe apps/bypy/folder_name --upload-sftp --verbose
```

### 5. 高级功能

#### 流式处理模式
下载一个文件后立即上传，节省磁盘空间：
```bash
pan-download.exe apps/bypy/folder_name --upload-sftp --streaming
```

#### 测试配置
验证配置是否正确：
```bash
pan-download.exe --test-config
```

### 6. 常见问题

#### 问题：下载失败，文件名太长
**解决方案**：工具自动使用简短临时路径（如 `d:\\a`），避免Windows路径长度限制。

#### 问题：认证失败
**解决方案**：
1. 检查 `.env` 文件配置
2. 运行 `pan-download.exe --test-config` 测试
3. 重新运行 `pan-download.exe --setup-bypi`

#### 问题：SFTP连接失败
**解决方案**：
1. 检查SFTP服务器地址、端口、用户名、密码
2. 确认网络连接正常
3. 检查防火墙设置

### 7. 统计信息说明

处理完成后会显示详细统计：
- **总文件数**: 处理的文件总数
- **已上传**: 成功上传到SFTP的文件数
- **完全跳过**: 本地和SFTP都存在的文件（跳过处理）
- **下载失败**: 下载失败的文件数
- **上传失败**: 上传失败的文件数

如果有失败文件，会显示详细的失败文件列表。

### 8. 技术特性

- [OK] 支持长文件名（220字符）
- [OK] 自动管理临时目录
- [OK] 流式处理，节省磁盘空间
- [OK] 详细错误报告
- [OK] 自动重试机制
- [OK] 进度实时显示

### 9. 版本信息

- **当前版本**: v{version}
- **编译时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Python版本**: 3.12

### 10. 支持和反馈

如有问题或建议，请联系开发团队。

---
**百度网盘下载工具** - 自动化文件传输解决方案
"""

    guide_file = PROJECT_ROOT / "使用说明.txt"
    guide_file.write_text(guide_content, encoding='utf-8')
    print(f"[OK] 使用说明已创建: {guide_file}")
    return guide_file


def create_package(version):
    """创建ZIP包"""
    print(f"创建版本 {version} 的发布包...")

    # 创建临时目录
    temp_dir = DIST_DIR / f"dupan-download-v{version}-windows"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True, exist_ok=True)

    # 复制文件
    files_to_copy = {
        "dist/pan-download.exe": "pan-download.exe",
        ".env.example": ".env.example",
        "使用说明.txt": "使用说明.txt",
    }

    for src, dst in files_to_copy.items():
        src_path = PROJECT_ROOT / src
        dst_path = temp_dir / dst
        if src_path.exists():
            if src_path.is_file():
                shutil.copy2(src_path, dst_path)
                print(f"[OK] 复制: {dst}")
            else:
                shutil.copytree(src_path, dst_path)
                print(f"[OK] 复制目录: {dst}")
        else:
            print(f"[WARNING] 文件不存在: {src}")

    # 创建README快速开始指南
    readme_content = f"""# 百度网盘下载工具 v{version}

## 快速开始

1. 配置文件：复制 `.env.example` 为 `.env` 并配置SFTP信息
2. 运行测试：`pan-download.exe --test-config`
3. 开始使用：`pan-download.exe apps/bypy/folder_name --upload-sftp`

详细说明请查看 `使用说明.txt`

## 文件说明

- `pan-download.exe`: 主程序
- `.env.example`: 配置文件模板
- `使用说明.txt`: 详细使用说明

## 系统要求

- Windows 10/11
- 无需安装Python

## 版本信息

- 版本: v{version}
- 发布日期: {datetime.now().strftime('%Y-%m-%d')}

---
自动化文件传输解决方案
"""

    readme_file = temp_dir / "README.md"
    readme_file.write_text(readme_content, encoding='utf-8')
    print(f"[OK] 创建: README.md")

    # 创建ZIP文件（直接生成到dist目录）
    zip_file = DIST_DIR / f"dupan-download-v{version}-windows.zip"
    if zip_file.exists():
        zip_file.unlink()

    with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in temp_dir.rglob('*'):
            if file.is_file():
                arcname = file.relative_to(temp_dir)
                zipf.write(file, arcname)
                print(f"[PACKAGE] 打包: {arcname}")

    print(f"[OK] ZIP包创建成功: {zip_file}")
    print(f"[INFO] 文件大小: {zip_file.stat().st_size / 1024 / 1024:.2f} MB")

    # 清理临时目录
    shutil.rmtree(temp_dir)
    print(f"[CLEAN] 已清理临时目录")

    return zip_file


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='打包工具')
    parser.add_argument('--version', action='store_true', help='显示当前版本')
    parser.add_argument('--bump', action='store_true', help='升级版本号')
    parser.add_argument('--build', action='store_true', help='只编译，不打包')
    parser.add_argument('--package', action='store_true', help='只打包，不编译')
    parser.add_argument('--full', action='store_true', help='完整打包流程（默认）')

    args = parser.parse_args()

    # 显示版本
    if args.version:
        print(f"当前版本: {get_current_version()}")
        return

    # 只升级版本号
    if args.bump:
        new_version = bump_version()
        print(f"版本已升级到: {new_version}")
        return

    # 只编译
    if args.build:
        if not build_exe():
            sys.exit(1)
        print("编译完成")
        return

    # 只打包
    if args.package:
        version = get_current_version()
        create_usage_guide(version)
        create_package(version)
        return

    # 完整打包流程（默认）
    print("=" * 60)
    print("自动化打包流程")
    print("=" * 60)
    print(f"当前版本: {get_current_version()}")
    print()

    # 1. 升级版本号
    print("步骤 1/5: 升级版本号")
    new_version = bump_version()
    print()

    # 2. 编译可执行文件
    print("步骤 2/5: 编译可执行文件")
    if not build_exe():
        print("[ERROR] 编译失败，终止流程")
        sys.exit(1)
    print()

    # 3. 创建使用说明
    print("步骤 3/5: 创建使用说明")
    create_usage_guide(new_version)
    print()

    # 4. 创建发布包
    print("步骤 4/5: 创建发布包")
    create_package(new_version)
    print()

    # 5. 复制到.venv/Scripts
    print("步骤 5/5: 更新本地可执行文件")
    exe_src = PROJECT_ROOT / "dist" / "pan-download.exe"
    exe_dst = PROJECT_ROOT / ".venv" / "Scripts" / "pan-download.exe"
    if exe_src.exists():
        shutil.copy2(exe_src, exe_dst)
        print(f"[OK] 已更新: {exe_dst}")
    print()

    print("=" * 60)
    print("[SUCCESS] 打包完成！")
    print("=" * 60)
    print(f"版本: v{new_version}")
    print(f"发布包: dupan-download-v{new_version}-windows.zip")
    print(f"可执行文件: dist/pan-download.exe")
    print(f"本地更新: .venv/Scripts/pan-download.exe")
    print()

    # 显示文件信息
    zip_file = DIST_DIR / f"dupan-download-v{new_version}-windows.zip"
    if zip_file.exists():
        print("[INFO] 发布包信息:")
        print(f"   文件: {zip_file.name}")
        print(f"   大小: {zip_file.stat().st_size / 1024 / 1024:.2f} MB")
        print(f"   位置: {zip_file}")


if __name__ == "__main__":
    main()