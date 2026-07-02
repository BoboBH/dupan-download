# 百度网盘自动下载SFTP上传工具

自动从百度网盘下载文件夹并上传到SFTP服务器的命令行工具。

## 功能特性

- 支持百度网盘文件夹下载
- 保持完整目录结构
- 自动上传到SFTP服务器
- 灵活的错误处理和重试机制
- 详细的执行报告

## 安装

```bash
pip install -r requirements.txt
python setup.py install
```

## 配置

复制 `.env.example` 为 `.env` 并填入实际配置：

```bash
cp .env.example .env
```

## 使用

```bash
dupan-download <网盘链接> <提取码>
```

## 选项

- `--keep-temp`: 保留临时文件
- `--temp-dir PATH`: 指定临时目录
- `--verbose`: 详细输出模式

## 许可证

MIT License
