@echo off
chcp 65001 > nul
REM ============================================
REM 百度网盘下载工具启动脚本
REM ============================================

echo.
echo ====================================
REM 百度网盘下载工具 - 启动脚本
REM ====================================
echo.
echo 版本: 2.0.1 (2026-07-05)
echo 包含长文件名修复
echo.

REM 检查Python环境
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到Python环境
    echo 请确保已安装Python 3.8或更高版本
    echo.
    pause
    exit /b 1
)

echo [信息] Python环境检测成功
echo.

REM 运行主程序
echo [信息] 启动百度网盘下载工具...
echo.
python -m dupan_download.integrated_cli %*

if %errorlevel% neq 0 (
    echo.
    echo [错误] 程序执行失败，错误代码: %errorlevel%
    echo.
    pause
    exit /b %errorlevel%
)

echo.
echo [信息] 程序执行完成
echo.
pause