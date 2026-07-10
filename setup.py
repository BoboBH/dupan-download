from setuptools import setup, find_packages

setup(
    name="dupan-download",
    version="2.1.5",
    description="百度网盘自动下载SFTP上传工具",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "python-dotenv>=0.19.0",
        "paramiko>=2.11.0",
        "requests>=2.27.0",
        "tqdm>=4.62.0",
    ],
    entry_points={
        "console_scripts": [
            "dupan-download=dupan_download.cli:main",
            "pan-download=dupan_download.integrated_cli:main",
        ],
    },
    python_requires=">=3.8",
)
