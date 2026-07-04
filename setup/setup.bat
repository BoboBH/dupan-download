@echo off
chcp 65001 > nul
REM ============================================
REM 百度网盘下载工具 - 统一打包脚本
REM ============================================
REM
REM 这是主打包脚本，提供完整的打包流程
REM
REM 使用方法:
REM   setup.bat              - 显示菜单
REM   setup.bat build       - 构建可执行文件
REM   setup.bat package     - 创建部署包
REM   setup.bat zip         - 创建 ZIP 分发包
REM   setup.bat clean       - 清理构建文件
REM   setup.bat all         - 完整打包流程
REM
REM ============================================

setlocal

REM 获取脚本所在目录的父目录（项目根目录）
set "PROJECT_DIR=%~dp0.."
cd /d "%PROJECT_DIR%"

echo.
echo ====================================
echo 百度网盘下载工具 - 打包工具
echo ====================================
echo.
echo 项目目录: %PROJECT_DIR%
echo.

REM 检查参数
if "%1"=="" goto :menu
if /i "%1"=="build" goto :build
if /i "%1"=="package" goto :package
if /i "%1"=="zip" goto :zip
if /i "%1"=="clean" goto :clean
if /i "%1"=="all" goto :all
if /i "%1"=="help" goto :help

echo 未知参数: %1
echo.
goto :help

:menu
echo 请选择操作:
echo.
echo   1. 构建可执行文件 (build)
echo   2. 创建部署包 (package)
echo   3. 创建 ZIP 分发包 (zip)
echo   4. 清理构建文件 (clean)
echo   5. 完整打包流程 (all)
echo   6. 帮助 (help)
echo.
set /p choice="请输入选项 (1-6): "

if "%choice%"=="1" goto :build
if "%choice%"=="2" goto :package
if "%choice%"=="3" goto :zip
if "%choice%"=="4" goto :clean
if "%choice%"=="5" goto :all
if "%choice%"=="6" goto :help

echo 无效的选项
pause
exit /b 1

:build
echo.
echo ====================================
echo [1/4] 构建可执行文件
echo ====================================
echo.

REM 检查虚拟环境
if not exist ".venv\Scripts\python.exe" (
    echo 错误: 未找到虚拟环境
    echo 请先创建虚拟环境: python -m venv .venv
    pause
    exit /b 1
)

REM 检查 PyInstaller
.venv\Scripts\python.exe -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo 正在安装 PyInstaller...
    .venv\Scripts\pip.exe install pyinstaller pywin32
)

REM 清理旧构建
echo 清理旧构建文件...
if exist "build" rmdir /s /q "build" 2>nul
if exist "dist" rmdir /s /q "dist" 2>nul

REM 执行构建
echo 开始构建...
.venv\Scripts\python.exe -m PyInstaller setup\build.spec --clean

if %errorlevel% equ 0 (
    echo.
    echo ====================================
    echo 构建成功！
    echo ====================================
    echo.
    echo 可执行文件: dist\pan-download.exe
    dir "dist\pan-download.exe"
    echo.
) else (
    echo.
    echo ====================================
    echo 构建失败！
    echo ====================================
    echo.
    pause
    exit /b 1
)

if "%2"=="nopause" goto :eof
pause
exit /b 0

:package
echo.
echo ====================================
echo [2/4] 创建部署包
echo ====================================
echo.

REM 检查可执行文件
if not exist "dist\pan-download.exe" (
    echo 错误: 未找到可执行文件
    echo 请先运行: setup.bat build
    pause
    exit /b 1
)

REM 创建部署包目录
set "PACKAGE_DIR=release_2.0.0_20260703\dupan-download-windows"
if exist "%PACKAGE_DIR%" rmdir /s /q "%PACKAGE_DIR%"
mkdir "%PACKAGE_DIR%"

REM 复制文件
echo 复制文件到部署包...
copy "dist\pan-download.exe" "%PACKAGE_DIR%\" >nul
echo   [✓] pan-download.exe

copy ".env.example" "%PACKAGE_DIR%\" >nul
echo   [✓] .env.example

copy "README.md" "%PACKAGE_DIR%\" >nul
echo   [✓] README.md

if exist "docs\guides\INSTALL_GUIDE.md" (
    copy "docs\guides\INSTALL_GUIDE.md" "%PACKAGE_DIR%\" >nul
    echo   [✓] INSTALL_GUIDE.md
)

REM 复制辅助脚本
echo 创建辅助脚本...

REM 快速开始脚本
echo @echo off > "%PACKAGE_DIR%\快速开始.bat"
echo chcp 65001 ^> nul >> "%PACKAGE_DIR%\快速开始.bat"
echo echo 正在启动配置向导... >> "%PACKAGE_DIR%\快速开始.bat"
echo echo. >> "%PACKAGE_DIR%\快速开始.bat"
echo pan-download.exe --setup-bypi >> "%PACKAGE_DIR%\快速开始.bat"
echo pause >> "%PACKAGE_DIR%\快速开始.bat"
echo   [✓] 快速开始.bat

