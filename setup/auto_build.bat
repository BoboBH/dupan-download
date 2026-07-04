@echo off
REM ============================================
REM 百度网盘下载工具 - 完整打包脚本
REM ============================================
REM 这个脚本可以在任何Windows机器上运行
REM 只需要Python 3.8+环境
REM ============================================

echo.
echo ====================================
echo 百度网盘下载工具 - 自动打包脚本
echo ====================================
echo.

REM 保存当前目录
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo 工作目录: %CD%
echo.

REM ====================================
REM 步骤 1: 环境检查
REM ============================================
echo [1/6] 检查Python环境...

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Python
    echo.
    echo 请先安装Python 3.8或更高版本
    echo 下载地址: https://www.python.org/downloads/
    echo 安装时请勾选 "Add Python to PATH"
    pause
    exit /b 1
)

python --version
echo ✅ Python环境检查通过
echo.

REM ====================================
REM 步骤 2: 安装依赖
REM ============================================
echo [2/6] 检查和安装依赖...
echo.

echo 安装打包依赖...
pip install pyinstaller pywin32 --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    echo ⚠️  pip安装可能有问题，尝试继续...
)

echo 安装项目依赖...
pip install bypy click paramiko requests tqdm python-dotenv --quiet --disable-pip-version-check
if %errorlevel% neq 0 (
    echo ⚠️  部分依赖安装可能有问题，尝试继续...
)

echo ✅ 依赖检查完成
echo.

REM ====================================
REM 步骤 3: 清理旧文件
REM ============================================
echo [3/6] 清理旧的打包文件...
echo.

if exist build (
    echo 清理 build 目录...
    rmdir /s /q build 2>nul
)

if exist dist (
    echo 清理 dist 目录...
    rmdir /s /q dist 2>nul
)

echo ✅ 清理完成
echo.

REM ====================================
REM 步骤 4: 验证文件
REM ============================================
echo [4/6] 验证必要文件...
echo.

if not exist "build.spec" (
    echo ❌ 错误: 找不到 build.spec 文件
    echo 请确保在项目根目录运行此脚本
    pause
    exit /b 1
)

if not exist "dupan_download\integrated_cli.py" (
    echo ❌ 错误: 找不到主程序文件
    pause
    exit /b 1
)

echo ✅ 文件验证通过
echo.

REM ====================================
REM 步骤 5: 打包程序
REM ============================================
echo [5/6] 开始打包...
echo.
echo 这可能需要几分钟时间，请耐心等待...
echo.

pyinstaller build.spec --clean --noconfirm

if %errorlevel% neq 0 (
    echo.
    echo ====================================
    echo ❌ 打包失败！
    echo ====================================
    echo.
    echo 可能的原因:
    echo   1. Python版本不兼容（建议使用3.8-3.11）
    echo   2. 缺少必要的依赖库
    echo   3. 文件路径或权限问题
    echo.
    echo 请查看上面的错误信息
    pause
    exit /b 1
)

echo.
echo ====================================
echo ✅ 打包成功！
echo ====================================
echo.

REM ====================================
REM 步骤 6: 复制到发布包
REM ============================================
echo [6/6] 复制到发布包...
echo.

if exist "dist\pan-download.exe" (
    echo 主程序: dist\pan-download.exe

    REM 创建发布包目录
    if not exist "release_1.0.0_20260702\dupan-download-windows" mkdir "release_1.0.0_20260702\dupan-download-windows"

    REM 复制主程序
    copy "dist\pan-download.exe" "release_1.0.0_20260702\dupan-download-windows\" >nul
    echo ✅ 已复制到发布包目录

    REM 复制配置文件
    if exist ".env.example" copy ".env.example" "release_1.0.0_20260702\dupan-download-windows\" >nul
    if exist "README.md" copy "README.md" "release_1.0.0_20260702\dupan-download-windows\" >nul

    echo ✅ 发布包已准备完成
) else (
    echo ❌ 错误: 未找到生成的exe文件
    echo 请检查打包过程是否有错误
    pause
    exit /b 1
)

echo.
echo ====================================
echo 🎉 打包完成！
echo ====================================
echo.
echo 📦 生成文件:
echo    主程序: dist\pan-download.exe
echo    发布包: release_1.0.0_20260702\dupan-download-windows\
echo.
echo 🚀 下一步:
echo    1. 测试程序: dist\pan-download.exe --help
echo    2. 复制到目标机: 整个 release_1.0.0_20260702\dupan-download-windows 文件夹
echo    3. 在目标机运行: install.bat
echo.

REM 测试程序
echo 测试程序...
if exist "dist\pan-download.exe" (
    dist\pan-download.exe --help >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ 程序测试通过
    ) else (
        echo ⚠️  程序可能有问题，请手动测试
    )
)

echo.
pause