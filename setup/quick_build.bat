@echo off
REM 快速打包脚本 - 解决常见打包问题
echo ====================================
echo 百度网盘下载工具 - 快速打包脚本
echo ====================================
echo.

REM 检查Python环境
echo 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python环境
    echo 请先安装Python 3.8+
    pause
    exit /b 1
)
echo Python环境正常
echo.

REM 清理旧文件
echo 清理旧的打包文件...
if exist build rmdir /s /q build 2>nul
if exist dist rmdir /s /q dist 2>nul

REM 检查必要文件
echo 检查必要文件...
if not exist "dupan_download\integrated_cli.py" (
    echo 错误: 找不到主程序文件
    pause
    exit /b 1
)
if not exist "build.spec" (
    echo 错误: 找不到打包配置文件
    pause
    exit /b 1
)
echo 必要文件检查完成
echo.

REM 运行打包
echo ====================================
echo 开始打包...
echo ====================================
echo.

REM 使用PyInstaller打包
pyinstaller build.spec

if %errorlevel% neq 0 (
    echo.
    echo ====================================
    echo 打包失败！
    echo ====================================
    echo.
    echo 可能的原因:
    echo 1. 缺少依赖库
    echo 2. Python版本不兼容
    echo 3. 文件路径问题
    echo.
    echo 请检查上面的错误信息
    pause
    exit /b 1
)

echo.
echo ====================================
echo 打包成功！
echo ====================================
echo.
echo 可执行文件: dist\pan-download.exe
echo.

REM 自动复制到发布包
echo 复制到发布包...
if exist "dist\pan-download.exe" (
    if not exist "release_1.0.0_20260702\dupan-download-windows" mkdir "release_1.0.0_20260702\dupan-download-windows"
    copy "dist\pan-download.exe" "release_1.0.0_20260702\dupan-download-windows\" >nul
    echo 已复制到发布包目录
) else (
    echo 警告: 未找到生成的exe文件
)

echo.
echo ====================================
echo 打包完成！
echo ====================================
echo.
echo 文件位置:
echo   - 程序: dist\pan-download.exe
echo   - 发布包: release_1.0.0_20260702\dupan-download-windows\
echo.
echo 下一步:
echo   1. 测试: dist\pan-download.exe --help
echo   2. 安装: cd release_1.0.0_20260702\dupan-download-windows && install.bat
echo.
pause