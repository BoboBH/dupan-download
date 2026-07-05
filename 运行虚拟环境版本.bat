@echo off
chcp 65001 > nul
REM ============================================
REM 虚拟环境中启动百度网盘下载工具
REM ============================================

echo.
echo ====================================
REM 虚拟环境启动脚本
REM ====================================
echo.
echo 版本: 2.0.1 (2026-07-05)
echo 包含长文件名修复
echo.

REM 检查虚拟环境
if not exist ".venv\Scripts\activate.bat" (
    echo [错误] 未找到虚拟环境
    echo 请先创建虚拟环境: python -m venv .venv
    echo.
    pause
    exit /b 1
)

echo [信息] 激活虚拟环境...
call .venv\Scripts\activate.bat

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