REM 验证安装脚本
echo @echo off > "%PACKAGE_DIR%\验证安装.bat"
echo chcp 65001 ^> nul >> "%PACKAGE_DIR%\验证安装.bat"
echo echo 正在验证安装... >> "%PACKAGE_DIR%\验证安装.bat"
echo echo. >> "%PACKAGE_DIR%\验证安装.bat"
echo pan-download.exe --help >> "%PACKAGE_DIR%\验证安装.bat"
echo if %%errorlevel%% equ 0 ( >> "%PACKAGE_DIR%\验证安装.bat"
echo     echo   [✓] 程序可以正常运行 >> "%PACKAGE_DIR%\验证安装.bat"
echo ^) else ( >> "%PACKAGE_DIR%\验证安装.bat"
echo     echo   [✗] 程序运行失败 >> "%PACKAGE_DIR%\验证安装.bat"
echo ^) >> "%PACKAGE_DIR%\验证安装.bat"
echo pause >> "%PACKAGE_DIR%\验证安装.bat"
echo   [✓] 验证安装.bat

echo.
echo ====================================
echo 部署包创建成功！
echo ====================================
echo.
echo 部署包位置: %PACKAGE_DIR%\
echo.

if "%2"=="nopause" goto :eof
pause
exit /b 0

:zip
echo.
echo ====================================
echo [3/4] 创建 ZIP 分发包
echo ====================================
echo.

REM 检查部署包
set "PACKAGE_DIR=release_2.0.0_20260703\dupan-download-windows"
if not exist "%PACKAGE_DIR%" (
    echo 错误: 未找到部署包
    echo 请先运行: setup.bat package
    pause
    exit /b 1
)

REM 创建 ZIP
echo 正在创建 ZIP 文件...
powershell -Command "Compress-Archive -Path '%PACKAGE_DIR%\*' -DestinationPath 'dupan-download-windows-2.0.0.zip' -Force"

if %errorlevel% equ 0 (
    echo.
    echo ====================================
    echo ZIP 创建成功！
    echo ====================================
    echo.
    echo 文件: dupan-download-windows-2.0.0.zip
    dir "dupan-download-windows-2.0.0.zip"
    echo.
) else (
    echo.
    echo ====================================
    echo ZIP 创建失败！
    echo ====================================
    echo.
    pause
    exit /b 1
)

if "%2"=="nopause" goto :eof
pause
exit /b 0

:clean
echo.
echo ====================================
echo [4/4] 清理构建文件
echo ====================================
echo.

echo 清理以下目录和文件:
echo   - build\
echo   - dist\
echo   - release_*\
echo   - *.zip
echo.
set /p confirm="确认清理? (y/n): "

if /i not "%confirm%"=="y" (
    echo 已取消
    pause
    exit /b 0
)

echo.
echo 正在清理...

if exist "build" (
    rmdir /s /q "build" 2>nul
    echo   [✓] build\
)

if exist "dist" (
    rmdir /s /q "dist" 2>nul
    echo   [✓] dist\
)

for /d %%d in (release_*) do (
    rmdir /s /q "%%d" 2>nul
    echo   [✓] %%d
)

for %%f in (*.zip) do (
    del "%%f" 2>nul
    echo   [✓] %%f
)

echo.
echo ====================================
echo 清理完成！
echo ====================================
echo.

if "%2"=="nopause" goto :eof
pause
exit /b 0

:all
echo.
echo ====================================
echo 完整打包流程
echo ====================================
echo.
echo 这将执行以下步骤:
echo   1. 构建可执行文件
echo   2. 创建部署包
echo   3. 创建 ZIP 分发包
echo.
echo 预计耗时: 5-10 分钟
echo.
set /p confirm="开始完整打包? (y/n): "

if /i not "%confirm%"=="y" (
    echo 已取消
    pause
    exit /b 0
)

echo.
echo 开始完整打包流程...
echo.

REM 步骤 1: 构建
call :build nopause
if %errorlevel% neq 0 (
    echo 构建失败，终止流程
    pause
    exit /b 1
)

REM 步骤 2: 创建部署包
call :package nopause
if %errorlevel% neq 0 (
    echo 创建部署包失败，终止流程
    pause
    exit /b 1
)

REM 步骤 3: 创建 ZIP
call :zip nopause
if %errorlevel% neq 0 (
    echo 创建 ZIP 失败，终止流程
    pause
    exit /b 1
)

echo.
echo ====================================
echo 🎉 完整打包流程完成！
echo ====================================
echo.
echo 生成文件:
echo   - dist\pan-download.exe
echo   - release_2.0.0_20260703\dupan-download-windows\
echo   - dupan-download-windows-2.0.0.zip
echo.

pause
exit /b 0

:help
echo.
echo ====================================
echo 打包工具帮助
echo ====================================
echo.
echo 用法:
echo   setup.bat              - 显示交互菜单
echo   setup.bat build       - 构建可执行文件
echo   setup.bat package     - 创建部署包
echo   setup.bat zip         - 创建 ZIP 分发包
echo   setup.bat clean       - 清理构建文件
echo   setup.bat all         - 完整打包流程
echo   setup.bat help        - 显示帮助
echo.
echo 示例:
echo   setup.bat build       - 仅构建可执行文件
echo   setup.bat all         - 完整打包（构建+部署包+ZIP）
echo.
echo 注意:
echo   - 需要虚拟环境 (.venv)
echo   - 需要安装 PyInstaller
echo   - 构建过程需要 5-10 分钟
echo.

pause
exit /b 0
