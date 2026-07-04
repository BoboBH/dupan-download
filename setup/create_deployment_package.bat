@echo off
REM ============================================
REM 创建部署包 - 不包含敏感信息
REM ============================================

echo.
echo ====================================
echo 创建部署包
echo ====================================
echo.

REM 设置变量
set SOURCE_DIR=D:\baidu-download
set PACKAGE_DIR=D:\git\dupan-download\release_2.0.0_20260703\dupan-download-windows
set ZIP_NAME=dupan-download-windows-2.0.0.zip

echo 源目录: %SOURCE_DIR%
echo 目标目录: %PACKAGE_DIR%
echo.

REM 清理并创建目标目录
if exist "%PACKAGE_DIR%" rmdir /s /q "%PACKAGE_DIR%"
mkdir "%PACKAGE_DIR%"

REM 复制必要文件（不包含 .env 敏感配置）
echo 复制文件...
copy "%SOURCE_DIR%\pan-download.exe" "%PACKAGE_DIR%\" >nul
echo   [✓] pan-download.exe

copy "%SOURCE_DIR%\.env.example" "%PACKAGE_DIR%\" >nul
echo   [✓] .env.example

copy "%SOURCE_DIR%\README.md" "%PACKAGE_DIR%\" >nul
echo   [✓] README.md

REM 复制安装指南
if exist "D:\git\dupan-download\release_2.0.0_20260703\dupan-download-windows\INSTALL_GUIDE.md" (
    copy "D:\git\dupan-download\release_2.0.0_20260703\dupan-download-windows\INSTALL_GUIDE.md" "%PACKAGE_DIR%\" >nul
    echo   [✓] INSTALL_GUIDE.md
)

REM 创建快速启动脚本
echo @echo off > "%PACKAGE_DIR%\启动配置向导.bat"
echo echo 正在启动百度网盘下载工具配置向导... >> "%PACKAGE_DIR%\启动配置向导.bat"
echo echo. >> "%PACKAGE_DIR%\启动配置向导.bat"
echo pan-download.exe --setup-bypy >> "%PACKAGE_DIR%\启动配置向导.bat"
echo pause >> "%PACKAGE_DIR%\启动配置向导.bat"
echo   [✓] 启动配置向导.bat

REM 创建测试脚本
echo @echo off > "%PACKAGE_DIR%\测试配置.bat"
echo echo 正在测试配置... >> "%PACKAGE_DIR%\测试配置.bat"
echo echo. >> "%PACKAGE_DIR%\测试配置.bat"
echo pan-download.exe --test-config >> "%PACKAGE_DIR%\测试配置.bat"
echo pause >> "%PACKAGE_DIR%\测试配置.bat"
echo   [✓] 测试配置.bat

echo.
echo ====================================
echo 文件复制完成！
echo ====================================
echo.
echo 部署包位置: %PACKAGE_DIR%
echo.
echo 包含的文件:
dir "%PACKAGE_DIR%" /B
echo.

REM 显示文件大小
echo 文件大小:
for %%f in ("%PACKAGE_DIR%\*") do (
    echo   %%~nxf: %%~zf 字节
)
echo.

REM 提示用户配置
echo ====================================
echo 重要提示
echo ====================================
echo.
echo 1. 部署包不包含敏感配置信息
echo 2. 目标机器需要配置:
echo    - 复制 .env.example 为 .env
echo    - 填写 SFTP 配置信息
echo    - 运行 pan-download.exe --setup-bypy
echo.
echo 3. 可用脚本:
echo    - 启动配置向导.bat
echo    - 测试配置.bat
echo.

pause
