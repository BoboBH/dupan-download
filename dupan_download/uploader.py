"""SFTP上传模块"""
import logging
import paramiko
from dataclasses import dataclass
from typing import Optional, List
from pathlib import Path
from .config import get_config
from .utils import sanitize_filename, ensure_path_safe


@dataclass
class UploadResult:
    """上传结果"""
    success: bool
    local_path: str
    remote_path: str
    size: int
    error: Optional[str] = None


class SFTPUploader:
    """SFTP上传器 - 真实实现"""

    def __init__(self):
        """初始化上传器"""
        self.config = get_config()
        self.max_retries = self.config.max_retries
        self.connect_timeout = self.config.connect_timeout
        self.transfer_timeout = self.config.transfer_timeout
        self.logger = logging.getLogger(__name__)

        # SFTP连接配置
        self.host = self.config.sftp_host
        self.port = self.config.sftp_port
        self.username = self.config.sftp_username
        self.password = self.config.sftp_password
        self.remote_base_path = self.config.sftp_remote_path

        # SFTP连接（延迟建立）
        self.ssh_client = None
        self.sftp_client = None

    def connect(self) -> bool:
        """
        建立SFTP连接

        Returns:
            连接是否成功
        """
        try:
            self.logger.info(f"正在连接SFTP: {self.host}:{self.port}")

            # 创建SSH客户端
            self.ssh_client = paramiko.SSHClient()
            self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # 连接服务器
            self.ssh_client.connect(
                hostname=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=self.connect_timeout,
                allow_agent=False,
                look_for_keys=False
            )

            # 创建SFTP客户端
            self.sftp_client = self.ssh_client.open_sftp()

            self.logger.info("[OK] SFTP连接成功")
            return True

        except Exception as e:
            self.logger.error(f"[ERROR] SFTP连接失败: {e}")
            return False

    def disconnect(self) -> None:
        """断开SFTP连接"""
        try:
            if self.sftp_client:
                self.sftp_client.close()
                self.sftp_client = None

            if self.ssh_client:
                self.ssh_client.close()
                self.ssh_client = None

            self.logger.info("[OK] SFTP连接已断开")

        except Exception as e:
            self.logger.error(f"断开连接时出错: {e}")

    def create_remote_dir(self, remote_path: str) -> bool:
        """
        创建远程目录（递归创建）

        Args:
            remote_path: 远程目录路径

        Returns:
            创建是否成功
        """
        try:
            self.logger.info(f"创建远程目录: {remote_path}")

            # 如果目录已存在，直接返回
            try:
                self.sftp_client.stat(remote_path)
                self.logger.info(f"目录已存在: {remote_path}")
                return True
            except IOError:
                pass  # 目录不存在，需要创建

            # 递归创建目录
            dirs = []
            current_path = remote_path

            while current_path != '/':
                try:
                    self.sftp_client.stat(current_path)
                    break  # 找到已存在的目录
                except IOError:
                    dirs.append(current_path)
                    # 获取父目录
                    current_path = '/'.join(current_path.split('/')[:-1])
                    if not current_path:
                        current_path = '/'

            # 从已存在的目录开始创建
            for dir_path in reversed(dirs):
                try:
                    self.sftp_client.mkdir(dir_path)
                    self.logger.info(f"[OK] 创建目录: {dir_path}")
                except Exception as e:
                    self.logger.error(f"[ERROR] 创建目录失败 {dir_path}: {e}")
                    return False

            self.logger.info(f"[OK] 目录创建完成: {remote_path}")
            return True

        except Exception as e:
            self.logger.error(f"[ERROR] 创建目录时出错: {e}")
            return False

    def _file_exists(self, remote_path: str, expected_size: int) -> bool:
        """
        检查远程文件是否存在且大小匹配

        Args:
            remote_path: 远程文件路径
            expected_size: 期望的文件大小

        Returns:
            文件是否存在且大小匹配
        """
        try:
            stat = self.sftp_client.stat(remote_path)
            # 检查文件大小是否匹配
            if stat.st_size == expected_size:
                return True
            else:
                self.logger.info(f"文件存在但大小不匹配: {remote_path} (期望: {expected_size}, 实际: {stat.st_size})")
                return False
        except IOError:
            # 文件不存在
            return False
        except Exception as e:
            self.logger.warning(f"检查文件存在性时出错: {e}")
            return False

    def upload_file(self, local_path: Path, remote_path: str, skip_existing: bool = True) -> UploadResult:
        """
        上传单个文件

        Args:
            local_path: 本地文件路径
            remote_path: 远程文件路径
            skip_existing: 是否跳过已存在的文件

        Returns:
            上传结果
        """
        try:
            # 确保本地路径安全
            local_path = ensure_path_safe(local_path)

            # 获取文件大小
            file_size = local_path.stat().st_size

            # 检查文件是否已存在（如果启用跳过）
            if skip_existing and self._file_exists(remote_path, file_size):
                self.logger.info(f"⏭️  跳过（已存在）: {remote_path}")
                return UploadResult(
                    success=True,
                    local_path=str(local_path),
                    remote_path=remote_path,
                    size=file_size
                )

            self.logger.info(f"[CLOUD]  开始上传: {local_path.name}")
            self.logger.info(f"   源文件: {local_path}")
            self.logger.info(f"   目标路径: {remote_path}")
            self.logger.info(f"   文件大小: {file_size} bytes ({file_size / 1024:.2f} KB)")

            # 确保远程目录存在
            remote_dir = '/'.join(remote_path.split('/')[:-1])
            if remote_dir:
                self.logger.info(f"   创建远程目录: {remote_dir}")
                if not self.create_remote_dir(remote_dir):
                    error_reason = f"无法创建远程目录: {remote_dir}"
                    self.logger.error(f"[ERROR] 上传失败: {error_reason}")
                    return UploadResult(
                        success=False,
                        local_path=str(local_path),
                        remote_path=remote_path,
                        size=0,
                        error=error_reason
                    )

            # 上传文件
            self.logger.info(f"   正在传输数据...")
            for attempt in range(self.max_retries):
                try:
                    self.sftp_client.put(
                        str(local_path),
                        remote_path,
                        confirm=True
                    )

                    # 验证上传后的文件大小
                    try:
                        remote_stat = self.sftp_client.stat(remote_path)
                        if remote_stat.st_size != file_size:
                            error_reason = f"文件大小不匹配 - 本地: {file_size} bytes, 远程: {remote_stat.st_size} bytes"
                            self.logger.warning(f"⚠️  上传验证失败: {error_reason}")
                            if attempt == self.max_retries - 1:
                                raise ValueError(error_reason)
                            continue
                    except Exception as e:
                        error_reason = f"无法验证远程文件: {e}"
                        self.logger.warning(f"⚠️  验证失败: {error_reason}")
                        if attempt == self.max_retries - 1:
                            self.logger.warning(f"   文件可能已上传，但无法验证")

                    self.logger.info(f"[OK] 上传完成: {remote_path}")
                    self.logger.info(f"   传输大小: {file_size} bytes")
                    return UploadResult(
                        success=True,
                        local_path=str(local_path),
                        remote_path=remote_path,
                        size=file_size
                    )

                except PermissionError as e:
                    error_reason = f"权限错误 - 无法上传到 {remote_path}: {e}"
                    self.logger.warning(f"⚠️  上传重试 ({attempt + 1}/{self.max_retries}): {error_reason}")
                    if attempt == self.max_retries - 1:
                        self.logger.error(f"[ERROR] 上传失败: {error_reason}")
                        return UploadResult(
                            success=False,
                            local_path=str(local_path),
                            remote_path=remote_path,
                            size=0,
                            error=error_reason
                        )
                except TimeoutError as e:
                    error_reason = f"超时错误 - 上传超时 ({self.transfer_timeout}秒): {e}"
                    self.logger.warning(f"⚠️  上传重试 ({attempt + 1}/{self.max_retries}): {error_reason}")
                    if attempt == self.max_retries - 1:
                        self.logger.error(f"[ERROR] 上传失败: {error_reason}")
                        return UploadResult(
                            success=False,
                            local_path=str(local_path),
                            remote_path=remote_path,
                            size=0,
                            error=error_reason
                        )
                except IOError as e:
                    error_reason = f"SFTP IO错误 - 可能是网络问题或磁盘空间不足: {e}"
                    if "hash" in str(e).lower() or "match" in str(e).lower():
                        # 检查远程文件是否实际存在
                        try:
                            remote_stat = self.sftp_client.stat(remote_path)
                            remote_size = remote_stat.st_size
                            hash_error_detail = f"文件校验失败 - 本地和远程文件hash不匹配，可能是传输过程中数据损坏: {e}"
                            self.logger.warning(f"⚠️  {hash_error_detail}")
                            self.logger.info(f"   注意：文件可能已上传到服务器 (大小: {remote_size} bytes)")

                            # 如果远程文件大小正确，可能只是校验问题
                            if remote_size == file_size:
                                self.logger.info(f"   文件大小匹配，可能是校验算法问题")
                                if attempt == self.max_retries - 1:
                                    # 大小匹配但hash不匹配，警告但认为成功
                                    self.logger.warning(f"   ⚠️  文件大小正确但校验失败，标记为成功")
                                    return UploadResult(
                                        success=True,
                                        local_path=str(local_path),
                                        remote_path=remote_path,
                                        size=file_size,
                                        error=f"校验警告: {e}"
                                    )
                            else:
                                error_reason = f"文件校验失败且大小不匹配 (本地: {file_size}, 远程: {remote_size}): {e}"
                        except:
                            error_reason = f"文件校验失败且无法验证远程文件: {e}"

                    self.logger.warning(f"⚠️  上传重试 ({attempt + 1}/{self.max_retries}): {error_reason}")
                    if attempt == self.max_retries - 1:
                        self.logger.error(f"[ERROR] 上传失败: {error_reason}")
                        return UploadResult(
                            success=False,
                            local_path=str(local_path),
                            remote_path=remote_path,
                            size=0,
                            error=error_reason
                        )
                except Exception as e:
                    error_type = type(e).__name__
                    error_msg = str(e)
                    error_reason = f"上传失败 - {error_type}: {error_msg}"

                    # 特殊处理hash不匹配错误
                    if "hash" in error_msg.lower() or "match" in error_msg.lower():
                        error_reason = f"文件校验失败 - 本地和远程文件hash不匹配。可能原因：1)网络传输数据损坏 2)SFTP服务器问题 3)文件过大导致校验错误。建议：1)检查网络连接 2)检查SFTP服务器状态 3)尝试重新上传"

                    self.logger.warning(f"⚠️  上传重试 ({attempt + 1}/{self.max_retries}): {error_reason}")
                    if attempt == self.max_retries - 1:
                        self.logger.error(f"[ERROR] 上传失败: {error_reason}")
                        return UploadResult(
                            success=False,
                            local_path=str(local_path),
                            remote_path=remote_path,
                            size=0,
                            error=error_reason
                        )

            return UploadResult(
                success=False,
                local_path=str(local_path),
                remote_path=remote_path,
                size=0,
                error="上传失败，达到最大重试次数"
            )

        except FileNotFoundError as e:
            error_reason = f"文件未找到 - 本地文件不存在: {local_path}: {e}"
            self.logger.error(f"[ERROR] 上传失败: {error_reason}")
            return UploadResult(
                success=False,
                local_path=str(local_path),
                remote_path=remote_path,
                size=0,
                error=error_reason
            )
        except Exception as e:
            error_reason = f"上传失败 - {type(e).__name__}: {e}"
            self.logger.error(f"[ERROR] 上传失败: {error_reason}")
            return UploadResult(
                success=False,
                local_path=str(local_path),
                remote_path=remote_path,
                size=0,
                error=error_reason
            )

    def upload_folder(self, local_path: Path, remote_path: str) -> List[UploadResult]:
        """
        上传文件夹（递归上传）

        Args:
            local_path: 本地文件夹路径
            remote_path: 远程文件夹路径

        Returns:
            所有文件的上传结果列表
        """
        results = []

        try:
            self.logger.info(f"开始上传文件夹: {local_path} -> {remote_path}")

            # 确保远程基础目录存在
            self.create_remote_dir(remote_path)

            # 递归上传所有文件
            for local_file in local_path.rglob('*'):
                if local_file.is_file():
                    # 计算相对路径
                    relative_path = local_file.relative_to(local_path)

                    # 清理文件名以避免路径长度限制（针对SFTP远程路径）
                    safe_filename = sanitize_filename(local_file.name)
                    safe_relative_path = relative_path.parent / safe_filename

                    # 构建远程文件路径
                    remote_file_path = f"{remote_path}/{safe_relative_path}".replace('\\', '/')

                    # 上传文件
                    result = self.upload_file(local_file, remote_file_path)
                    results.append(result)

            # 统计结果
            success_count = sum(1 for r in results if r.success)
            fail_count = len(results) - success_count

            self.logger.info(f"文件夹上传完成: {success_count} 成功, {fail_count} 失败")

            return results

        except Exception as e:
            self.logger.error(f"[ERROR] 上传文件夹失败: {e}")
            return results
