@echo off
chcp 65001 > nul
REM ============================================
REM 创建发布ZIP并放到dist目录
REM ============================================

setlocal

echo.
echo ====================================
REM 创建发布ZIP（放到dist目录）
REM ====================================
echo.

REM 返回项目根目录
cd /d "%~dp0.."

echo 项目目录: %CD%
echo.

REM 检查可执行文件
if not exist "dist\pan-download.exe" (
    echo 错误: 未找到可执行文件
    echo 请先运行: setup.bat build
    pause
    exit /b 1
)

REM 创建dist目录（如果不存在）
if not exist "dist" mkdir dist
echo   [✓] dist目录已准备

REM 获取版本号
for /f "tokens=*" %%i in ('findstr /R "version=" setup.py') do (
    set VERSION_LINE=%%i
    set VERSION_LINE=!VERSION_LINE:*version= =!
    set VERSION=!VERSION_LINE:"=!
)

echo.
echo 版本号: !VERSION!
echo.

REM 创建临时部署包目录
set "TEMP_PACKAGE=dist\dupan-download-windows-v!VERSION!"
if exist "%TEMP_PACKAGE%" rmdir /s /q "%TEMP_PACKAGE%"
mkdir "%TEMP_PACKAGE%"

echo 正在创建部署包...

REM 复制文件
copy "dist\pan-download.exe" "%TEMP_PACKAGE%\" >nul
copy ".env.example" "%TEMP_PACKAGE%\" >nul
copy "README.md" "%TEMP_PACKAGE%\" >nul

if exist "docs\guides\INSTALL_GUIDE.md" (
    copy "docs\guides\INSTALL_GUIDE.md" "%TEMP_PACKAGE%\" >nul
)

REM 创建快速启动脚本
echo @echo off > "%TEMP_PACKAGE%\快速开始.bat"
echo chcp 65001 ^> nul >> "%TEMP_PACKAGE%\快速开始.bat"
echo echo 正在启动配置向导... >> "%TEMP_PACKAGE%\快速开始.bat"
echo echo. >> "%TEMP_PACKAGE%\快速开始.bat"
echo pan-download.exe --setup-bypi >> "%TEMP_PACKAGE%\快速开始.bat"
echo pause >> "%TEMP_PACKAGE%\快速开始.bat"

echo   [✓] 部署包已创建

REM 创建ZIP文件到dist目录
echo 正在创建ZIP文件...
powershell -Command "Compress-Archive -Path '%TEMP_PACKAGE%\*' -DestinationPath 'dist\dupan-download-windows-v!VERSION!.zip' -Force"

if %errorlevel% equ 0 (
    echo.
    echo ====================================
    echo ✅ ZIP创建成功！
    echo ====================================
    echo.

    echo 文件位置:
    dir "dist\dupan-download-windows-v!VERSION!.zip"

    echo.
    echo 清理临时目录...
    rmdir /s /q "%TEMP_PACKAGE%"

    echo.
    echo ====================================
    echo 🎉 打包完成！
    echo ====================================
    echo.
    echo 版本: !VERSION!
    echo.
    echo 发布文件:
    echo   dist\dupan-download-windows-v!VERSION!.zip
    echo.
    echo 使用说明:
    echo   1. 将ZIP文件复制到目标机器
    echo   2. 解压到任意位置
    echo   3. 运行: pan-download.exe --setup-bypi
    echo   4. 测试: pan-download.exe test_pdf --upload-sftp
    echo.

) else (
    echo.
    echo ====================================
    echo ❌ ZIP创建失败！
    echo ====================================
    echo.
    pause
    exit /b 1
)

pause
