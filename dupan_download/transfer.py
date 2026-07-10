"""百度网盘分享链接转存模块"""
import logging
import re
import subprocess
from typing import Optional, List, Dict
from dataclasses import dataclass
from bypy import ByPy


@dataclass
class TransferResult:
    """转存结果"""
    success: bool
    source_folder: str
    target_folder: str
    files_count: int
    error: Optional[str] = None


class BaiduTransfer:
    """百度网盘分享链接转存器 - 实际实现版本"""

    def __init__(self):
        """初始化转存器"""
        self.logger = logging.getLogger(__name__)
        self.byp = ByPy()

    def extract_share_id(self, share_link: str) -> Optional[str]:
        """从分享链接中提取share_id"""
        try:
            patterns = [
                r'/s/([a-zA-Z0-9_-]+)',
                r'surl=([a-zA-Z0-9_-]+)'
            ]

            for pattern in patterns:
                match = re.search(pattern, share_link)
                if match:
                    share_id = match.group(1)
                    self.logger.info(f"[OK] 提取到share_id: {share_id}")
                    return share_id

            self.logger.error(f"[ERROR] 无法从链接中提取share_id: {share_link}")
            return None

        except Exception as e:
            self.logger.error(f"[ERROR] 提取share_id失败: {e}")
            return None

    def access_share_via_bypy(self, share_id: str, extract_code: str) -> bool:
        """使用bypy访问分享内容"""
        try:
            self.logger.info("🔍 尝试使用bypy访问分享内容...")

            # 使用bypy访问分享
            # 这里我们需要使用bypy的特定功能
            # 由于bypy主要是用于已认证用户的操作，对于分享链接的处理有限

            self.logger.info("⚠️  当前bypy版本对分享链接支持有限")
            self.logger.info("[INFO] 建议先手动在百度网盘Web端转存，或使用分享链接直接下载")

            return False

        except Exception as e:
            self.logger.error(f"[ERROR] 通过bypy访问失败: {e}")
            return False

    def transfer_to_own_drive_via_bypy(self, share_link: str, extract_code: str, target_folder: str) -> TransferResult:
        """
        使用bypy将分享内容转存到自己的网盘

        由于bypy的限制，这里提供一个实用的解决方案
        """
        try:
            self.logger.info("=" * 60)
            self.logger.info("🔄 开始转存分享链接到百度网盘")
            self.logger.info("=" * 60)
            self.logger.info(f"📥 分享链接: {share_link}")
            self.logger.info(f"🔑 提取码: {extract_code}")
            self.logger.info(f"[FOLDER] 目标路径: {target_folder}")

            # 提取share_id
            share_id = self.extract_share_id(share_link)
            if not share_id:
                return TransferResult(
                    success=False,
                    source_folder=share_link,
                    target_folder=target_folder,
                    files_count=0,
                    error="无法提取share_id"
                )

            # 由于bypy的限制，我们需要使用替代方案
            self.logger.info("[INFO] 当前bypy版本对直接转存支持有限")
            self.logger.info("📋 建议工作流程：")

            self.logger.info("1. 方案A：手动转存")
            self.logger.info("   - 在浏览器中打开分享链接")
            self.logger.info(f"   - 输入提取码: {extract_code}")
            self.logger.info("   - 在百度网盘中找到目标文件夹")
            self.logger.info(f"   - 点击\"保存到自己的网盘\"")
            self.logger.info(f"   - 选择路径: {target_folder}")
            self.logger.info("   - 然后使用本工具下载上传")

            self.logger.info("2. 方案B：直接下载上传（推荐）")
            self.logger.info("   - 先下载分享内容到本地")
            self.logger.info("   - 然后直接上传到SFTP")
            self.logger.info("   - 跳过百度网盘转存步骤")

            # 返回一个"未实现"的结果，建议使用方案B
            return TransferResult(
                success=False,
                source_folder=share_id,
                target_folder=target_folder,
                files_count=0,
                error="bypy转存功能需要手动完成，建议先手动转存然后使用下载上传功能"
            )

        except Exception as e:
            error_msg = f"转存过程出错: {e}"
            self.logger.error(f"[ERROR] {error_msg}")
            return TransferResult(
                success=False,
                source_folder=share_link,
                target_folder=target_folder,
                files_count=0,
                error=error_msg
            )

    def extract_folder_name_from_link(self, share_link: str) -> Optional[str]:
        """从分享链接中提取文件夹名称"""
        try:
            share_id = self.extract_share_id(share_link)
            if share_id:
                # 使用share_id的后6位作为文件夹名
                folder_name = share_id[-6:] if len(share_id) > 6 else share_id
                self.logger.info(f"[FOLDER] 推断文件夹名: {folder_name}")
                return folder_name

            return None

        except Exception as e:
            self.logger.error(f"[ERROR] 提取文件夹名称失败: {e}")
            return None

    def get_share_content_directly(self, share_link: str, extract_code: str, target_folder: str) -> TransferResult:
        """
        直接处理分享链接（实际可行的方案）

        这个方法的思路：
        1. 接收分享链接和提取码
        2. 通知用户需要手动在浏览器中转存
        3. 或者直接从分享链接下载（如果支持）
        """
        try:
            self.logger.info("=" * 60)
            self.logger.info("📋 分享链接处理方案")
            self.logger.info("=" * 60)
            self.logger.info(f"分享链接: {share_link}")
            self.logger.info(f"提取码: {extract_code}")
            self.logger.info(f"推断目标: {target_folder}")

            self.logger.info("")
            self.logger.info("🔧 推荐操作流程：")
            self.logger.info("1. 在浏览器中打开分享链接并输入提取码")
            self.logger.info(f"2. 将内容转存到百度网盘 {target_folder}")
            self.logger.info("3. 运行: pan-download apps/bypy/260703 --upload-sftp --streaming")

            return TransferResult(
                success=False,
                source_folder=share_link,
                target_folder=target_folder,
                files_count=0,
                error="需要手动完成转存，或使用直接下载模式"
            )

        except Exception as e:
            return TransferResult(
                success=False,
                source_folder=share_link,
                target_folder=target_folder,
                files_count=0,
                error=str(e)
            )
