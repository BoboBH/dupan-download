@echo off
REM 一键发布脚本 - 创建完整的部署包
echo ====================================
echo 百度网盘下载工具 - 一键发布脚本
echo ====================================
echo.

REM 设置版本号
set VERSION=1.0.0
set RELEASE_DIR=release_%VERSION%_%date:~0,4%%date:~5,2%%date:~8,2%
set PACKAGE_DIR=%RELEASE_DIR%\dupan-download-windows

echo 创建发布包: %PACKAGE_DIR%
echo.

REM 清理旧的发布包
if exist %RELEASE_DIR% rmdir /s /q %RELEASE_DIR%

REM 创建发布目录结构
mkdir %PACKAGE_DIR%
mkdir %PACKAGE_DIR%\docs

echo ====================================
echo 步骤 1: 打包程序
echo ====================================
echo.

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
pip install pyinstaller pywin32 bypy

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

echo ✅ 打包完成
echo.

echo ====================================
echo 步骤 2: 复制文件到发布目录
echo ====================================
echo.

REM 复制主要文件
copy dist\pan-download.exe %PACKAGE_DIR%\ >nul
copy .env.example %PACKAGE_DIR%\ >nul
copy README.md %PACKAGE_DIR%\ >nul
copy DEPLOYMENT_GUIDE.md %PACKAGE_DIR%\ >nul
copy USAGE_GUIDE.md %PACKAGE_DIR%\docs\ >nul
copy CONFIG_CLEAN.md %PACKAGE_DIR%\docs\ >nul
copy PROJECT_STATUS.md %PACKAGE_DIR%\docs\ >nul
copy build.bat %PACKAGE_DIR%\docs\ >nul
copy build.spec %PACKAGE_DIR%\docs\ >nul

echo ✅ 文件复制完成
echo.

echo ====================================
echo 步骤 3: 创建安装脚本
echo ====================================
echo.

REM 创建安装脚本
(
echo @echo off
echo REM 一键安装脚本 - 在目标Windows电脑上运行
echo echo ====================================
echo echo 百度网盘下载工具 - 一键安装向导
echo echo ====================================
echo echo.
echo.
echo REM 检查管理员权限
echo net session ^>nul 2^>^&1
echo if %%errorlevel%% neq 0 ^(
echo     echo 提示: 建议以管理员身份运行此脚本
echo     echo.
echo ^)
echo.
echo REM 设置安装目录
echo set INSTALL_DIR=%%USERPROFILE%%\dupan-download
echo set EXE_NAME=pan-download.exe
echo.
echo echo 安装目录: %%INSTALL_DIR%%
echo echo.
echo.
echo REM 创建安装目录
echo if not exist "%%INSTALL_DIR%%" mkdir "%%INSTALL_DIR%%"
echo.
echo REM 复制文件
echo echo 正在复制文件...
echo copy "%%EXE_NAME%%" "%%INSTALL_DIR%%\" ^>nul
echo if exist .env.example copy .env.example "%%INSTALL_DIR%%\" ^>nul
echo if exist README.md copy README.md "%%INSTALL_DIR%%\" ^>nul
echo if exist DEPLOYMENT_GUIDE.md copy DEPLOYMENT_GUIDE.md "%%INSTALL_DIR%%\" ^>nul
echo.
echo REM 检查认证文件
echo if exist "auth_files" ^(
echo     echo 发现认证文件，正在安装...
echo     xcopy "auth_files\*" "%%USERPROFILE%%\.bypy\" /E /I /Y ^>nul 2^>^&1
echo     if %%errorlevel%% equ 0 ^(
echo         echo 认证文件安装成功
echo     ^) else ^(
echo         echo 认证文件安装失败
echo     ^)
echo ^) else ^(
echo     echo 未找到认证文件，需要手动配置
echo     echo 请按照 %%INSTALL_DIR%%\DEPLOYMENT_GUIDE.md 中的说明配置认证
echo ^)
echo.
echo REM 添加到PATH
echo echo.
echo echo 正在添加到系统PATH...
echo setx PATH "%%PATH%%;%%INSTALL_DIR%%" /M ^>nul 2^>^&1
echo if %%errorlevel%% neq 0 ^(
echo     echo 警告: 无法修改系统PATH，需要管理员权限
echo     echo 请手动添加 %%INSTALL_DIR%% 到系统PATH
echo ^)
echo.
echo echo ====================================
echo echo 安装完成！
echo echo ====================================
echo echo.
echo echo 安装位置: %%INSTALL_DIR%%
echo echo 可执行文件: %%INSTALL_DIR%%\%%EXE_NAME%%
echo echo.
echo if exist "%%USERPROFILE%%\.bypy\token.json" ^(
echo     echo ✅ 认证文件已安装，可以直接使用
echo ^) else ^(
echo     echo ⚠️  认证文件未安装，需要配置
echo ^)
echo echo.
echo echo 下一步操作:
echo echo   1. 配置百度网盘认证: pan-download --setup-bypy
echo echo   2. 编辑SFTP配置: 编辑 %%INSTALL_DIR%%\.env
echo echo   3. 测试配置: pan-download --test-config
echo echo   4. 开始使用: pan-download ^<远程路径^> [选项]
echo echo.
echo echo 详细文档:
echo echo   - %%INSTALL_DIR%%\DEPLOYMENT_GUIDE.md
echo echo   - %%INSTALL_DIR%%\NO_PYTHON_DEPLOYMENT.md
echo echo.
echo pause
) > %PACKAGE_DIR%\install.bat

