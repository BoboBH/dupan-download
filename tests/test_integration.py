"""集成测试"""
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from dupan_download.cli import main


@pytest.fixture
def mock_env():
    """设置测试环境变量"""
    env_vars = {
        'BAIDU_APP_ID': 'test_app_id',
        'BAIDU_APP_KEY': 'test_app_key',
        'BAIDU_SECRET_KEY': 'test_secret',
        'BAIDU_ACCESS_TOKEN': 'test_token',
        'SFTP_HOST': 'test.example.com',
        'SFTP_PORT': '22',
        'SFTP_USERNAME': 'testuser',
        'SFTP_PASSWORD': 'testpass',
        'SFTP_REMOTE_PATH': '/test/path',
    }

    # 保存原始环境变量
    original_vars = {}
    for key in env_vars:
        original_vars[key] = os.environ.get(key)
        os.environ[key] = env_vars[key]

    yield env_vars

    # 恢复原始环境变量
    for key, value in original_vars.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


def test_end_to_end_success_flow(mock_env):
    """测试端到端成功流程"""
    runner = CliRunner()

    with patch('dupan_download.downloader.BaiduDownloader') as mock_dl_class, \
         patch('dupan_download.uploader.SFTPUploader') as mock_ul_class:

        # 模拟下载器
        mock_dl = MagicMock()
        mock_dl.validate_link.return_value = True
        mock_dl.download_folder.return_value = []
        mock_dl_class.return_value = mock_dl

        # 模拟上传器
        mock_ul = MagicMock()
        mock_ul.connect.return_value = True
        mock_ul.upload_folder.return_value = []
        mock_ul_class.return_value = mock_ul

        result = runner.invoke(main, [
            'https://pan.baidu.com/s/test123',
            'abcd'
        ])

        # 验证执行流程
        assert result.exit_code == 0
        mock_dl.validate_link.assert_called_once()
        mock_dl.download_folder.assert_called_once()
        mock_ul.connect.assert_called_once()
        mock_ul.upload_folder.assert_called_once()
        mock_ul.disconnect.assert_called_once()


def test_end_to_end_with_keep_temp(mock_env):
    """测试保留临时文件"""
    runner = CliRunner()

    with patch('dupan_download.downloader.BaiduDownloader') as mock_dl_class, \
         patch('dupan_download.uploader.SFTPUploader') as mock_ul_class, \
         patch('dupan_download.cli.cleanup_temp_dir') as mock_cleanup:

        mock_dl = MagicMock()
        mock_dl.validate_link.return_value = True
        mock_dl.download_folder.return_value = []
        mock_dl_class.return_value = mock_dl

        mock_ul = MagicMock()
        mock_ul.connect.return_value = True
        mock_ul.upload_folder.return_value = []
        mock_ul_class.return_value = mock_ul

        result = runner.invoke(main, [
            'https://pan.baidu.com/s/test123',
            'abcd',
            '--keep-temp'
        ])

        assert result.exit_code == 0
        # 验证临时文件未被清理
        mock_cleanup.assert_not_called()


def test_validation_failure(mock_env):
    """测试链接验证失败"""
    runner = CliRunner()

    with patch('dupan_download.downloader.BaiduDownloader') as mock_dl_class:
        mock_dl = MagicMock()
        mock_dl.validate_link.return_value = False
        mock_dl_class.return_value = mock_dl

        result = runner.invoke(main, [
            'https://pan.baidu.com/s/test123',
            'wrong_code'
        ])

        assert result.exit_code == 1
        assert '链接验证失败' in result.output


def test_sftp_connection_failure(mock_env):
    """测试SFTP连接失败"""
    runner = CliRunner()

    with patch('dupan_download.downloader.BaiduDownloader') as mock_dl_class, \
         patch('dupan_download.uploader.SFTPUploader') as mock_ul_class:

        mock_dl = MagicMock()
        mock_dl.validate_link.return_value = True
        mock_dl.download_folder.return_value = []
        mock_dl_class.return_value = mock_dl

        mock_ul = MagicMock()
        mock_ul.connect.return_value = False
        mock_ul_class.return_value = mock_ul

        result = runner.invoke(main, [
            'https://pan.baidu.com/s/test123',
            'abcd'
        ])

        assert result.exit_code == 1
        assert 'SFTP连接失败' in result.output
