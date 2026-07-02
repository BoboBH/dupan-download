"""上传模块测试"""
import pytest
from unittest.mock import MagicMock, patch
from dupan_download.uploader import SFTPUploader, UploadResult


def test_upload_result_success():
    """测试成功上传结果"""
    result = UploadResult(
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


def test_upload_result_failure():
    """测试失败上传结果"""
    result = UploadResult(
        success=False,
        local_path="/local/path.pdf",
        remote_path="/remote/path.pdf",
        size=0,
        error="Connection failed"
    )
    assert result.success is False
    assert result.error == "Connection failed"


@pytest.fixture
def mock_config():
    """模拟配置"""
    config = MagicMock()
    config.sftp_host = "test.example.com"
    config.sftp_port = 22
    config.sftp_username = "testuser"
    config.sftp_password = "testpass"
    config.sftp_remote_path = "/remote/path"
    config.max_retries = 3
    config.connect_timeout = 30
    config.transfer_timeout = 300
    return config


def test_uploader_initialization(mock_config):
    """测试上传器初始化"""
    with patch('dupan_download.uploader.get_config', return_value=mock_config):
        uploader = SFTPUploader()
        assert uploader.config == mock_config
        assert uploader.max_retries == 3
