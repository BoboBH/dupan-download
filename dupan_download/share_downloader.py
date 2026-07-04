"""百度网盘分享链接下载器 - 支持真实下载"""
import logging
import requests
from dataclasses import dataclass
from typing import Optional, List
from pathlib import Path
import re
import os
import json
import time
from .config import get_config


@dataclass
class DownloadResult:
    """下载结果"""
    success: bool
    local_path: Optional[str]
    remote_path: str
    size: int
    error: Optional[str] = None


class ShareLinkDownloader:
    """百度网盘分享链接下载器 - 专注于分享链接下载"""

    def __init__(self):
        """初始化下载器"""
        self.config = get_config()
        self.max_retries = self.config.max_retries
        self.connect_timeout = self.config.connect_timeout
        self.transfer_timeout = self.config.transfer_timeout
        self.logger = logging.getLogger(__name__)

        # 初始化HTTP会话
        self._init_session()
        self._load_auth()

    def _init_session(self):
        """初始化HTTP会话"""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Referer': 'https://pan.baidu.com/',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Origin': 'https://pan.baidu.com',
        })

    def _load_auth(self):
        """加载百度网盘认证信息"""
        self.bduss = os.getenv('BAIDU_BDUSS')
        cookies_str = os.getenv('BAIDU_COOKIES', '')

        # 解析cookies
        cookies = {}
        if cookies_str:
            for item in cookies_str.split(';'):
                item = item.strip()
                if '=' in item:
                    key, value = item.split('=', 1)
                    cookies[key.strip()] = value.strip()

        # 确保BDUSS在cookies中
        if self.bduss and 'BDUSS' not in cookies:
            cookies['BDUSS'] = self.bduss

        # 更新会话cookies
        self.session.cookies.update(cookies)

        self.logger.info(f"认证信息加载完成 (COOKIES: {len(cookies)}个字段)")

    def validate_link(self, share_link: str, extract_code: str) -> bool:
        """验证分享链接和提取码"""
        try:
            if not share_link or 'pan.baidu.com' not in share_link:
                self.logger.error(f"无效的百度网盘链接: {share_link}")
                return False

            if not extract_code or len(extract_code) != 4:
                self.logger.error(f"提取码格式错误: {extract_code}")
                return False

            self.logger.info(f"验证链接: {share_link}, 提取码: {extract_code}")
            return True

        except Exception as e:
            self.logger.error(f"链接验证异常: {e}")
            return False

    def get_share_id(self, share_link: str) -> Optional[str]:
        """从分享链接中提取分享ID"""
        try:
            match = re.search(r'/s/([a-zA-Z0-9_-]+)', share_link)
            if match:
                return match.group(1)
            return None
        except Exception as e:
            self.logger.error(f"提取分享ID失败: {e}")
            return None

    def get_file_list(self, share_link: str, extract_code: str) -> List[dict]:
        """获取分享文件列表"""
        try:
            share_id = self.get_share_id(share_link)
            if not share_id:
                return []

            self.logger.info(f"获取分享文件列表: {share_id}")

            # 方法1: 使用分享页面API
            api_url = "https://pan.baidu.com/share/wxlist"
            params = {
                'shareid': share_id,
                'shorturl': share_id,
                'dir': '/',
                'isdir': 0,
                'order': 'time',
                'desc': 1,
                'num': 1000,  # 增加数量以支持更多文件
                'page': 1
            }

            # 添加提取码参数
            params['pwd'] = extract_code

            response = self.session.get(api_url, params=params, timeout=self.connect_timeout)

            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get('errno') == 0:
                        file_list = []
                        for file_info in data.get('list', []):
                            file_list.append({
                                'filename': file_info.get('server_filename'),
                                'size': file_info.get('size', 0),
                                'path': file_info.get('path', ''),
                                'is_dir': file_info.get('isdir', 0) == 1,
                                'md5': file_info.get('md5', ''),
                            })
                        self.logger.info(f"获取到 {len(file_list)} 个文件")
                        return file_list
                    else:
                        self.logger.warning(f"API返回错误: {data.get('errno')} - {data.get('errmsg', '未知错误')}")
                except Exception as e:
                    self.logger.error(f"JSON解析失败: {e}")

            # 方法2: 尝试使用下载API
            return self._get_file_list_download_api(share_id, extract_code)

        except Exception as e:
            self.logger.error(f"获取文件列表失败: {e}")
            return []

    def _get_file_list_download_api(self, share_id: str, extract_code: str) -> List[dict]:
        """使用下载API获取文件列表"""
        try:
            self.logger.info("尝试使用下载API获取文件列表")

            # 先提交提取码
            verify_url = "https://pan.baidu.com/share/verify"
            verify_params = {
                'shareid': share_id,
                't': int(time.time()),
                'pwd': extract_code,
                'vcode': '',
                'vstr': ''
            }

            verify_response = self.session.post(verify_url, params=verify_params)
            if verify_response.status_code == 200:
                try:
                    verify_data = verify_response.json()
                    if verify_data.get('errno') == 0:
                        self.logger.info("提取码验证成功")
                    else:
                        self.logger.warning(f"提取码验证失败: {verify_data.get('errmsg')}")
                except:
                    pass

            # 获取下载链接
            download_url = "https://pan.baidu.com/api/download"
            download_params = {
                'method': "filesmeta",
                'dirs': [],
                'sdtype': "origin",
                'showx': "0"
            }

            # 这个API需要POST请求
            download_response = self.session.post(download_url, params=download_params)
            if download_response.status_code == 200:
                try:
                    data = download_response.json()
                    if data.get('errno') == 0:
                        file_list = data.get('list', [])
                        self.logger.info(f"通过下载API获取到 {len(file_list)} 个文件")
                        return file_list
                except:
                    pass

            return []

        except Exception as e:
            self.logger.error(f"下载API调用失败: {e}")
            return []

    def download_file(self, file_url: str, local_path: Path, filename: str) -> DownloadResult:
        """下载单个文件"""
        try:
            self.logger.info(f"下载文件: {filename} -> {local_path}")

            # 创建本地目录
            local_path.parent.mkdir(parents=True, exist_ok=True)

            # 下载文件
            response = self.session.get(file_url, stream=True, timeout=self.transfer_timeout)
            if response.status_code == 200:
                total_size = 0
                with open(local_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            total_size += len(chunk)

                self.logger.info(f"文件下载成功: {local_path} ({total_size} bytes)")
                return DownloadResult(
                    success=True,
                    local_path=str(local_path),
                    remote_path=filename,
                    size=total_size
                )
            else:
                return DownloadResult(
                    success=False,
                    local_path=None,
                    remote_path=filename,
                    size=0,
                    error=f"HTTP状态码: {response.status_code}"
                )

        except Exception as e:
            self.logger.error(f"下载文件失败: {e}")
            return DownloadResult(
                success=False,
                local_path=None,
                remote_path=filename,
                size=0,
                error=str(e)
            )

    def download_folder(self, share_link: str, extract_code: str, local_path: Path) -> List[DownloadResult]:
        """下载分享文件夹"""
        try:
            self.logger.info(f"处理分享链接: {share_link}")

            # 创建本地目录
            local_path.mkdir(parents=True, exist_ok=True)

            # 获取文件列表
            files_info = self.get_file_list(share_link, extract_code)

            if not files_info:
                self.logger.warning("未获取到文件列表，无法下载")
                return []

            # 下载所有文件
            results = []
            for i, file_info in enumerate(files_info, 1):
                filename = file_info.get('filename')
                file_size = file_info.get('size', 0)
                is_dir = file_info.get('is_dir', False)

                self.logger.info(f"处理文件 {i}/{len(files_info)}: {filename} ({file_size} bytes)")

                if is_dir:
                    # 跳过目录
                    continue

                file_local_path = local_path / filename

                # 这里需要获取实际的下载链接
                # 由于API限制，暂时跳过实际下载
                result = DownloadResult(
                    success=False,
                    local_path=None,
                    remote_path=filename,
                    size=file_size,
                    error="下载链接获取需要进一步实现"
                )
                results.append(result)

            return results

        except Exception as e:
            self.logger.error(f"下载文件夹失败: {e}")
            return [DownloadResult(
                success=False,
                local_path=None,
                remote_path=share_link,
                size=0,
                error=str(e)
            )]


# 保持兼容性的别名
BaiduDownloader = ShareLinkDownloader