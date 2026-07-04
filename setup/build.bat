@echo off
REM 打包脚本 - 将项目打包为Windows可执行文件
echo ====================================
echo 开始打包 dupan-download 项目
echo ====================================

REM 检查Python环境
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: 未找到Python环境
    echo 请确保Python已安装并在PATH中
    pause
    exit /b 1
)

REM 安装打包依赖
echo 正在安装打包依赖...
pip install pyinstaller pywin32

REM 清理旧的打包文件
echo 清理旧的打包文件...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM 执行打包
echo 开始打包...
pyinstaller build.spec --clean

if %errorlevel% neq 0 (
    echo 打包失败！
    pause
    exit /b 1
)

echo ====================================
echo 打包完成！
echo 可执行文件位置: dist\pan-download.exe
echo ====================================

REM 复制必要文件到dist目录
echo 复制配置文件...
if exist .env.example copy .env.example dist\

echo.
echo 打包流程完成！
echo 请将 dist 目录中的所有文件复制到目标电脑
pause