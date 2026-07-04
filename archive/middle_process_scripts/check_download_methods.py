#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查下载相关方法的详细信息"""
import sys
from pathlib import Path

# 设置控制台输出编码为UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from baidupcs_py import BaiduPCS
import inspect

methods_to_check = ['download_link', 'file_stream', 'list', 'list_shared', 'share']

print('下载相关方法详细信息:')
print('=' * 60)

for method_name in methods_to_check:
    if hasattr(BaiduPCS, method_name):
        method = getattr(BaiduPCS, method_name)
        sig = inspect.signature(method)
        print(f'\n{method_name}{sig}')

        # 获取文档
        doc = method.__doc__
        if doc:
            # 清理并显示文档
            doc_lines = doc.strip().split('\n')
            print(f'  文档:')
            for line in doc_lines[:5]:  # 显示前5行
                print(f'    {line.strip()}')
            if len(doc_lines) > 5:
                print(f'    ... (共 {len(doc_lines)} 行)')
        else:
            print('  文档: 无文档')

print('\n' + '=' * 60)
