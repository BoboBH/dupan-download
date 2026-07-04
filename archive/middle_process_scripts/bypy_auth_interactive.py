#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
bypy 认证辅助脚本
用于完成百度网盘 OAuth 认证
"""

import sys
import os

def main():
    """主函数"""
    print("=" * 70)
    print("bypy 百度网盘 OAuth 认证助手")
    print("=" * 70)
    print()
    print("步骤说明：")
    print("1. 在浏览器中打开下面的授权链接")
    print("2. 登录您的百度账号")
    print("3. 点击"授权"按钮")
    print("4. 复制页面显示的授权码")
    print("5. 将授权码粘贴到下面的输入框中")
    print()
    print("=" * 70)
    print("授权链接：")
    print("https://openapi.baidu.com/oauth/2.0/authorize?client_id=q8WE4EpCsau1oS0MplgMKNBn&response_type=code&redirect_uri=oob&scope=basic+netdisk")
    print()
    print("=" * 70)
    print()
    print("请复制上面的链接到浏览器中打开，完成授权后...")
    print()

    # 获取用户输入
    auth_code = input("请在 10 分钟内粘贴授权码并按回车：").strip()

    if not auth_code:
        print("错误：授权码不能为空")
        return 1

    if len(auth_code) < 16:
        print("错误：授权码长度不足，请检查是否复制完整")
        return 1

    print()
    print(f"授权码：{auth_code}")
    print("正在认证中，请耐心等待...")

    # 导入 bypy 模块
    try:
        # 我们需要直接调用 bypy 的内部认证函数
        # 首先设置认证码为环境变量或直接修改输入

        # 方案：创建一个临时的输入模拟
        import io
        from contextlib import redirect_stdout, redirect_stderr

        # 创建一个模拟的输入流
        old_stdin = sys.stdin
        sys.stdin = io.StringIO(auth_code + '\n')

        try:
            # 导入并运行 bypy
            from bypy import bypy

            # 运行 bypy 的主函数
            sys.argv = ['bypy', 'quota']
            bypy.main()

        except SystemExit as e:
            # bypy 会调用 sys.exit，这是正常的
            if e.code == 0:
                print()
                print("=" * 70)
                print("✓ 认证成功！")
                print("=" * 70)
                return 0
            else:
                print()
                print("=" * 70)
                print("✗ 认证失败")
                print("=" * 70)
                return 1
        finally:
            sys.stdin = old_stdin

    except Exception as e:
        print()
        print(f"认证过程中出错：{e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
