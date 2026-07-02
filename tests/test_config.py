"""配置模块测试"""
import os
import pytest
from pathlib import Path
from dupan_download.config import Config, get_config


def test_get_config_creates_singleton():
    """测试配置单例模式"""
    config1 = get_config()
    config2 = get_config()
    assert config1 is config2


def test_config_loads_from_env():
    """测试从环境变量加载配置"""
    os.environ['BAIDU_APP_ID'] = 'test_app_id'
    os.environ['BAIDU_APP_KEY'] = 'test_app_key'
    os.environ['BAIDU_SECRET_KEY'] = 'test_secret'
    os.environ['BAIDU_ACCESS_TOKEN'] = 'test_token'

    os.environ['SFTP_HOST'] = 'test.example.com'
    os.environ['SFTP_PORT'] = '2222'
    os.environ['SFTP_USERNAME'] = 'testuser'
    os.environ['SFTP_PASSWORD'] = 'testpass'
    os.environ['SFTP_REMOTE_PATH'] = '/test/path'

    config = get_config()
    assert config.baidu_app_id == 'test_app_id'
    assert config.baidu_app_key == 'test_app_key'
    assert config.baidu_secret_key == 'test_secret'
    assert config.baidu_access_token == 'test_token'

    assert config.sftp_host == 'test.example.com'
    assert config.sftp_port == 2222
    assert config.sftp_username == 'testuser'
    assert config.sftp_password == 'testpass'
    assert config.sftp_remote_path == '/test/path'


def test_config_defaults():
    """测试默认配置值"""
    # 清除环境变量
    for key in ['MAX_RETRIES', 'CONNECT_TIMEOUT', 'TRANSFER_TIMEOUT']:
        os.environ.pop(key, None)

    config = get_config()
    assert config.max_retries == 3
    assert config.connect_timeout == 30
    assert config.transfer_timeout == 300


def test_config_custom_values():
    """测试自定义配置值"""
    os.environ['MAX_RETRIES'] = '5'
    os.environ['CONNECT_TIMEOUT'] = '60'
    os.environ['TRANSFER_TIMEOUT'] = '600'

    config = get_config()
    assert config.max_retries == 5
    assert config.connect_timeout == 60
    assert config.transfer_timeout == 600


def test_config_validation_raises_error_for_missing_required():
    """测试缺少必需配置时抛出错误"""
    # 清除所有必需的环境变量
    required_keys = [
        'BAIDU_APP_ID', 'BAIDU_APP_KEY', 'BAIDU_SECRET_KEY',
        'BAIDU_ACCESS_TOKEN', 'SFTP_HOST', 'SFTP_USERNAME',
        'SFTP_PASSWORD', 'SFTP_REMOTE_PATH'
    ]

    saved_values = {}
    for key in required_keys:
        saved_values[key] = os.environ.pop(key, None)

    try:
        with pytest.raises(ValueError, match="缺少必需的配置"):
            get_config()
    finally:
        # 恢复环境变量
        for key, value in saved_values.items():
            if value is not None:
                os.environ[key] = value
