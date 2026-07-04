@echo off
chcp 65001 > nul
REM ============================================
REM 清理脚本 - 删除不需要的文件
REM ============================================

setlocal

echo.
echo ====================================
echo 清理脚本
echo ====================================
echo.
echo 此脚本将删除以下内容:
echo   - build\ 目录
echo   - dist\ 目录
echo   - release_*\ 目录
echo   - *.zip 文件
echo   - test_deployment\ 目录
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

if exist "test_deployment" (
    rmdir /s /q "test_deployment" 2>nul
    echo   [✓] test_deployment\
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

pause
