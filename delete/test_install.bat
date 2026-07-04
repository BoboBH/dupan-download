@echo off
REM ============================================
REM 测试安装脚本 - 安装到指定目录进行测试
REM ============================================

echo.
echo ====================================
echo 百度网盘下载工具 - 测试安装脚本
echo ====================================
echo.

REM 检查管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo 提示: 建议以管理员身份运行此脚本
    echo.
    pause
    exit /b 1
)

REM 设置测试安装目录
set INSTALL_DIR=D:\temp\baidu-download
set EXE_NAME=pan-download.exe

echo 测试安装目录: %INSTALL_DIR%
echo.

REM 检查主程序是否存在
if not exist "%EXE_NAME%" (
    echo ⚠️  未找到主程序 %EXE_NAME%
    echo.
    echo 当前目录: %CD%
    echo.

    REM 检查是否有模拟程序
    if exist "pan-download-mock.exe" (
        echo ✅ 使用模拟程序进行测试安装
        echo.
        echo 注意: 这是模拟安装，用于测试安装流程
        echo.
        set EXE_NAME=pan-download-mock.exe
    ) else (
        echo ❌ 错误: 找不到主程序和模拟程序
        echo.
        echo 请先运行打包脚本生成程序:
        echo   1. 运行 auto_build.bat
        echo   2. 或运行 build.bat
        echo.
        pause
        exit /b 1
    )
)

echo ✅ 找到主程序: %EXE_NAME%
echo.

REM 创建安装目录
echo 创建安装目录...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
echo ✅ 目录创建完成: %INSTALL_DIR%
echo.

REM 复制文件
echo 复制程序文件...
copy "%EXE_NAME%" "%INSTALL_DIR%\" >nul
if %errorlevel% equ 0 (
    echo ✅ 主程序复制成功
) else (
    echo ❌ 主程序复制失败
    pause
    exit /b 1
)

if exist .env.example (
    copy .env.example "%INSTALL_DIR%\" >nul
    echo ✅ 配置模板复制成功
)

if exist README.md (
    copy README.md "%INSTALL_DIR%\" >nul
    echo ✅ 说明文档复制成功
)

echo.
echo ====================================
echo ✅ 测试安装完成！
echo ====================================
echo.
echo 安装位置: %INSTALL_DIR%
echo 可执行文件: %INSTALL_DIR%\%EXE_NAME%
echo.

REM 测试程序是否可运行
echo 测试程序...
if exist "%INSTALL_DIR%\%EXE_NAME%" (
    echo 运行帮助命令测试...
    "%INSTALL_DIR%\%EXE_NAME%" --help >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ 程序测试通过 - 可以正常运行
    ) else (
        echo ⚠️  程序可能有问题，建议手动测试
    )
)

echo.
echo ====================================
echo 🚀 测试命令
echo ====================================
echo.
echo 你现在可以运行:
echo.
echo   cd /d %INSTALL_DIR%
echo   %EXE_NAME% --help
echo   %EXE_NAME% --test-config
echo   %EXE_NAME% apps/bypy/test_pdf --upload-sftp
echo.

REM 添加到PATH (测试环境)
echo 是否添加到系统PATH? (测试环境可选)
set /p ADD_PATH="添加到PATH? (y/n): "
if /i "%ADD_PATH%"=="y" (
    setx PATH "%PATH%;%INSTALL_DIR%" /M >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ 已添加到系统PATH
    ) else (
        echo ⚠️  添加失败，可能需要管理员权限
    )
)

echo.
echo ====================================
echo 📋 测试检查清单
echo ====================================
echo.
echo 请手动验证:
echo   [ ] 目录存在: %INSTALL_DIR%
echo   [ ] 程序文件: %INSTALL_DIR%\%EXE_NAME%
echo   [ ] 程序可运行: %EXE_NAME% --help
echo   [ ] 配置文件: %INSTALL_DIR%\.env.example
echo.

REM 打开安装目录
echo ====================================
echo 打开安装目录...
echo.

explorer "%INSTALL_DIR%"

echo.
echo 测试安装完成！请检查程序是否正常运行。
pause