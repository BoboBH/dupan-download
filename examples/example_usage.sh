#!/bin/bash
# 示例使用脚本

echo "=== 百度网盘下载SFTP上传工具示例 ==="
echo ""

# 示例1: 基本使用
echo "1. 基本使用:"
echo "   dupan-download https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg 0409"
echo ""

# 示例2: 保留临时文件
echo "2. 保留临时文件用于调试:"
echo "   dupan-download https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg 0409 --keep-temp"
echo ""

# 示例3: 指定临时目录
echo "3. 指定临时目录:"
echo "   dupan-download https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg 0409 --temp-dir \"D:/temp\""
echo ""

# 示例4: 详细输出模式
echo "4. 详细输出模式:"
echo "   dupan-download https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg 0409 --verbose"
echo ""

echo "=== 确保已正确配置 .env 文件 ==="
