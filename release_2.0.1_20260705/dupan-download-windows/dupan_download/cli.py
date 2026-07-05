"""命令行接口模块"""
import sys
import click
import logging
from pathlib import Path
from typing import Optional

from .config import get_config
from .downloader import BaiduDownloader
from .uploader import SFTPUploader
from .utils import create_temp_dir, cleanup_temp_dir, setup_logger, mask_sensitive_info


@click.command()
@click.argument('share_link')
@click.argument('extract_code')
@click.option('--keep-temp', is_flag=True, help='保留临时文件')
@click.option('--temp-dir', type=click.Path(), help='指定临时目录')
@click.option('--verbose', is_flag=True, help='详细输出模式')
def main(share_link: str, extract_code: str, keep_temp: bool,
         temp_dir: Optional[str], verbose: bool):
    """
    百度网盘自动下载SFTP上传工具

    从百度网盘下载文件夹并上传到SFTP服务器
    """
    # 设置日志
    logger = setup_logger('dupan_download', verbose=verbose)

    try:
        # 验证配置
        config = get_config()
        logger.info("配置加载成功")

        # 创建临时目录
        if temp_dir:
            temp_path = create_temp_dir(base_dir=temp_dir)
        else:
            temp_path = create_temp_dir()
        logger.info(f"临时目录: {temp_path}")

        # 初始化下载器
        downloader = BaiduDownloader()
        logger.info("下载器初始化完成")

        # 验证链接
        logger.info(f"验证链接: {mask_sensitive_info(share_link)}")
        if not downloader.validate_link(share_link, extract_code):
            logger.error("链接验证失败，请检查链接和提取码")
            sys.exit(1)

        logger.info("链接验证成功")

        # 下载文件
        logger.info("开始下载文件...")
        download_results = downloader.download_folder(share_link, temp_path)

        success_count = sum(1 for r in download_results if r.success)
        fail_count = len(download_results) - success_count

        logger.info(f"下载完成: {success_count} 成功, {fail_count} 失败")

        if fail_count > 0:
            logger.warning("失败的文件:")
            for result in download_results:
                if not result.success:
                    logger.warning(f"  - {result.remote_path}: {result.error}")

        # 如果有成功下载的文件，继续上传流程
        if success_count > 0:
            # 初始化上传器
            uploader = SFTPUploader()
            logger.info("上传器初始化完成")

            # 连接SFTP
            if not uploader.connect():
                logger.error("SFTP连接失败")
                sys.exit(1)

            try:
                logger.info("开始上传文件...")
                upload_results = uploader.upload_folder(temp_path, config.sftp_remote_path)

                success_count = sum(1 for r in upload_results if r.success)
                fail_count = len(upload_results) - success_count

                logger.info(f"上传完成: {success_count} 成功, {fail_count} 失败")

                if fail_count > 0:
                    logger.warning("失败的文件:")
                    for result in upload_results:
                        if not result.success:
                            logger.warning(f"  - {result.local_path}: {result.error}")

            finally:
                uploader.disconnect()
        else:
            logger.info("没有文件被成功下载，跳过上传步骤")

        # 清理临时文件
        if not keep_temp:
            cleanup_temp_dir(temp_path)
            logger.info("清理临时文件")
        else:
            logger.info(f"保留临时文件: {temp_path}")

        # 最终报告
        total_success = success_count
        total_fail = fail_count

        click.echo("\n执行完成")
        click.echo(f"成功处理: {total_success} 个文件")
        if total_fail > 0:
            click.echo(f"失败: {total_fail} 个文件")

    except ValueError as e:
        logger.error(f"配置错误: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"执行错误: {e}", exc_info=verbose)
        sys.exit(1)


if __name__ == '__main__':
    main()
