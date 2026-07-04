"""配置管理模块"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """配置类，管理所有配置项"""

    _instance: Optional['Config'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        # 加载.env文件
        env_path = Path('.env')
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)

    @property
    def sftp_host(self) -> str:
        """SFTP主机地址"""
        value = os.getenv('SFTP_HOST')
        if not value:
            raise ValueError("缺少必需的配置: SFTP_HOST")
        return value

    @property
    def sftp_port(self) -> int:
        """SFTP端口"""
        value = os.getenv('SFTP_PORT', '22')
        try:
            return int(value)
        except ValueError:
            raise ValueError(f"SFTP_PORT必须是整数: {value}")

    @property
    def sftp_username(self) -> str:
        """SFTP用户名"""
        value = os.getenv('SFTP_USERNAME')
        if not value:
            raise ValueError("缺少必需的配置: SFTP_USERNAME")
        return value

    @property
    def sftp_password(self) -> str:
        """SFTP密码"""
        value = os.getenv('SFTP_PASSWORD')
        if not value:
            raise ValueError("缺少必需的配置: SFTP_PASSWORD")
        return value

    @property
    def sftp_remote_path(self) -> str:
        """SFTP远程路径"""
        value = os.getenv('SFTP_REMOTE_PATH')
        if not value:
            raise ValueError("缺少必需的配置: SFTP_REMOTE_PATH")
        return value

    @property
    def max_retries(self) -> int:
        """最大重试次数"""
        value = os.getenv('MAX_RETRIES', '3')
        try:
            return int(value)
        except ValueError:
            return 3

    @property
    def connect_timeout(self) -> int:
        """连接超时时间(秒)"""
        value = os.getenv('CONNECT_TIMEOUT', '30')
        try:
            return int(value)
        except ValueError:
            return 30

    @property
    def transfer_timeout(self) -> int:
        """传输超时时间(秒)"""
        value = os.getenv('TRANSFER_TIMEOUT', '300')
        try:
            return int(value)
        except ValueError:
            return 300


# 全局配置实例
_config: Optional[Config] = None


def get_config() -> Config:
    """获取配置单例"""
    global _config
    if _config is None:
        _config = Config()
    return _config
