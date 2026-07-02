"""工具函数模块"""
import os
import logging
import tempfile
import shutil
import re
from pathlib import Path
from typing import Optional
from tqdm import tqdm


def create_temp_dir(base_dir: Optional[str] = None) -> Path:
    """
    创建临时目录

    Args:
        base_dir: 基础目录，如果为None则使用系统默认临时目录

    Returns:
        临时目录路径
    """
    if base_dir:
        base = Path(base_dir)
        base.mkdir(parents=True, exist_ok=True)
        temp_dir = base / f"dupan_download_{os.getpid()}"
    else:
        temp_dir = Path(tempfile.mkdtemp(prefix="dupan_download_"))

    temp_dir.mkdir(parents=True, exist_ok=True)
    return temp_dir


def cleanup_temp_dir(temp_dir: Path, keep: bool = False) -> None:
    """
    清理临时目录

    Args:
        temp_dir: 临时目录路径
        keep: 是否保留目录
    """
    if keep:
        return

    if temp_dir.exists():
        shutil.rmtree(temp_dir)


def setup_logger(name: str, verbose: bool = False) -> logging.Logger:
    """
    设置日志记录器

    Args:
        name: 记录器名称
        verbose: 是否启用详细日志

    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(name)

    if verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    # 避免重复添加handler
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def get_progress_bar(total: int, desc: str = "Processing") -> tqdm:
    """
    获取进度条对象

    Args:
        total: 总数量
        desc: 描述文本

    Returns:
        tqdm进度条对象
    """
    return tqdm(total=total, desc=desc, unit='item')


def mask_sensitive_info(text: str) -> str:
    """
    遮蔽敏感信息

    Args:
        text: 输入文本

    Returns:
        遮蔽后的文本
    """
    # 遮蔽URL中的密码参数
    text = re.sub(r'[&?]pwd=([^&\s]+)', lambda m: f'?pwd={"*" * len(m.group(1))}', text)

    # 遮蔽access_token
    text = re.sub(r'token=([^&\s]+)', lambda m: f'token={"*" * len(m.group(1))}', text, flags=re.IGNORECASE)

    return text
