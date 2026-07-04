@echo off
chcp 65001 > nul
REM ============================================
REM 创建发布 ZIP 包
REM ============================================

setlocal

echo.
echo ====================================
echo 创建发布 ZIP 包
echo ====================================
echo.

REM 设置路径
set "SOURCE_DIR=D:\git\dupan-download\release_2.0.0_20260703\dupan-download-windows-clean"
set "ZIP_NAME=dupan-download-windows-2.0.0.zip"
set "ZIP_PATH=D:\git\dupan-download\%ZIP_NAME%"

echo 源目录: %SOURCE_DIR%
echo ZIP 文件: %ZIP_PATH%
echo.

REM 检查源目录
if not exist "%SOURCE_DIR%" (
    echo 错误: 源目录不存在
    pause
    exit /b 1
)

REM 显示将要打包的文件
echo 将要打包的文件:
echo.
dir "%SOURCE_DIR%" /B
echo.

REM 计算总大小
echo 计算文件大小...
powershell -Command "Get-ChildItem -Path '%SOURCE_DIR%' -Recurse | Measure-Object -Property Length -Sum | Select-Object -ExpandProperty Sum" > "%TEMP%\size.txt"
set /p TOTAL_SIZE=<"%TEMP%\size.txt"
set /a TOTAL_SIZE_MB=%TOTAL_SIZE% / 1048576
echo   总大小: ~%TOTAL_SIZE_MB% MB
echo.

REM 创建 ZIP 文件
echo 正在创建 ZIP 文件...
echo.

powershell -Command "Compress-Archive -Path '%SOURCE_DIR%\*' -DestinationPath '%ZIP_PATH%' -Force"

if %errorlevel% equ 0 (
    echo.
    echo ====================================
    echo ZIP 创建成功！
    echo ====================================
    echo.

    if exist "%ZIP_PATH%" (
        for %%F in ("%ZIP_PATH%") do (
            echo   文件: %%~nxF
            echo   位置: %%~dpF
            echo   大小: %%~zF 字节
        )
        echo.

        echo ZIP 文件内容:
        powershell -Command "Get-ChildItem -Path '%ZIP_PATH%' | Select-Object Name, Length, LastWriteTime | Format-Table -AutoSize"
    )

    echo.
    echo ====================================
    echo 部署说明
    echo ====================================
    echo.
    echo 1. 将 %ZIP_NAME% 复制到目标机器
    echo 2. 解压到任意位置（如：C:\Program Files\dupan-download\）
    echo 3. 运行: 快速开始.bat
    echo 4. 或运行: 验证安装.bat
    echo.
    echo 目标机器要求:
    echo   - Windows 10/11 (64位)
    echo   - 无需 Python 环境
    echo   - 网络连接
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

pause
