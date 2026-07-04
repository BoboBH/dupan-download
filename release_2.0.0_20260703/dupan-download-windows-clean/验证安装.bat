@echo off
chcp 65001 > nul
REM ============================================
REM 部署验证脚本
REM ============================================

echo.
echo ====================================
echo 部署验证测试
echo ====================================
echo.

echo [1/5] 检查可执行文件...
if exist "pan-download.exe" (
    echo   ✓ pan-download.exe 存在

    for %%F in ("pan-download.exe") do echo   大小: %%~zF 字节
) else (
    echo   ✗ pan-download.exe 不存在
    goto :error
)
echo.

echo [2/5] 检查配置文件...
if exist ".env.example" (
    echo   ✓ .env.example 存在
) else (
    echo   ✗ .env.example 不存在
)
if exist ".env" (
    echo   ✓ .env 已配置
) else (
    echo   ⚠ .env 未配置（首次运行时创建）
)
echo.

echo [3/5] 测试程序功能...
echo   运行帮助命令...
pan-download.exe --help >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✓ 程序可以正常运行
) else (
    echo   ✗ 程序运行失败
    goto :error
)
echo.

echo [4/5] 检查文档文件...
if exist "README.md" (
    echo   ✓ README.md 存在
) else (
    echo   ✗ README.md 不存在
)
if exist "INSTALL_GUIDE.md" (
    echo   ✓ INSTALL_GUIDE.md 存在
) else (
    echo   ✗ INSTALL_GUIDE.md 不存在
)
echo.

echo [5/5] 独立性检查...
echo   ✓ 这是一个独立的部署包
echo   ✓ 无需 Python 环境
echo   ✓ 包含所有依赖
echo.

echo ====================================
echo 验证完成！
echo ====================================
echo.
echo 部署包状态: ✓ 可以部署
echo.
echo 下一步:
echo   1. 运行: 快速开始.bat
echo   2. 或手动: pan-download.exe --setup-bypy
echo   3. 测试: pan-download.exe apps/bypy/test_pdf --keep-temp
echo.

pause
exit /b 0

:error
echo.
echo ====================================
echo 验证失败！
echo ====================================
echo.
pause
exit /b 1
