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

    优化临时目录名称长度，为长文件名预留更多路径空间。
    使用更短的目录名前缀和更短的PID后缀。

    Args:
        base_dir: 基础目录，如果为None则使用系统默认临时目录

    Returns:
        临时目录路径
    """
    if base_dir:
        base = Path(base_dir)
        base.mkdir(parents=True, exist_ok=True)
        # 使用极短的目录名，最大程度为长文件名预留空间
        # 仅使用PID的后4位数字来缩短目录名
        pid_suffix = str(os.getpid())[-4:]  # 取PID最后4位
        temp_dir = base / f"dl_{pid_suffix}"
    else:
        # 使用更短的前缀和更短的PID后缀
        pid_suffix = str(os.getpid())[-4:]  # 取PID最后4位
        temp_dir = Path(tempfile.mkdtemp(prefix=f"dl_{pid_suffix}_"))

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


def sanitize_filename(filename: str, max_length: int = 200) -> str:
    """
    清理和截断文件名以避免系统路径长度限制

    Windows系统有MAX_PATH限制（260字符），当完整路径超过此限制时，
    文件操作会失败。此函数智能截断文件名以确保路径在安全范围内。

    Args:
        filename: 原始文件名
        max_length: 文件名最大长度（默认200字符，为路径开销预留空间）

    Returns:
        清理后的文件名

    Examples:
        >>> sanitize_filename("very_long_filename..." + ".pdf")
        'very_long_filename...[truncated].pdf'
    """
    if not filename:
        return "unknown_file"

    # 移除Windows文件名中的非法字符
    # Windows不允许的字符: < > : " / \ | ? *
    illegal_chars = r'[<>:"/\\|?*]'
    cleaned = re.sub(illegal_chars, '_', filename)

    # 如果文件名长度在限制内，直接返回
    if len(cleaned) <= max_length:
        return cleaned

    # 需要截断文件名
    # 保留文件扩展名
    name_parts = cleaned.rsplit('.', 1)
    if len(name_parts) == 2 and len(name_parts[1]) <= 10:  # 合理的扩展名长度
        base_name, extension = name_parts
        # 确保扩展名不为空
        if not extension:
            extension = "unknown"
    else:
        # 没有明显的扩展名或扩展名太长
        base_name = cleaned
        extension = ""

    # 计算可用长度（包含扩展名和分隔符）
    if extension:
        available_length = max_length - len(extension) - 1  # -1 for dot
        truncated_base = base_name[:available_length]
        return f"{truncated_base}.{extension}"
    else:
        # 没有扩展名，直接截断
        return base_name[:max_length]


def ensure_path_safe(file_path: Path, max_total_length: int = 250) -> Path:
    """
    确保文件路径在安全长度范围内

    Args:
        file_path: 原始文件路径
        max_total_length: 最大总路径长度（默认250，留出安全余量）

    Returns:
        调整后的安全路径

    Examples:
        >>> ensure_path_safe(Path("/very/long/path/very_long_filename.pdf"))
        Path("/very/long/path/truncated_filename.pdf")
    """
    path_str = str(file_path)

    if len(path_str) <= max_total_length:
        return file_path

    # 路径太长，需要缩短文件名
    parent = file_path.parent
    filename = file_path.name

    # 计算路径长度（不含文件名）
    parent_str = str(parent)
    path_length = len(parent_str) + 1  # +1 for path separator

    # 计算文件名可用长度
    max_filename_length = max_total_length - path_length

    if max_filename_length < 10:  # 文件名至少10个字符
        # 如果路径本身太长，返回原始路径（让系统报错）
        return file_path

    # 清理文件名
    safe_filename = sanitize_filename(filename, max_filename_length)
    return parent / safe_filename
