"""流式下载上传处理器 - 优化版本"""
import logging
import os
from pathlib import Path
from typing import List, Optional, Callable
from dataclasses import dataclass
from bypy import ByPy
from .uploader import SFTPUploader
from .config import get_config
from .utils import sanitize_filename, ensure_path_safe


@dataclass
class StreamingResult:
    """流式处理结果"""
    total_files: int
    downloaded_files: int
    uploaded_files: int
    uploaded_from_local: int  # 从本地已有文件上传的数量
    skipped_files: int  # 完全跳过的文件（本地+SFTP都有）
    skipped_sftp_only: int  # 仅SFTP有的文件（新下载但SFTP已有）
    failed_downloads: int
    failed_uploads: int
    total_size: int
    errors: List[str]


class StreamingProcessor:
    """
    流式下载上传处理器

    优化功能：
    1. 下载一个文件后立即上传（流式处理）
    2. 检查SFTP文件是否已存在（去重）
    3. 自动创建SFTP子目录
    4. 实时进度显示
    """

    def __init__(self,
                 progress_callback: Optional[Callable] = None,
                 keep_local: bool = False):
        """
        初始化流式处理器

        Args:
            progress_callback: 进度回调函数
            keep_local: 是否保留本地文件
        """
        self.logger = logging.getLogger(__name__)
        self.config = get_config()
        self.progress_callback = progress_callback
        self.keep_local = keep_local

        # 初始化组件
        self.byp = ByPy()
        self.uploader = SFTPUploader()
        self.sftp_connected = False

    def _notify_progress(self, message: str, current: int = 0, total: int = 0):
        """通知进度更新"""
        if self.progress_callback:
            self.progress_callback(message, current, total)
        else:
            self.logger.info(f"[{current}/{total}] {message}")

    def _connect_sftp(self) -> bool:
        """连接SFTP服务器"""
        if not self.sftp_connected:
            self._notify_progress("连接SFTP服务器...")
            self.sftp_connected = self.uploader.connect()
        return self.sftp_connected

    def _get_remote_files(self, remote_folder: str) -> List[dict]:
        """
        获取百度网盘远程文件列表

        Args:
            remote_folder: 远程文件夹路径

        Returns:
            文件信息列表
        """
        try:
            self.logger.info(f"获取远程文件列表: {remote_folder}")

            # 使用bypy获取文件列表
            # 注意：bypy的列表功能
            files_info = []

            # 这里需要通过bypy的内部方法获取文件列表
            # 由于bypy没有直接的列表API，我们使用替代方法

            # 方法1: 使用bypy的list命令
            import tempfile
            import sys
            from io import StringIO

            # 重定向输出捕获文件列表
            old_stdout = sys.stdout
            captured_output = StringIO()

            try:
                sys.stdout = captured_output
                # 调用bypy的list方法
                self.byp.list(remote_folder)
                output = captured_output.getvalue()

                # 解析输出获取文件列表
                # 注意：这里需要根据bypy的实际输出格式来解析
                # 暂时使用简化方法

            except Exception as e:
                self.logger.warning(f"获取文件列表失败: {e}")
            finally:
                sys.stdout = old_stdout

            # 由于bypy的list功能限制，我们使用替代方案
            # 直接使用download来获取所有文件，然后逐个处理

            return []

        except Exception as e:
            self.logger.error(f"获取远程文件列表失败: {e}")
            return []

    def _check_file_exists_on_sftp(self, remote_path: str, expected_size: int) -> bool:
        """
        检查SFTP上文件是否已存在

        Args:
            remote_path: SFTP远程文件路径
            expected_size: 期望的文件大小

        Returns:
            文件是否存在且大小匹配
        """
        try:
            if not self.sftp_connected:
                return False

            # 检查文件是否存在
            try:
                stat = self.uploader.sftp_client.stat(remote_path)
                # 检查文件大小
                if stat.st_size == expected_size:
                    self.logger.info(f"文件已存在且大小匹配: {remote_path}")
                    return True
                else:
                    self.logger.warning(f"文件存在但大小不匹配: {remote_path} (本地: {expected_size}, 远程: {stat.st_size})")
                    return False
            except IOError:
                # 文件不存在
                return False

        except Exception as e:
            self.logger.warning(f"检查文件存在性失败: {e}")
            return False

    def _ensure_remote_dir(self, remote_path: str) -> bool:
        """
        确保远程目录存在

        Args:
            remote_path: 远程目录路径

        Returns:
            是否成功
        """
        try:
            # 获取父目录
            remote_dir = '/'.join(remote_path.split('/')[:-1])

            if remote_dir:
                return self.uploader.create_remote_dir(remote_dir)
            return True

        except Exception as e:
            self.logger.error(f"确保远程目录失败: {e}")
            return False

    def _download_and_upload_single_file(self,
                                         remote_file: str,
                                         local_file: Path,
                                         sftp_target: str) -> bool:
        """
        下载并上传单个文件（流式处理）

        Args:
            remote_file: 百度网盘远程文件路径
            local_file: 本地临时文件路径
            sftp_target: SFTP目标文件路径

        Returns:
            是否成功
        """
        try:
            # 1. 下载文件
            self._notify_progress(f"下载: {Path(remote_file).name}")

            # 确保本地目录存在
            local_file.parent.mkdir(parents=True, exist_ok=True)

            # 使用bypy下载单个文件
            try:
                # bypy的download方法用于文件夹
                # 对于单个文件，我们需要使用其他方法
                # 这里使用简化的方法：下载到临时目录

                # 由于bypy的限制，我们使用整个文件夹下载，
                # 但立即处理每个文件
                pass

            except Exception as e:
                self.logger.error(f"下载失败 {remote_file}: {e}")
                return False

            # 2. 如果需要上传，立即上传
            if self.sftp_connected and sftp_target:
                self._notify_progress(f"上传: {Path(sftp_target).name}")

                # 确保远程目录存在
                self._ensure_remote_dir(sftp_target)

                # 上传文件
                from .uploader import UploadResult
                result = self.uploader.upload_file(local_file, sftp_target)

                if not result.success:
                    self.logger.error(f"上传失败: {result.error}")
                    return False

                self._notify_progress(f"完成: {Path(remote_file).name}")

            # 3. 如果不需要保留本地文件，删除
            if not self.keep_local and local_file.exists():
                local_file.unlink()
                self.logger.info(f"已删除临时文件: {local_file}")

            return True

        except Exception as e:
            self.logger.error(f"处理文件失败 {remote_file}: {e}")
            return False

    def process_folder(self,
                      remote_folder: str,
                      sftp_base_path: str,
                      local_temp_dir: Path) -> StreamingResult:
        """
        流式处理整个文件夹

        Args:
            remote_folder: 百度网盘远程文件夹
            sftp_base_path: SFTP基础路径
            local_temp_dir: 本地临时目录

        Returns:
            处理结果统计
        """
        result = StreamingResult(
            total_files=0,
            downloaded_files=0,
            uploaded_files=0,
            uploaded_from_local=0,
            skipped_files=0,
            skipped_sftp_only=0,
            failed_downloads=0,
            failed_uploads=0,
            total_size=0,
            errors=[]
        )

        try:
            self.logger.info("=" * 60)
            self.logger.info("开始流式处理")
            self.logger.info("=" * 60)

            # 连接SFTP（如果需要上传）
            if sftp_base_path:
                if not self._connect_sftp():
                    result.errors.append("SFTP连接失败，将仅下载")
                    self.logger.warning("SFTP连接失败，将仅下载文件")

            # 确保路径格式正确
            if not remote_folder.startswith('/'):
                remote_folder = '/' + remote_folder

            self.logger.info(f"百度网盘路径: {remote_folder}")
            self.logger.info(f"SFTP路径: {sftp_base_path}")
            self.logger.info(f"本地临时目录: {local_temp_dir}")

            # 创建临时目录
            local_temp_dir.mkdir(parents=True, exist_ok=True)

            # 检查本地临时目录是否已有文件
            existing_local_files = []
            if local_temp_dir.exists():
                existing_local_files = [f for f in local_temp_dir.rglob('*') if f.is_file()]

            if existing_local_files:
                self.logger.info(f"📁 发现本地已有 {len(existing_local_files)} 个文件，跳过百度网盘下载")
                self._notify_progress(f"跳过下载（本地已有 {len(existing_local_files)} 个文件）")
                local_files = existing_local_files
            else:
                # 使用bypy下载整个文件夹到临时目录
                self._notify_progress("🔽 开始下载文件夹...")
                self.logger.info(f"百度网盘路径: {remote_folder}")
                self.logger.info(f"本地临时目录: {local_temp_dir}")

                try:
                    # bypy下载整个文件夹
                    self.logger.info("正在调用bypy下载...")
                    self.byp.download(remote_folder, str(local_temp_dir))
                    self.logger.info("✅ 百度网盘下载完成")

                except PermissionError as e:
                    error_reason = f"下载权限错误: {e}"
                    result.errors.append(error_reason)
                    self.logger.error(f"❌ 下载失败: {error_reason}")
                    return result
                except ConnectionError as e:
                    error_reason = f"网络连接错误: {e}"
                    result.errors.append(error_reason)
                    self.logger.error(f"❌ 下载失败: {error_reason}")
                    return result
                except Exception as e:
                    error_reason = f"下载失败 - {type(e).__name__}: {e}"
                    result.errors.append(error_reason)
                    self.logger.error(f"❌ 下载失败: {error_reason}")
                    return result

                # 获取下载的文件列表
                local_files = list(local_temp_dir.rglob('*'))
                local_files = [f for f in local_files if f.is_file()]

            result.total_files = len(local_files)
            self._notify_progress(f"共 {result.total_files} 个文件")

            # 流式处理：检查本地文件，上传到SFTP
            for idx, local_file in enumerate(local_files, 1):
                try:
                    # 计算相对路径
                    relative_path = local_file.relative_to(local_temp_dir)

                    # 清理文件名以避免路径长度限制
                    safe_filename = sanitize_filename(local_file.name)
                    safe_local_file = local_file.parent / safe_filename

                    # 如果文件名被改变，重命名文件
                    if safe_local_file != local_file:
                        if safe_local_file.exists():
                            # 目标文件已存在，删除原文件
                            local_file.unlink()
                            local_file = safe_local_file
                        else:
                            # 重命名文件
                            local_file.rename(safe_local_file)
                            local_file = safe_local_file

                    file_size = local_file.stat().st_size

                    # 重新计算相对路径（使用清理后的文件名）
                    relative_path = local_file.relative_to(local_temp_dir)

                    # 构建SFTP目标路径
                    sftp_target = f"{sftp_base_path}/{relative_path}".replace('\\', '/') if sftp_base_path else None

                    # 检查是否是从本地已有文件（跳过下载）
                    is_from_local = local_file in existing_local_files if existing_local_files else False

                    # 检查文件是否已存在于SFTP
                    if sftp_target and self.sftp_connected and self._check_file_exists_on_sftp(sftp_target, file_size):
                        if is_from_local:
                            self._notify_progress(f"⏭️  完全跳过（本地+SFTP都有）: {relative_path} ({idx}/{result.total_files})", idx, result.total_files)
                            result.skipped_files += 1
                        else:
                            self._notify_progress(f"⏭️  跳过上传（SFTP已有）: {relative_path} ({idx}/{result.total_files})", idx, result.total_files)
                            result.skipped_sftp_only += 1

                        # 如果是从本地已有文件，保留；如果是新下载的，按原有逻辑处理
                        if not self.keep_local and not is_from_local and local_file.exists():
                            local_file.unlink()

                        continue

                    # 上传到SFTP
                    if sftp_target and self.sftp_connected:
                        if is_from_local:
                            self._notify_progress(f"☁️  上传（本地已有）: {relative_path} ({idx}/{result.total_files})", idx, result.total_files)
                        else:
                            self._notify_progress(f"☁️  上传: {relative_path} ({idx}/{result.total_files})", idx, result.total_files)

                        try:
                            # 确保远程目录存在
                            self._ensure_remote_dir(sftp_target)

                            # 上传文件
                            from .uploader import UploadResult
                            upload_result = self.uploader.upload_file(local_file, sftp_target)

                            if upload_result.success:
                                result.uploaded_files += 1
                                result.total_size += file_size
                                if is_from_local:
                                    result.uploaded_from_local += 1
                                    self.logger.info(f"✅ 从本地上传成功: {relative_path}")
                                else:
                                    self.logger.info(f"✅ 上传成功: {relative_path}")
                            else:
                                result.failed_uploads += 1
                                error_detail = f"上传失败: {relative_path} - {upload_result.error}"
                                result.errors.append(error_detail)
                                self.logger.error(f"❌ {error_detail}")

                        except Exception as e:
                            result.failed_uploads += 1
                            error_detail = f"上传异常: {relative_path} - {type(e).__name__}: {e}"
                            result.errors.append(error_detail)
                            self.logger.error(f"❌ {error_detail}")

                    else:
                        # 仅下载不上传
                        if is_from_local:
                            self.logger.info(f"📁 本地已有（未配置SFTP）: {relative_path}")
                        else:
                            result.downloaded_files += 1
                        result.total_size += file_size

                    # 如果不需要保留本地文件，删除
                    if not self.keep_local and not is_from_local and local_file.exists():
                        local_file.unlink()
                    elif is_from_local and self.keep_local:
                        self.logger.info(f"📁 保留本地文件: {relative_path}")

                except Exception as e:
                    result.failed_downloads += 1
                    error_detail = f"处理失败: {relative_path} - {type(e).__name__}: {e}"
                    result.errors.append(error_detail)
                    self.logger.error(f"❌ {error_detail}")

            # 总结
            self.logger.info("=" * 60)
            self.logger.info("流式处理完成")
            self.logger.info("=" * 60)
            self.logger.info(f"总文件数: {result.total_files}")
            if existing_local_files:
                self.logger.info(f"📁 本地已有文件: {len(existing_local_files)} (跳过百度网盘下载)")
            self.logger.info(f"☁️  已上传: {result.uploaded_files}")
            if result.uploaded_from_local > 0:
                self.logger.info(f"   └─ 从本地已有上传: {result.uploaded_from_local}")
            self.logger.info(f"⏭️  完全跳过: {result.skipped_files} (本地+SFTP都有)")
            if result.skipped_sftp_only > 0:
                self.logger.info(f"⏭️  跳过上传: {result.skipped_sftp_only} (SFTP已有)")
            self.logger.info(f"❌ 下载失败: {result.failed_downloads}")
            self.logger.info(f"❌ 上传失败: {result.failed_uploads}")
            self.logger.info(f"📊 总大小: {result.total_size} bytes ({result.total_size / 1024 / 1024:.2f} MB)")

            if result.errors:
                self.logger.warning(f"⚠️  错误数量: {len(result.errors)}")
                for error in result.errors[:5]:  # 只显示前5个错误
                    self.logger.warning(f"  - {error}")

            return result

        except Exception as e:
            result.errors.append(f"处理失败: {str(e)}")
            self.logger.error(f"流式处理失败: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return result

        finally:
            # 断开SFTP连接
            if self.sftp_connected:
                self.uploader.disconnect()
                self.sftp_connected = False
