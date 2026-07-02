"""CLI模块测试"""
import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock
from dupan_download.cli import main


@pytest.fixture
def runner():
    """CLI测试运行器"""
    return CliRunner()


def test_cli_help(runner):
    """测试帮助信息"""
    result = runner.invoke(main, ['--help'])
    assert result.exit_code == 0
    assert '百度网盘自动下载SFTP上传工具' in result.output


def test_cli_missing_arguments(runner):
    """测试缺少必需参数"""
    result = runner.invoke(main, [])
    assert result.exit_code != 0
    assert 'Missing argument' in result.output


@patch('dupan_download.cli.BaiduDownloader')
@patch('dupan_download.cli.SFTPUploader')
@patch('dupan_download.cli.create_temp_dir')
@patch('dupan_download.cli.get_config')
def test_cli_basic_flow(mock_get_config, mock_create_temp, mock_uploader, mock_downloader, runner):
    """测试基本CLI流程"""
    # 模拟配置
    mock_config = MagicMock()
    mock_get_config.return_value = mock_config

    # 模拟临时目录
    mock_temp = MagicMock()
    mock_create_temp.return_value = mock_temp

    # 模拟下载器
    mock_dl_instance = MagicMock()
    mock_dl_instance.validate_link.return_value = True
    mock_dl_instance.download_folder.return_value = []
    mock_downloader.return_value = mock_dl_instance

    # 模拟上传器
    mock_ul_instance = MagicMock()
    mock_ul_instance.upload_folder.return_value = []
    mock_uploader.return_value = mock_ul_instance

    result = runner.invoke(main, [
        'https://pan.baidu.com/s/test',
        '1234'
    ])

    # 验证调用链
    mock_dl_instance.validate_link.assert_called_once()
    mock_dl_instance.download_folder.assert_called_once()
    mock_ul_instance.upload_folder.assert_called_once()
