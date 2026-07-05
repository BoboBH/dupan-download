"""下载和上传整合的CLI命令"""
import sys
import click
import logging
import tempfile
from pathlib import Path
from typing import Optional

from .config import get_config
from .uploader import SFTPUploader
from .transfer import BaiduTransfer
from .utils import create_temp_dir, cleanup_temp_dir, setup_logger

# 尝试导入bypy
try:
    from bypy import ByPy
    BYPY_AVAILABLE = True
except ImportError:
    BYPY_AVAILABLE = False
    print("警告: bypy未安装，请运行: pip install bypy")
    sys.exit(1)


@click.command()
@click.argument('share_link', required=False)
@click.argument('extract_code', required=False)
@click.option('--local-dir', type=click.Path(), help='本地下载目录（默认为临时目录）')
@click.option('--upload-sftp', is_flag=True, help='下载后自动上传到SFTP服务器')
@click.option('--keep-temp', is_flag=True, help='保留临时文件，不自动清理')
@click.option('--temp-dir', type=click.Path(), help='指定临时文件存储位置（需与--keep-temp配合使用）')
@click.option('--verbose', is_flag=True, help='详细输出模式')
@click.option('--setup-bypy', is_flag=True, help='启动bypy认证向导')
@click.option('--test-config', is_flag=True, help='测试配置是否正确')
@click.option('--streaming', is_flag=True, help='启用流式处理模式：下载一个文件后立即上传，自动创建SFTP目录')
def main(share_link: Optional[str], extract_code: Optional[str], local_dir: Optional[Path], upload_sftp: bool,
         keep_temp: bool, temp_dir: Optional[str], verbose: bool, setup_bypy: bool, test_config: bool, streaming: bool):
    """
    百度网盘下载和SFTP上传工具

    示例:
        # 传统模式：直接指定百度网盘路径
        pan-download apps/bypy/260701
        pan-download apps/bypy/260701 --upload-sftp

        # 转存模式：分享链接 + 提取码（推荐）
        pan-download https://pan.baidu.com/s/1Fi2LAxr441x57Kk4B6ws2Q 0409 --upload-sftp --streaming

        # 指定本地目录
        pan-download apps/bypy/260701 --local-dir "D:\我的文件"

        # 保留临时文件
        pan-download apps/bypy/260701 --keep-temp
        pan-download https://pan.baidu.com/s/1Fi2LAxr441x57Kk4B6ws2Q 0409 --upload-sftp --streaming --keep-temp

        # 启动认证向导
        pan-download --setup-bypy

        # 测试配置
        pan-download --test-config
    """
    # 设置日志
    logger = setup_logger('dupan_download_integrated', verbose=verbose)

    # 处理特殊命令
    if setup_bypy:
        return setup_bypy_wizard()

    if test_config:
        return test_configuration()

    try:
        # 判断模式：转存模式 vs 传统模式
        is_transfer_mode = share_link and extract_code and 'pan.baidu.com' in share_link

        # 转存模式：分享链接 + 提取码
        if is_transfer_mode:
            logger.info("=" * 60)
            logger.info("检测到转存模式：分享链接 + 提取码")
            logger.info("=" * 60)
            logger.info(f"分享链接: {share_link}")
            logger.info(f"提取码: {extract_code}")

            # 执行转存
            from .transfer import BaiduTransfer

            transfer = BaiduTransfer()

            # 从分享链接中推断目标文件夹名
            # 例如：链接中有270703文件夹，转存到apps/bypy/260703
            source_folder_name = transfer.extract_folder_name_from_link(share_link)
            if not source_folder_name:
                logger.error("无法从链接中推断目标文件夹名")
                sys.exit(1)

            target_folder = f"apps/bypy/{source_folder_name}"
            logger.info(f"推断目标文件夹: {target_folder}")

            # 执行转存
            transfer_result = transfer.transfer_to_own_drive(
                share_link, extract_code, target_folder
            )

            if not transfer_result.success:
                logger.error(f"转存失败: {transfer_result.error}")
                sys.exit(1)

            logger.info(f"✅ 转存成功: {transfer_result.source_folder} -> {transfer_result.target_folder}")
            logger.info(f"转存文件数: {transfer_result.files_count}")

            # 设置远程路径为转存后的路径
            remote_folder = target_folder

        else:
            # 传统模式：直接指定远程路径
            if not share_link:
                logger.error("请提供远程文件夹路径或分享链接")
                sys.exit(1)
            remote_folder = share_link

            # bypy使用相对路径，不需要apps/bypy前缀
            if remote_folder.startswith('apps/bypy/'):
                # 自动移除apps/bypy前缀
                remote_folder = remote_folder.replace('apps/bypy/', '')
                logger.info(f"自动调整路径为: {remote_folder}")

        # 创建本地目录
        if local_dir:
            local_path = Path(local_dir)
            local_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"使用指定的本地目录: {local_path}")
        elif temp_dir:
            # 使用指定的临时目录
            local_path = Path(temp_dir)
            local_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"使用指定的临时目录: {local_path}")
            # 如果指定了temp_dir，自动保留文件
            if not keep_temp:
                logger.info("检测到--temp-dir参数，自动启用--keep-temp")
                keep_temp = True
        else:
            # 使用默认临时目录
            local_path = create_temp_dir()
            logger.info(f"创建默认临时目录: {local_path}")

        logger.info(f"远程路径: {remote_folder}")
        logger.info(f"本地路径: {local_path}")
        logger.info(f"SFTP上传: {'是' if upload_sftp else '否'}")
        logger.info(f"流式处理: {'是' if streaming else '否'}")

        # 流式处理模式
        if streaming:
            logger.info("=" * 50)
            logger.info("使用流式处理模式")
            logger.info("=" * 50)
            logger.info("流式处理优势：")
            logger.info("  - 下载一个文件后立即上传")
            logger.info("  - 自动跳过已存在的文件")
            logger.info("  - 自动创建SFTP子目录")
            logger.info("  - 节省磁盘空间")

            from .streaming_processor import StreamingProcessor

            # 提取文件夹名称
            folder_name = extract_folder_name(remote_folder)

            # 构建SFTP目标路径
            if upload_sftp:
                config = get_config()
                sftp_base_path = f"{config.sftp_remote_path}/{folder_name}".replace('//', '/')
            else:
                sftp_base_path = None

            # 创建流式处理器
            processor = StreamingProcessor(
                progress_callback=lambda msg, cur, tot: logger.info(f"[{cur}/{tot}] {msg}") if tot > 0 else logger.info(msg),
                keep_local=keep_temp
            )

            # 执行流式处理
            result = processor.process_folder(
                remote_folder=remote_folder,
                sftp_base_path=sftp_base_path,
                local_temp_dir=local_path
            )

            # 显示结果
            logger.info("=" * 50)
            logger.info("流式处理结果")
            logger.info("=" * 50)
            logger.info(f"总文件数: {result.total_files}")
            logger.info(f"已上传: {result.uploaded_files}")
            if hasattr(result, 'uploaded_from_local') and result.uploaded_from_local > 0:
                logger.info(f"  └─ 从本地已有上传: {result.uploaded_from_local}")
            if hasattr(result, 'skipped_files') and result.skipped_files > 0:
                logger.info(f"完全跳过: {result.skipped_files} (本地+SFTP都有)")
            if hasattr(result, 'skipped_sftp_only') and result.skipped_sftp_only > 0:
                logger.info(f"跳过上传: {result.skipped_sftp_only} (SFTP已有)")
            logger.info(f"下载失败: {result.failed_downloads}")
            logger.info(f"上传失败: {result.failed_uploads}")
            logger.info(f"总大小: {result.total_size / 1024 / 1024:.2f} MB")

            if result.errors:
                logger.warning(f"有 {len(result.errors)} 个错误")
                if verbose:
                    for error in result.errors[:10]:
                        logger.warning(f"  - {error}")

            # 最终报告
            click.echo(f"\n🎉 流式处理完成！")
            click.echo(f"📊 处理统计:")
            click.echo(f"   - 总文件: {result.total_files}")
            click.echo(f"   - 已上传: {result.uploaded_files}")
            if hasattr(result, 'uploaded_from_local') and result.uploaded_from_local > 0:
                click.echo(f"     └─ 从本地已有上传: {result.uploaded_from_local}")
            if hasattr(result, 'skipped_files') and result.skipped_files > 0:
                click.echo(f"   - 完全跳过: {result.skipped_files} (本地+SFTP都有)")
            if hasattr(result, 'skipped_sftp_only') and result.skipped_sftp_only > 0:
                click.echo(f"   - 跳过上传: {result.skipped_sftp_only} (SFTP已有)")
            click.echo(f"   - 下载失败: {result.failed_downloads}")
            click.echo(f"   - 上传失败: {result.failed_uploads}")

            if result.failed_downloads + result.failed_uploads > 0:
                sys.exit(1)

            return  # 流式处理完成，退出

        # 传统模式：先下载后上传
        # 下载阶段
        logger.info("=" * 50)
        logger.info("开始下载阶段")
        logger.info("=" * 50)

        download_results = download_folder(remote_folder, local_path)

        if not download_results:
            logger.error("下载失败，无法继续")
            sys.exit(1)

        success_count = sum(1 for r in download_results if r.success)
        fail_count = len(download_results) - success_count

        logger.info(f"下载完成: {success_count} 成功, {fail_count} 失败")

        if success_count == 0:
            logger.error("没有成功下载任何文件")
            sys.exit(1)

        # SFTP上传阶段
        if upload_sftp:
            logger.info("=" * 50)
            logger.info("开始SFTP上传阶段")
            logger.info("=" * 50)

            try:
                config = get_config()
                uploader = SFTPUploader()

                logger.info(f"连接SFTP: {config.sftp_host}:{config.sftp_port}")

                if not uploader.connect():
                    logger.error("SFTP连接失败")
                    sys.exit(1)

                try:
                    # 提取文件夹名称作为远程子目录
                    folder_name = extract_folder_name(remote_folder)
                    remote_path = f"{config.sftp_remote_path}/{folder_name}".replace('//', '/')

                    logger.info(f"上传到远程路径: {remote_path}")
                    logger.info(f"创建远程文件夹: {folder_name}")

                    logger.info("开始上传文件...")
                    upload_results = uploader.upload_folder(local_path, remote_path)

                    upload_success = sum(1 for r in upload_results if r.success)
                    upload_fail = len(upload_results) - upload_success

                    logger.info(f"上传完成: {upload_success} 成功, {upload_fail} 失败")

                    if upload_fail > 0:
                        logger.warning("上传失败的文件:")
                        for result in upload_results:
                            if not result.success:
                                logger.warning(f"  - {result.local_path}: {result.error}")

                finally:
                    uploader.disconnect()

            except Exception as e:
                logger.error(f"SFTP上传异常: {e}")
                import traceback
                logger.error(traceback.format_exc())
        else:
            logger.info("跳过SFTP上传步骤")

        # 清理临时文件
        if not keep_temp:
            cleanup_temp_dir(local_path)
            logger.info("✅ 已清理临时文件")
        else:
            logger.info(f"📁 临时文件已保留: {local_path}")

            # 提供额外的便利信息
            click.echo(f"\n📁 临时文件位置: {local_path}")
            click.echo(f"💡 提示: 你可以手动打开此文件夹访问下载的文件")

            # 尝试打开文件夹（仅Windows）
            if local_path.exists():
                try:
                    import subprocess
                    import os
                    if os.name == 'nt':  # Windows
                        click.echo("📂 正在打开文件位置...")
                        subprocess.run(['explorer', str(local_path)], check=True)
                        logger.info("✅ 已自动打开文件位置")
                except Exception as e:
                    logger.info(f"ℹ️  无法自动打开文件夹: {e}")
                    click.echo("💡 请手动复制上面的路径到文件资源管理器中打开")

        # 最终报告
        logger.info("=" * 50)
        logger.info("执行完成")
        logger.info("=" * 50)
        logger.info(f"下载: {success_count} 成功, {fail_count} 失败")

        if upload_sftp:
            # 这里可以从upload_results获取上传统计
            logger.info(f"SFTP上传: 已完成")

        click.echo(f"\n🎉 任务完成！")

        # 下载位置信息
        click.echo(f"📥 下载位置: {local_path}")

        # 临时文件状态
        if keep_temp:
            click.echo(f"💾 临时文件: 已保留 ({local_path})")
            # 显示文件夹大小
            if local_path.exists():
                try:
                    import os
                    size = sum(f.stat().st_size for f in local_path.rglob('*') if f.is_file())
                    size_mb = size / (1024 * 1024)
                    click.echo(f"📊 文件大小: {size_mb:.2f} MB")
                except:
                    pass
        else:
            click.echo(f"🗑️  临时文件: 已清理")

        # SFTP上传状态
        if upload_sftp:
            click.echo(f"☁️  SFTP上传: {get_config().sftp_remote_path}")

        # 提供后续操作建议
        if keep_temp and local_path.exists():
            click.echo(f"\n💡 下一步操作:")
            click.echo(f"   - 查看文件: {local_path}")
            click.echo(f"   - 手动上传到其他位置")
            click.echo(f"   - 完成后手动删除此文件夹")

    except ValueError as e:
        logger.error(f"配置错误: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"执行错误: {e}", exc_info=verbose)
        sys.exit(1)


def download_folder(remote_folder: str, local_path: Path):
    """
    使用bypy下载文件夹

    Args:
        remote_folder: 远程文件夹路径
        local_path: 本地保存路径

    Returns:
        下载结果列表
    """
    logger = logging.getLogger(__name__)

    try:
        # 创建bypy实例
        byp = ByPy()

        # 确保路径以/开头
        if not remote_folder.startswith('/'):
            remote_folder = '/' + remote_folder

        logger.info(f"下载路径: {remote_folder}")

        # 获取远程文件列表
        logger.info("获取文件列表...")
        # 这里bypy会自动列出文件

        # 下载文件
        logger.info(f"开始下载到: {local_path}")

        # 检查路径长度，使用更激进的策略
        # 针对用户报告的长文件名问题，直接使用系统临时目录的极短路径
        max_safe_filename_length = 200  # 文件名最大安全长度
        estimated_path_length = len(str(local_path)) + max_safe_filename_length

        # 如果预计路径超过250字符，强制使用更短的临时目录
        if estimated_path_length > 250:
            logger.warning(f"⚠️  检测到路径可能过长 ({estimated_path_length} 字符)")
            logger.warning(f"强制使用系统临时目录的极短路径")

            # 使用系统临时目录，但创建极短的子目录名
            import tempfile
            pid_suffix = str(os.getpid())[-3:]  # 仅使用PID后3位
            ultra_short_path = Path(tempfile.gettempdir()) / f"dl_{pid_suffix}"
            ultra_short_path.mkdir(parents=True, exist_ok=True)

            logger.info(f"使用极短路径: {ultra_short_path}")
            logger.info(f"极短路径长度: {len(str(ultra_short_path))} 字符")

            # 计算新路径的预计长度
            new_estimated_length = len(str(ultra_short_path)) + max_safe_filename_length
            logger.info(f"新路径预计长度: {new_estimated_length} 字符")

            if new_estimated_length <= 260:
                local_path = ultra_short_path
                logger.info("✅ 路径长度现在在安全范围内")
            else:
                logger.error("❌ 即使使用极短路径，仍然可能超过限制")
                # 尝试使用更短的方案
                local_path = ultra_short_path  # 无论如何都使用短路径

        local_path.mkdir(parents=True, exist_ok=True)

        # 使用bypy的download方法，并实施实时文件名监控
        try:
            # 启动一个后台线程来监控和处理长文件名
            import threading
            import time

            def monitor_and_rename_files():
                """后台线程：实时监控并重命名过长文件名"""
                time.sleep(2)  # 等待bypy开始下载
                max_attempts = 60  # 最多监控60次（10分钟）
                processed_files = set()

                for attempt in range(max_attempts):
                    try:
                        # 扫描当前目录中的文件
                        current_files = list(local_path.rglob('*'))
                        current_files = [f for f in current_files if f.is_file()]

                        for file in current_files:
                            if file.name not in processed_files and len(file.name) > 200:
                                try:
                                    # 立即重命名过长文件名
                                    safe_filename = sanitize_filename(file.name)
                                    safe_file = file.parent / safe_filename

                                    if safe_file != file:
                                        logger.info(f"🔄 发现过长文件名，立即重命名: {file.name[:50]}...")
                                        if safe_file.exists():
                                            # 目标文件已存在，删除源文件
                                            file.unlink()
                                            logger.info(f"   删除重复文件")
                                        else:
                                            # 重命名文件
                                            file.rename(safe_file)
                                            logger.info(f"   重命名为: {safe_filename[:50]}...")

                                        processed_files.add(file.name)
                                        processed_files.add(safe_filename)

                                except Exception as rename_error:
                                    logger.warning(f"实时重命名失败 {file.name}: {rename_error}")

                        time.sleep(10)  # 每10秒检查一次

                    except Exception as e:
                        logger.debug(f"监控过程出错: {e}")
                        time.sleep(5)

            # 启动监控线程
            monitor_thread = threading.Thread(target=monitor_and_rename_files, daemon=True)
            monitor_thread.start()

            # 执行bypy下载
            result = byp.download(remote_folder, str(local_path))
            logger.info(f"bypy下载完成")

            # 等待监控线程完成处理
            time.sleep(3)

            # 最终清理：再次扫描并清理所有过长文件名
            logger.info("执行最终文件名清理...")
            from .utils import sanitize_filename
            renamed_count = 0

            for file in local_path.rglob('*'):
                if file.is_file():
                    try:
                        safe_filename = sanitize_filename(file.name)
                        safe_file = file.parent / safe_filename

                        if safe_file != file:
                            if safe_file.exists():
                                file.unlink()
                            else:
                                file.rename(safe_file)
                            renamed_count += 1
                            logger.info(f"重命名: {file.name[:50]}... -> {safe_filename[:50]}...")
                    except Exception as e:
                        logger.warning(f"最终重命名失败 {file.name}: {e}")

            if renamed_count > 0:
                logger.info(f"✅ 最终清理完成，处理了 {renamed_count} 个文件")

            # 创建下载结果
            return create_download_result(local_path, True, "所有文件")
        except Exception as e:
            logger.error(f"bypy下载失败: {e}")
            return create_download_result(local_path, False, f"下载失败: {e}")

    except Exception as e:
        logger.error(f"下载过程失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []


def create_download_result(local_path: Path, success: bool, message: str):
    """创建下载结果对象"""
    from .downloader import DownloadResult

    # 列出本地文件
    if local_path.exists() and local_path.is_dir():
        files = list(local_path.rglob('*'))
        return [
            DownloadResult(
                success=True,
                local_path=str(file),
                remote_path=file.name,
                size=file.stat().st_size if file.exists() else 0,
                error=None
            )
            for file in files if file.is_file()
        ]
    else:
        return [
            DownloadResult(
                success=success,
                local_path=str(local_path),
                remote_path="unknown",
                size=0,
                error=message
            )
        ]


def setup_bypy_wizard():
    """bypy认证向导 - 使用内置bypy模块"""
    logger = logging.getLogger(__name__)

    click.echo("=" * 60)
    click.echo("百度网盘 bypy 认证向导")
    click.echo("=" * 60)
    click.echo("")

    try:
        # 检查bypy是否可用
        click.echo("1. 检查bypy可用性...")
        if not BYPY_AVAILABLE:
            click.echo("❌ bypy模块不可用")
            click.echo("请确保程序正确打包，包含了bypy模块")
            return

        try:
            byp = ByPy()
            click.echo("✅ bypy模块已加载")
        except Exception as e:
            click.echo(f"❌ bypy初始化失败: {e}")
            return

        click.echo("")
        click.echo("2. 百度网盘认证说明...")
        click.echo("")
        click.echo("bypy使用OAuth认证方式，需要你手动完成认证:")
        click.echo("")
        click.echo("方法一: 使用Python环境认证（推荐）")
        click.echo("  1. 在有Python环境的电脑上安装bypy:")
        click.echo("     pip install bypy")
        click.echo("  2. 运行认证命令:")
        click.echo("     bypy info")
        click.echo("  3. 按提示完成OAuth认证")
        click.echo("  4. 认证成功后，复制认证文件到目标机器:")
        click.echo("     - 文件位置: ~/.bypy/ (或 %USERPROFILE%\.bypy\\)")
        click.echo("     - 包含文件: token.json, cookie.json 等")
        click.echo("")
        click.echo("方法二: 手动创建认证文件")
        click.echo("  1. 在已认证的机器上找到认证文件")
        click.echo("  2. 复制到目标机器的相同位置")
        click.echo("  3. 确保文件结构一致")
        click.echo("")
        click.echo("方法三: 环境变量配置（高级）")
        click.echo("  1. 编辑 .env 文件")
        click.echo("  2. 设置 BAIDU_BDUSS 和 BAIDU_COOKIES")
        click.echo("  3. 这些信息可以从浏览器开发者工具获取")
        click.echo("")

        click.echo("=" * 60)
        click.echo("3. 验证认证状态...")
        click.echo("=" * 60)
        click.echo("")

        try:
            # 尝试获取配额信息来验证认证
            click.echo("正在验证认证状态...")
            from bypy import bypy
            import sys
            from io import StringIO

            # 重定向输出
            old_stdout = sys.stdout
            sys.stdout = captured_output = StringIO()

            try:
                byp.quota()
                output = captured_output.getvalue()
                click.echo("✅ 认证验证成功！")
                if output.strip():
                    click.echo("")
                    click.echo("百度网盘配额信息:")
                    click.echo(output)
            except Exception as e:
                click.echo(f"❌ 认证验证失败: {e}")
                click.echo("请按照上述方法完成认证配置")
            finally:
                sys.stdout = old_stdout

        except Exception as e:
            click.echo(f"❌ 验证过程出错: {e}")

        click.echo("=" * 60)
        click.echo("")
        click.echo("📝 认证配置说明")
        click.echo("=" * 60)
        click.echo("")
        click.echo("由于本程序是打包版本，bypy认证文件需要手动配置。")
        click.echo("最简单的方法是在一台有Python环境的电脑上完成认证，")
        click.echo("然后将认证文件复制到目标机器。")
        click.echo("")
        click.echo("认证文件位置:")
        click.echo("  - Windows: %USERPROFILE%\\.bypy\\")
        click.echo("  - Linux/Mac: ~/.bypy/")
        click.echo("")
        click.echo("需要复制的文件:")
        click.echo("  - token.json (OAuth令牌)")
        click.echo("  - cookie.json (认证Cookie)")
        click.echo("  - 其他相关配置文件")
        click.echo("")

        # 检查当前认证状态
        click.echo("=" * 60)
        click.echo("4. 检查当前认证文件...")
        click.echo("=" * 60)
        click.echo("")

        import os
        bypy_dir = os.path.expanduser("~/.bypy")
        if os.path.exists(bypy_dir):
            files = os.listdir(bypy_dir)
            if files:
                click.echo(f"✅ 发现认证文件: {bypy_dir}")
                for file in files:
                    file_path = os.path.join(bypy_dir, file)
                    if os.path.isfile(file_path):
                        size = os.path.getsize(file_path)
                        click.echo(f"   - {file} ({size} bytes)")
            else:
                click.echo(f"⚠️  认证目录存在但为空: {bypy_dir}")
        else:
            click.echo(f"❌ 未找到认证目录: {bypy_dir}")
            click.echo("请按照上述说明配置认证文件")

        click.echo("")
        click.echo("=" * 60)
        click.echo("")
        click.echo("认证配置完成后，可以运行以下命令测试:")
        click.echo("  pan-download --test-config")
        click.echo("")

    except Exception as e:
        click.echo(f"❌ 认证向导失败: {e}")
        logger.error(f"认证向导失败: {e}")


def test_configuration():
    """测试配置是否正确"""
    logger = logging.getLogger(__name__)

    click.echo("=" * 60)
    click.echo("配置测试")
    click.echo("=" * 60)
    click.echo("")

    all_ok = True

    try:
        # 测试bypy配置
        click.echo("1. 测试bypy配置...")
        if not BYPY_AVAILABLE:
            click.echo("❌ bypy模块不可用")
            click.echo("   请确保程序正确打包")
            all_ok = False
        else:
            try:
                byp = ByPy()
                # 尝试调用bypy功能来验证配置
                from bypy import bypy
                import sys
                from io import StringIO

                # 重定向输出
                old_stdout = sys.stdout
                sys.stdout = captured_output = StringIO()

                try:
                    byp.quota()
                    output = captured_output.getvalue()
                    click.echo("✅ bypy配置正常")
                    if output.strip():
                        click.echo(f"   配额信息: {output.strip()[:100]}...")
                except Exception as e:
                    click.echo(f"❌ bypy配置有问题: {e}")
                    click.echo("   请运行: pan-download --setup-bypy")
                    all_ok = False
                finally:
                    sys.stdout = old_stdout

            except Exception as e:
                click.echo(f"❌ bypy初始化失败: {e}")
                all_ok = False

        click.echo("")

        # 测试SFTP配置
        click.echo("2. 测试SFTP配置...")
        try:
            from .config import get_config
            config = get_config()

            # 检查必要配置
            missing = []
            if not config.sftp_host:
                missing.append("SFTP_HOST")
            if not config.sftp_port:
                missing.append("SFTP_PORT")
            if not config.sftp_username:
                missing.append("SFTP_USERNAME")

            if missing:
                click.echo(f"❌ SFTP配置缺少必要参数: {', '.join(missing)}")
                click.echo("   请在.env文件中配置这些参数")
                all_ok = False
            else:
                click.echo("✅ SFTP配置完整")

                # 尝试连接SFTP
                try:
                    from .uploader import SFTPUploader
                    uploader = SFTPUploader()
                    if uploader.connect():
                        click.echo("✅ SFTP连接成功")
                        uploader.disconnect()
                    else:
                        click.echo("❌ SFTP连接失败")
                        all_ok = False
                except Exception as e:
                    click.echo(f"❌ SFTP连接出错: {e}")
                    all_ok = False

        except Exception as e:
            click.echo(f"❌ 配置文件有问题: {e}")
            all_ok = False

        click.echo("")
        click.echo("=" * 60)
        if all_ok:
            click.echo("🎉 所有配置检查通过！可以开始使用。")
        else:
            click.echo("⚠️  有些配置需要修复，请按照提示操作。")
        click.echo("=" * 60)

    except Exception as e:
        click.echo(f"❌ 配置测试失败: {e}")
        logger.error(f"配置测试失败: {e}")


def extract_folder_name(remote_path: str) -> str:
    """
    从远程路径中提取文件夹名称

    Args:
        remote_path: 远程路径，如 "apps/bypy/test_pdf" 或 "test_pdf"

    Returns:
        文件夹名称，如 "test_pdf"

    Examples:
        >>> extract_folder_name("apps/bypy/test_pdf")
        'test_pdf'
        >>> extract_folder_name("test_pdf")
        'test_pdf'
        >>> extract_folder_name("/apps/bypy/test_pdf/")
        'test_pdf'
    """
    # 移除前导和尾随的斜杠
    clean_path = remote_path.strip('/')

    # 分割路径并获取最后一个非空部分
    parts = [p for p in clean_path.split('/') if p]

    if parts:
        folder_name = parts[-1]
        logger = logging.getLogger(__name__)
        logger.info(f"从路径 '{remote_path}' 提取文件夹名称: '{folder_name}'")
        return folder_name
    else:
        # 如果路径为空，返回默认名称
        return "upload"


if __name__ == '__main__':
    main()
