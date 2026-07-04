@echo off
REM 一键安装脚本 - 在目标Windows电脑上运行
echo ====================================
echo 百度网盘下载工具 - 一键安装脚本
echo ====================================

REM 检查管理员权限
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo 提示: 建议以管理员身份运行此脚本以获得最佳体验
    echo.
)

REM 设置安装目录
set INSTALL_DIR=%USERPROFILE%\dupan-download
set EXE_NAME=pan-download.exe

echo 安装目录: %INSTALL_DIR%
echo.

REM 创建安装目录
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
)

REM 复制文件
echo 正在复制文件...
copy "%EXE_NAME%" "%INSTALL_DIR%\" >nul
if exist .env.example copy .env.example "%INSTALL_DIR%\" >nul
if exist README.md copy README.md "%INSTALL_DIR%\" >nul
if exist DEPLOYMENT_GUIDE.md copy DEPLOYMENT_GUIDE.md "%INSTALL_DIR%\" >nul

REM 检查是否有认证文件
if exist "auth_files" (
    echo 发现认证文件，正在安装...
    xcopy "auth_files\*" "%USERPROFILE%\.bypy\" /E /I /Y >nul 2>&1
    if %errorlevel% equ 0 (
        echo ✅ 认证文件安装成功
    ) else (
        echo ⚠️  认证文件安装失败，请手动复制
    )
) else (
    echo 未找到认证文件，需要手动配置
)

REM 添加到PATH
echo.
echo 正在添加到系统PATH...
setx PATH "%PATH%;%INSTALL_DIR%" /M >nul 2>&1
if %errorlevel% neq 0 (
    echo 警告: 无法修改系统PATH，需要管理员权限
    echo 请手动添加 %INSTALL_DIR% 到系统PATH
)

REM 创建配置文件向导
echo.
echo ====================================
echo 配置向导
echo ====================================
echo.
echo 请按以下步骤完成配置:
echo.
echo 1. 百度网盘认证配置
echo    - 运行: pan-download --setup-bypy
echo    - 按提示完成OAuth认证
echo.
echo 2. SFTP服务器配置
echo    - 编辑 .env 文件
echo    - 填写SFTP服务器信息
echo.

if exist "%USERPROFILE%\.bypy\token.json" (
    echo 3. 测试配置
    echo    - 运行: pan-download --test-config
    echo.
    echo ✅ 认证文件已安装，可以直接使用
) else (
    echo 3. 百度网盘认证配置
    echo    - 认证文件未安装
    echo    - 请参考 DEPLOYMENT_GUIDE.md 中的"认证配置"章节
    echo    - 或查看 NO_PYTHON_DEPLOYMENT.md 了解详细步骤
    echo.
    echo 4. 测试配置
    echo    - 运行: pan-download --test-config
    echo.
    echo ⚠️  需要配置百度网盘认证文件才能使用下载功能
)

REM 启动配置向导
set /p START_NOW="是否现在开始配置? (y/n): "
if /i "%START_NOW%"=="y" (
    if not exist "%INSTALL_DIR%\.env" (
        copy "%INSTALL_DIR%\.env.example" "%INSTALL_DIR%\.env"
        echo 已创建 .env 配置文件
    )

    echo.
    echo 启动bypy认证向导...
    cd "%INSTALL_DIR%"
    pan-download --setup-bypy
)

echo.
echo ====================================
echo 安装完成！
echo ====================================
echo.
echo 安装位置: %INSTALL_DIR%
echo 可执行文件: %INSTALL_DIR%\%EXE_NAME%
echo.
echo 使用方法:
echo   pan-download <远程文件夹路径> [选项]
echo.
echo 示例:
echo   pan-download 260701 --upload-sftp
echo.
pause