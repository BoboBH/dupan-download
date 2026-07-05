@echo off
chcp 65001 > nul
REM ============================================
REM 安装Python依赖脚本
REM ============================================

echo.
echo ====================================
REM 安装Python依赖
REM ====================================
echo.
echo 这将安装项目所需的Python包
echo.

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未找到Python环境
    echo 请先安装Python 3.8或更高版本
    echo.
    pause
    exit /b 1
)

echo [信息] 正在安装依赖包...
echo.

pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo [成功] 依赖安装完成
    echo.
    echo 现在可以运行 "启动工具.bat" 来使用程序
    echo.
) else (
    echo.
    echo [错误] 依赖安装失败
    echo 请检查网络连接或权限设置
    echo.
)

pause