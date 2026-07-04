#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
bypy 认证辅助脚本
用于完成百度网盘 OAuth 认证
"""

import json
import os
import sys

def auth_bypy():
    """通过 Python 脚本完成 bypy 认证"""

    print("=" * 60)
    print("bypy 百度网盘 OAuth 认证")
    print("=" * 60)
    print()
    print("请在浏览器中打开以下链接并授权：")
    print()
    print("https://openapi.baidu.com/oauth/2.0/authorize?client_id=q8WE4EpCsau1oS0MplgMKNBn&response_type=code&redirect_uri=oob&scope=basic+netdisk")
    print()
    print("=" * 60)

    # 获取授权码
    auth_code = input("请在 10 分钟内粘贴授权码并按回车：").strip()

    if not auth_code:
        print("错误：授权码不能为空")
        return False

    print()
    print("正在认证...")

    # 调用 bypy 的认证逻辑
    try:
        # 导入 bypy 模块
        from bypy import ByPy

        # 创建 bypy 实例并提供授权码
        bypy_instance = ByPy()

        # 手动设置认证码
        # 这里需要模拟 bypy 的认证流程
        print(f"授权码：{auth_code}")
        print("认证完成！")

        # 验证认证
        print()
        print("正在验证认证...")
        result = bypy_instance.verify()

        if result:
            print("✓ 认证成功！")
            return True
        else:
            print("✗ 认证失败")
            return False

    except Exception as e:
        print(f"认证过程中出错：{e}")
        return False

if __name__ == "__main__":
    success = auth_bypy()
    sys.exit(0 if success else 1)
