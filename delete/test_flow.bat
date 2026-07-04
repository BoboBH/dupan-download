@echo off
REM 快速测试脚本 - 验证发布流程
echo ====================================
echo 测试发布流程
echo ====================================
echo.

echo 1. 检查当前文件...
dir *.bat
echo.

echo 2. 运行发布脚本会生成：
echo    - release_*/dupan-download-windows/ 目录
echo    - pan-download.exe (主程序)
echo    - install.bat (安装脚本)
echo    - 其他文档和配置文件
echo.

echo 3. 完整流程：
echo    步骤1: create_release.bat
echo    步骤2: 复制 release_*/dupan-download-windows/ 到目标机
echo    步骤3: 在目标机运行 install.bat
echo.

echo 是否现在运行 create_release.bat？
set /p choice="输入 y 继续，其他键退出: "

if /i "%choice%"=="y" (
    echo.
    echo 开始运行发布脚本...
    call create_release.bat
) else (
    echo.
    echo 请手动运行: create_release.bat
)

pause