echo ✅ 安装脚本创建完成
echo.

echo ====================================
echo 步骤 4: 创建快速启动指南
echo ====================================
echo.

(
echo # 快速启动指南
echo.
echo ## 安装步骤
echo.
echo 1. 以管理员身份运行 install.bat
echo.
echo ## 配置步骤
echo.
echo ### 1. 百度网盘认证
echo ```bash
echo pan-download --setup-bypy
echo ```
echo.
echo ### 2. SFTP服务器配置
echo.
echo 编辑 .env 文件，填写SFTP服务器信息:
echo.
echo ```env
echo SFTP_HOST=your.server.com
echo SFTP_PORT=22
echo SFTP_USERNAME=your_username
echo SFTP_PASSWORD=your_password
echo SFTP_REMOTE_PATH=/remote/path
echo ```
echo.
echo ### 3. 测试配置
echo ```bash
echo pan-download --test-config
echo ```
echo.
echo ## 使用方法
echo.
echo ```bash
echo # 下载文件
echo pan-download 260701
echo.
echo # 下载并上传到SFTP
echo pan-download 260701 --upload-sftp
echo.
echo # 详细日志
echo pan-download 260701 --verbose
echo ```
echo.
echo ## 详细文档
echo.
echo - 完整部署指南: DEPLOYMENT_GUIDE.md
echo - 使用说明: docs/USAGE_GUIDE.md
echo - 配置说明: docs/CONFIG_CLEAN.md
echo.
echo ## 系统要求
echo.
echo - Windows 7/8/10/11
echo - 无需安装Python
echo - 建议管理员权限运行
echo.
echo ## 技术支持
echo.
echo 如遇问题，请查看 DEPLOYMENT_GUIDE.md 中的"常见问题"章节
) > %PACKAGE_DIR%\QUICK_START.txt

echo ✅ 快速启动指南创建完成
echo.

echo ====================================
echo 步骤 5: 创建版本信息
echo ====================================
echo.

(
echo 版本: %VERSION%
echo 发布日期: %date%
echo.
echo 包含文件:
echo - pan-download.exe (主程序)
echo - install.bat (安装脚本)
echo - .env.example (配置模板)
echo - README.md (项目说明)
echo - DEPLOYMENT_GUIDE.md (部署指南)
echo - QUICK_START.txt (快速启动指南)
echo - docs/ (详细文档目录)
echo.
echo 系统要求:
echo - Windows 7/8/10/11
echo - 无需安装Python
echo - 建议管理员权限
echo.
echo 快速开始:
echo 1. 运行 install.bat
echo 2. 运行 pan-download --setup-bypy
echo 3. 配置 .env 文件
echo 4. 运行 pan-download --test-config
echo 5. 开始使用
) > %PACKAGE_DIR%\VERSION.txt

echo ✅ 版本信息创建完成
echo.

echo ====================================
echo 步骤 6: 创建打包说明
echo ====================================
echo.

