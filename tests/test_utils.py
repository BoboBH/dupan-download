"""工具模块测试"""
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from dupan_download.utils import (
    create_temp_dir, cleanup_temp_dir, setup_logger,
    get_progress_bar, mask_sensitive_info
)


def test_create_temp_dir_default():
    """测试创建默认临时目录"""
    temp_dir = create_temp_dir()
    assert temp_dir.exists()
    assert temp_dir.is_dir()
    assert 'dupan_download' in temp_dir.name.lower()

    # 清理
    shutil.rmtree(temp_dir)


def test_create_temp_dir_custom():
    """测试创建自定义临时目录"""
    custom_base = tempfile.gettempdir()
    temp_dir = create_temp_dir(base_dir=custom_base)
    assert temp_dir.exists()
    assert temp_dir.parent == Path(custom_base)

    # 清理
    shutil.rmtree(temp_dir)


def test_cleanup_temp_dir():
    """测试清理临时目录"""
    temp_dir = create_temp_dir()
    # 创建一些测试文件
    test_file = temp_dir / "test.txt"
    test_file.write_text("test")

    assert temp_dir.exists()
    cleanup_temp_dir(temp_dir)
    assert not temp_dir.exists()


def test_cleanup_temp_dir_with_keep_flag():
    """测试保留临时目录"""
    temp_dir = create_temp_dir()
    test_file = temp_dir / "test.txt"
    test_file.write_text("test")

    cleanup_temp_dir(temp_dir, keep=True)
    assert temp_dir.exists()

    # 清理
    shutil.rmtree(temp_dir)


def test_mask_sensitive_info():
    """测试敏感信息遮蔽"""
    url = "https://pan.baidu.com/s/1abc123?pwd=secret123"
    masked = mask_sensitive_info(url)
    assert "secret123" not in masked
    assert "***" in masked

    # 测试不敏感信息
    safe_url = "https://example.com/path"
    result = mask_sensitive_info(safe_url)
    assert result == safe_url


@patch('dupan_download.utils.logging')
def test_setup_logger(mock_logging):
    """测试日志设置"""
    mock_logger = MagicMock()
    mock_logging.getLogger.return_value = mock_logger

    logger = setup_logger('test_logger', verbose=True)

    mock_logging.getLogger.assert_called_with('test_logger')
    mock_logger.setLevel.assert_called()


@patch('dupan_download.utils.tqdm')
def test_get_progress_bar(mock_tqdm):
    """测试进度条创建"""
    mock_progress = MagicMock()
    mock_tqdm.return_value = mock_progress

    progress = get_progress_bar(total=100, desc="Test")

    mock_tqdm.assert_called_once()
    assert progress == mock_progress
