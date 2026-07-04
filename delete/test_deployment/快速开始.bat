@echo off
chcp 65001 > nul
REM ============================================
REM 百度网盘下载工具 - 快速开始向导
REM ============================================

echo.
echo ====================================
echo 百度网盘下载工具 - 快速开始
echo ====================================
echo.
echo 欢迎使用百度网盘下载工具！
echo.
echo 请按以下步骤完成配置：
echo.

REM 检查 .env 文件
if not exist ".env" (
    echo [1/3] 创建配置文件...
    copy ".env.example" ".env" >nul
    echo   ✓ 已创建 .env 配置文件
    echo.
    echo [2/3] 编辑配置文件...
    echo   请打开 .env 文件并配置以下信息：
    echo   - SFTP 服务器信息（如需上传功能）
    echo   - 其他可选配置
    echo.
    notepad ".env"
) else (
    echo [✓] 配置文件已存在
)

echo.
echo [3/3] 配置百度网盘认证...
echo   启动认证向导...
echo.

pan-download.exe --setup-bypy

echo.
echo ====================================
echo 配置完成！
echo ====================================
echo.
echo 测试命令:
echo   pan-download.exe --test-config
echo   pan-download.exe --help
echo.
echo 下载示例:
echo   pan-download.exe apps/bypy/test_pdf --keep-temp
echo.

pause
