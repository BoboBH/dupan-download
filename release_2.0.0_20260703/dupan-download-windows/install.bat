@echo off
REM ============================================
REM 百度网盘下载工具 - 一键安装脚本 v2.0.0
REM ============================================

echo.
echo ====================================
echo 百度网盘下载工具 - 一键安装向导 v2.0.0
echo ====================================
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo 提示: 建议以管理员身份运行此脚本
    echo.
)

REM 设置安装目录
set INSTALL_DIR=D:\baidu-download
set EXE_NAME=pan-download.exe

echo 安装目录: %INSTALL_DIR%
echo 版本: 2.0.0
echo.

REM 创建安装目录
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo 正在创建安装目录...
if exist "%INSTALL_DIR%" (
    echo ✅ 目录已存在: %INSTALL_DIR%
) else (
    echo ✅ 目录创建成功: %INSTALL_DIR%
)
echo.

REM 检查主程序
if not exist "%EXE_NAME%" (
    echo ❌ 错误: 找不到主程序 %EXE_NAME%
    echo.
    echo 当前目录: %CD%
    echo.
    echo 请确保在正确的目录运行此脚本
    echo 或先运行打包脚本生成程序
    echo.
    pause
    exit /b 1
)

echo 正在复制程序文件...
copy "%EXE_NAME%" "%INSTALL_DIR%\" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 主程序复制成功
) else (
    echo ❌ 主程序复制失败
    pause
    exit /b 1
)

echo 正在复制配置文件...
if exist .env.example copy .env.example "%INSTALL_DIR%\" >nul 2>&1
if exist README.md copy README.md "%INSTALL_DIR%\" >nul 2>&1
if exist docs\README.md copy docs\README.md "%INSTALL_DIR%\" >nul 2>&1
echo ✅ 配置文件复制完成

REM 添加到PATH
echo.
echo 正在添加到系统PATH...
setx PATH "%PATH%;%INSTALL_DIR%" /M >nul 2>&1
if %errorlevel% neq 0 (
    echo 警告: 无法修改系统PATH，需要管理员权限
    echo 请手动添加 %INSTALL_DIR% 到系统PATH
) else (
    echo ✅ 已添加到系统PATH
)

echo.
echo ====================================
echo ✅ 安装完成！
echo ====================================
echo.
echo 安装位置: %INSTALL_DIR%
echo 可执行文件: %INSTALL_DIR%\%EXE_NAME%
echo 版本: 2.0.0
echo.

REM 显示安装结果
echo.
echo ====================================
echo 📁 安装目录内容
echo ====================================
dir "%INSTALL_DIR%"
echo.

echo ====================================
echo 🚀 下一步操作
echo ====================================
echo.
echo 1. 配置百度网盘认证:
echo    pan-download --setup-bypy
echo.
echo 2. 配置SFTP服务器:
echo    编辑 %INSTALL_DIR%\.env 文件
echo.
echo 3. 测试配置:
echo    pan-download --test-config
echo.
echo 4. 开始使用:
echo    pan-download apps/bypy/test_pdf --upload-sftp
echo.

REM 打开安装目录
echo ====================================
echo 📂 打开安装目录...
echo.

explorer "%INSTALL_DIR%"

echo.
echo 安装完成！请检查程序是否正常运行。
pause