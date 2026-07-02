"""配置模块测试"""
import os
import pytest
from pathlib import Path
from dupan_download.config import Config, get_config, _config


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
    # 使用子进程测试，避免单例缓存问题
    import subprocess
    import sys

    # 创建一个临时脚本来测试配置验证
    test_script = """
import os
from dupan_download.config import Config

# 确保所有必需的环境变量都不存在
for key in ['BAIDU_APP_ID', 'BAIDU_APP_KEY', 'BAIDU_SECRET_KEY',
            'BAIDU_ACCESS_TOKEN', 'SFTP_HOST', 'SFTP_USERNAME',
            'SFTP_PASSWORD', 'SFTP_REMOTE_PATH']:
    os.environ.pop(key, None)

try:
    config = Config()
    # 访问属性来触发验证
    _ = config.baidu_app_id  # 这应该抛出ValueError
    print("ERROR: Should have raised ValueError")
    exit(1)
except ValueError as e:
    if "缺少必需的配置" in str(e):
        print("SUCCESS: Correctly raised ValueError")
        exit(0)
    else:
        print(f"ERROR: Wrong error message: {e}")
        exit(1)
"""

    result = subprocess.run(
        [sys.executable, '-c', test_script],
        capture_output=True,
        text=True,
        cwd=os.getcwd()
    )

    assert result.returncode == 0, f"Config validation test failed: {result.stdout} {result.stderr}"
    assert "SUCCESS" in result.stdout
