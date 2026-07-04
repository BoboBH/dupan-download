#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
bypy 手动认证脚本
使用方法：
1. 浏览器打开授权链接并完成授权
2. 将授权码保存到文件 auth_code.txt
3. 运行此脚本：python bypy_manual_auth.py
"""

import os
import sys

def read_auth_code():
    """从文件读取授权码"""
    auth_file = os.path.join(os.path.dirname(__file__), 'auth_code.txt')
    if not os.path.exists(auth_file):
        return None

    with open(auth_file, 'r', encoding='utf-8') as f:
        return f.read().strip()

def main():
    """主函数"""
    print("=" * 70)
    print("bypy 百度网盘 OAuth 认证")
    print("=" * 70)
    print()

    # 显示授权链接
    auth_url = "https://openapi.baidu.com/oauth/2.0/authorize?client_id=q8WE4EpCsau1oS0MplgMKNBn&response_type=code&redirect_uri=oob&scope=basic+netdisk"

    print("授权链接：")
    print(auth_url)
    print()
    print("步骤：")
    print("1. 复制上面的链接到浏览器中打开")
    print("2. 登录您的百度账号并授权")
    print("3. 复制页面显示的授权码")
    print("4. 将授权码保存到 auth_code.txt 文件中（放在此脚本同一目录）")
    print("5. 重新运行此脚本")
    print()

    # 尝试读取授权码
    auth_code = read_auth_code()

    if not auth_code:
        print("未找到授权码文件 (auth_code.txt)")
        print("请按照上述步骤完成授权并保存授权码")
        return 1

    if len(auth_code) < 16:
        print("授权码长度不足，请检查是否复制完整")
        return 1

    print(f"找到授权码：{auth_code[:8]}...")
    print("开始认证...")

    # 使用授权码进行认证
    try:
        import io
        from bypy import bypy

        # 模拟输入
        old_stdin = sys.stdin
        sys.stdin = io.StringIO(auth_code + '\n')

        try:
            # 运行 bypy quota 命令来触发认证
            sys.argv = ['bypy', 'quota']
            bypy.main()

        except SystemExit as e:
            if e.code == 0:
                print()
                print("=" * 70)
                print("✓ 认证成功！")
                print("=" * 70)
                print()
                print("现在可以使用 bypy 命令了：")
                print("  .venv/Scripts/bypy.exe list    # 列出文件")
                print("  .venv/Scripts/bypy.exe quota   # 查看配额")
                return 0
            else:
                print()
                print("认证失败")
                return 1
        finally:
            sys.stdin = old_stdin

    except Exception as e:
        print(f"认证过程中出错：{e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