(
echo # 百度网盘下载工具 - Windows部署包
echo.
echo ## 包信息
echo.
echo - 版本: %VERSION%
echo - 发布日期: %date%
echo - 平台: Windows 7/8/10/11
echo.
echo ## 快速开始
echo.
echo 1. 将整个文件夹复制到目标电脑
echo 2. 以管理员身份运行 install.bat
echo 3. 按照安装向导完成配置
echo 4. 开始使用
echo.
echo ## 详细说明
echo.
echo 请查看:
echo - QUICK_START.txt - 快速启动指南
echo - DEPLOYMENT_GUIDE.md - 完整部署指南
echo - README.md - 项目说明
echo.
echo ## 文件清单
echo.
echo ### 主程序
echo - pan-download.exe - 主程序（已包含所有依赖）
echo.
echo ### 安装文件
echo - install.bat - 一键安装脚本
echo - .env.example - 配置文件模板
echo.
echo ### 文档文件
echo - README.md - 项目说明
echo - DEPLOYMENT_GUIDE.md - 部署指南
echo - QUICK_START.txt - 快速启动指南
echo - VERSION.txt - 版本信息
echo - docs/ - 详细文档目录
echo.
echo ## 系统要求
echo.
echo - Windows 7/8/10/11
echo - 无需安装Python或其他依赖
echo - 建议以管理员权限运行安装程序
echo.
echo ## 安全说明
echo.
echo - .env 文件包含敏感信息，请妥善保管
echo - 建议使用强密码和SFTP密钥认证
echo - 定期更新程序以获取安全修复
echo.
echo ## 技术支持
echo.
echo 如遇问题，请查看 DEPLOYMENT_GUIDE.md 中的"常见问题"章节
) > %PACKAGE_DIR%\README_PACKAGE.txt

echo ✅ 打包说明创建完成
echo.

echo ====================================
echo 步骤 7: 收集认证文件（可选）
echo ====================================
echo.

echo 是否包含认证文件？（推荐）
echo 如果选择是，脚本会复制当前的bypy认证文件
echo 这样目标机就可以直接使用，无需重新认证
echo.
set /p INCLUDE_AUTH="是否包含认证文件? (y/n): "

if /i "%INCLUDE_AUTH%"=="y" (
    echo 正在检查认证文件...

    set AUTH_DIR=%USERPROFILE%\.bypy
    if exist "%AUTH_DIR%" (
        echo ✅ 发现认证文件目录

        REM 创建认证文件目录
        mkdir %PACKAGE_DIR%\auth_files

        REM 复制认证文件
        echo 复制认证文件...
        xcopy "%AUTH_DIR%\*" "%PACKAGE_DIR%\auth_files\" /E /I /Y >nul 2>&1

        if %errorlevel% equ 0 (
            echo ✅ 认证文件复制成功

            REM 创建认证文件说明
            (
            echo # 认证文件说明
            echo.
            echo 这些文件是你的百度网盘认证凭据，包含：
            echo - OAuth令牌
            echo - Cookie信息
            echo - 其他认证相关数据
            echo.
            echo ## 安装步骤
            echo.
            echo 1. 将 auth_files 目录中的所有文件复制到:
            echo    %%USERPROFILE%%\.bypy\
            echo.
            echo 2. 确保文件结构完整
            echo.
            echo 3. 运行配置测试:
            echo    pan-download --test-config
            echo.
            echo ## 安全说明
            echo.
            echo - 这些文件包含你的认证信息，请妥善保管
            echo - 不要分享给他人
            echo - 定期更新认证令牌
            echo.
            echo ## 注意事项
            echo.
            echo - 如果认证文件过期，需要重新认证
            echo - 认证文件与你的百度账号绑定
            echo - 请确保在安全的网络上完成认证
            ) > %PACKAGE_DIR%\auth_files\README.txt

            echo ✅ 认证文件说明已创建
        ) else (
            echo ⚠️  认证文件复制失败
        )
    ) else (
        echo ⚠️  未找到认证文件目录: %AUTH_DIR%
        echo 请先在一台有Python环境的机器上完成bypy认证
    )
) else (
    echo 跳过认证文件收集
    echo 目标机需要手动配置认证文件
)

echo.
echo ====================================
echo 步骤 8: 打包完成
echo ====================================
echo.

echo 📦 发布包创建完成！
echo.
echo 发布位置: %PACKAGE_DIR%
echo.
echo 包含文件:
dir /b %PACKAGE_DIR%
echo.
echo 📋 打包清单:
echo     - pan-download.exe (主程序)
echo     - install.bat (安装脚本)
echo     - .env.example (配置模板)
echo     - README.md (项目说明)
echo     - DEPLOYMENT_GUIDE.md (部署指南)
echo     - QUICK_START.txt (快速启动指南)
echo     - VERSION.txt (版本信息)
echo     - README_PACKAGE.txt (打包说明)
echo     - docs/ (详细文档目录)
echo.
echo 🚀 部署步骤:
echo     1. 将整个 %PACKAGE_DIR% 文件夹复制到目标电脑
echo     2. 在目标电脑上以管理员身份运行 install.bat
echo     3. 按照安装向导完成配置
echo     4. 开始使用
echo.
echo ====================================
echo 发布包制作完成！
echo ====================================
echo.

pause