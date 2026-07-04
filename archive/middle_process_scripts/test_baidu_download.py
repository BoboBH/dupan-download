#!/usr/bin/env python
"""
百度网盘下载功能测试脚本
"""
import sys
import os
from pathlib import Path

# 添加项目路径到sys.path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 加载环境变量
try:
    from dotenv import load_dotenv
    env_path = project_root / '.env'
    load_dotenv(dotenv_path=env_path)
    print(f"已加载环境配置: {env_path}")
except ImportError:
    print("警告: python-dotenv未安装，尝试使用系统环境变量")

from dupan_download.config import get_config
from dupan_download.downloader import BaiduDownloader

def test_config_loading():
    """测试配置加载"""
    print("=" * 60)
    print("测试 1: 配置加载")
    print("=" * 60)

    try:
        config = get_config()
        print("[OK] 配置加载成功")
        print(f"  - 百度APP_ID: {config.baidu_app_id[:10]}...")
        print(f"  - 百度APP_KEY: {config.baidu_app_key[:10]}...")
        print(f"  - 最大重试次数: {config.max_retries}")
        print(f"  - 连接超时: {config.connect_timeout}")
        return True
    except Exception as e:
        print(f"[FAIL] 配置加载失败: {e}")
        return False

def test_baidu_pcs_installation():
    """测试BaiduPCS-Py安装"""
    print("\n" + "=" * 60)
    print("测试 2: BaiduPCS-Py安装检查")
    print("=" * 60)

    try:
        from baidupcs_py import BaiduPCS
        print("[OK] BaiduPCS-Py已安装")
        print(f"  - 版本: {BaiduPCS.__version__ if hasattr(BaiduPCS, '__version__') else '未知'}")
        return True
    except ImportError as e:
        print(f"[FAIL] BaiduPCS-Py未安装: {e}")
        return False

def test_baidu_auth():
    """测试百度网盘认证"""
    print("\n" + "=" * 60)
    print("测试 3: 百度网盘认证信息")
    print("=" * 60)

    bduss = os.getenv('BAIDU_BDUSS')
    cookies = os.getenv('BAIDU_COOKIES')

    if bduss:
        print(f"[OK] BDUSS已设置 (长度: {len(bduss)})")
        print(f"  - 前10位: {bduss[:10]}...")
    else:
        print("[FAIL] BDUSS未设置")
        return False

    if cookies:
        print(f"[OK] COOKIES已设置 (长度: {len(cookies)})")
        # 检查关键字段
        if 'BDUSS' in cookies:
            print("  - COOKIES包含BDUSS字段")
        if 'STOKEN' in cookies:
            print("  - COOKIES包含STOKEN字段")
    else:
        print("[FAIL] COOKIES未设置")
        return False

    return True

def test_downloader_initialization():
    """测试下载器初始化"""
    print("\n" + "=" * 60)
    print("测试 4: 下载器初始化")
    print("=" * 60)

    try:
        downloader = BaiduDownloader()
        print("[OK] 下载器初始化成功")
        print(f"  - 最大重试次数: {downloader.max_retries}")
        print(f"  - 连接超时: {downloader.connect_timeout}")
        print(f"  - 传输超时: {downloader.transfer_timeout}")
        return True
    except Exception as e:
        print(f"[FAIL] 下载器初始化失败: {e}")
        return False

def test_baidu_pcs_init():
    """测试BaiduPCS初始化"""
    print("\n" + "=" * 60)
    print("测试 5: BaiduPCS初始化")
    print("=" * 60)

    try:
        downloader = BaiduDownloader()
        result = downloader._init_baidupcs()

        if result:
            print("[OK] BaiduPCS初始化成功")
            print(f"  - BaiduPCS对象: {type(downloader.baidupcs)}")
            return True
        else:
            print("[FAIL] BaiduPCS初始化失败")
            return False
    except Exception as e:
        print(f"[FAIL] BaiduPCS初始化异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_link_validation():
    """测试链接验证功能"""
    print("\n" + "=" * 60)
    print("测试 6: 链接验证功能")
    print("=" * 60)

    try:
        downloader = BaiduDownloader()

        # 测试有效链接格式
        test_link = "https://pan.baidu.com/s/1wE7tFQRitGj4gfdMRhrawg"
        test_code = "0409"

        print(f"测试链接: {test_link}")
        print(f"测试提取码: {test_code}")

        result = downloader.validate_link(test_link, test_code)
        if result:
            print("[OK] 链接验证通过")
        else:
            print("[FAIL] 链接验证失败")

        return result
    except Exception as e:
        print(f"[FAIL] 链接验证异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """运行所有测试"""
    print("\n")
    print("=" * 60)
    print(" " + " " * 58 + " ")
    print(" " + " " * 15 + "百度网盘下载功能测试" + " " * 19 + " ")
    print(" " + " " * 58 + " ")
    print("=" * 60)

    results = []

    # 运行所有测试
    results.append(("配置加载", test_config_loading()))
    results.append(("BaiduPCS-Py安装", test_baidu_pcs_installation()))
    results.append(("百度网盘认证", test_baidu_auth()))
    results.append(("下载器初始化", test_downloader_initialization()))
    results.append(("BaiduPCS初始化", test_baidu_pcs_init()))
    results.append(("链接验证", test_link_validation()))

    # 打印总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)

    for test_name, result in results:
        status = "[OK] 通过" if result else "[FAIL] 失败"
        print(f"{status} - {test_name}")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    print("\n" + "=" * 60)
    print(f"总计: {passed}/{total} 测试通过")
    print("=" * 60)

    if passed == total:
        print("\n[SUCCESS] 所有测试通过！可以进行真实下载测试。")
        return 0
    else:
        print(f"\n[WARNING] 有 {total - passed} 个测试失败，请检查配置。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
