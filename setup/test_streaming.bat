@echo off
chcp 65001 > nul
REM ============================================
REM 流式处理测试脚本
REM ============================================

echo.
echo ====================================
REM 流式处理功能测试
REM ====================================
echo.
echo 此脚本将测试流式处理功能
echo.
echo 测试内容:
echo   1. 验证程序是否包含流式处理模块
echo   2. 测试流式处理功能
echo   3. 对比传统模式和流式模式
echo.

REM 检查程序是否存在
if not exist "dist\pan-download.exe" (
    echo 错误: 未找到可执行文件
    echo 请先运行: cd setup ^&^& setup.bat build
    pause
    exit /b 1
)

echo [1/3] 验证流式处理模块...
echo.
dist\pan-download.exe --help | findstr /C:"--streaming" >nul
if %errorlevel% equ 0 (
    echo   [✓] 流式处理功能可用
) else (
    echo   [✗] 流式处理功能不可用
    echo   请确保使用最新版本
    pause
    exit /b 1
)
echo.

echo [2/3] 测试流式处理功能...
echo.
echo 测试命令:
echo   pan-download.exe apps/bypi/test_pdf --upload-sftp --streaming --keep-temp --verbose
echo.
pause

echo.
echo 正在测试...
echo.
dist\pan-download.exe apps/bypi/test_pdf --upload-sftp --streaming --keep-temp --verbose

if %errorlevel% equ 0 (
    echo.
    echo ====================================
    echo 测试成功！
    echo ====================================
    echo.
    echo 流式处理功能正常工作
    echo.
) else (
    echo.
    echo ====================================
    echo 测试失败！
    echo ====================================
    echo.
    echo 请检查:
    echo   1. SFTP配置是否正确
    echo   2. 网络连接是否正常
    echo   3. bypy认证是否完成
    echo.
)

echo [3/3] 性能对比说明
echo.
echo 传统模式 vs 流式模式:
echo.
echo 传统模式:
echo   - 下载所有文件 → 上传所有文件
echo   - 耗时较长
echo   - 占用大量磁盘空间
echo   - 无去重功能
echo.
echo 流式模式:
echo   - 下载一个文件 → 立即上传一个文件
echo   - 耗时减半
echo   - 占用最小磁盘空间
echo   - 自动跳过已存在文件
echo   - 自动创建目录结构
echo.

echo ====================================
REM 测试完成
echo ====================================
echo.

echo 推荐使用方式:
echo   pan-download.exe apps/bypi/your_folder --upload-sftp --streaming
echo.

pause
