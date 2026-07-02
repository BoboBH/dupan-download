"""下载模块测试"""
import pytest
from unittest.mock import MagicMock, patch
from dupan_download.downloader import BaiduDownloader, DownloadResult


def test_download_result_success():
    """测试成功下载结果"""
    result = DownloadResult(
        success=True,
        local_path="/local/path.pdf",
        remote_path="/remote/path.pdf",
        size=1024,
        error=None
    )
    assert result.success is True
    assert result.local_path == "/local/path.pdf"
    assert result.size == 1024
    assert result.error is None


def test_download_result_failure():
    """测试失败下载结果"""
    result = DownloadResult(
        success=False,
        local_path=None,
        remote_path="/remote/path.pdf",
        size=0,
        error="Network error"
    )
    assert result.success is False
    assert result.local_path is None
    assert result.error == "Network error"


@pytest.fixture
def mock_config():
    """模拟配置"""
    config = MagicMock()
    config.baidu_app_id = "test_app_id"
    config.baidu_app_key = "test_key"
    config.baidu_secret_key = "test_secret"
    config.baidu_access_token = "test_token"
    config.max_retries = 3
    config.connect_timeout = 30
    config.transfer_timeout = 300
    return config


def test_downloader_initialization(mock_config):
    """测试下载器初始化"""
    with patch('dupan_download.downloader.get_config', return_value=mock_config):
        downloader = BaiduDownloader()
        assert downloader.config == mock_config
        assert downloader.max_retries == 3
