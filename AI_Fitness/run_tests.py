#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import unittest
import os

# 定义测试文件所在的目录
# 相对于项目根目录 (run_tests.py 所在的目录)
TEST_DIR = 'tests' # unittest 会递归查找这个目录下的 test*.py

# 定义测试文件的匹配模式
# unittest 默认就是 'test*.py', 这里可以明确指定
TEST_PATTERN = 'test*.py'

def run_all_tests():
    """自动发现并运行所有测试"""
    print(f"正在从 '{TEST_DIR}' 目录中发现测试...")

    # 创建一个测试加载器
    loader = unittest.TestLoader()

    # 发现指定目录下的所有测试用例
    # discover() 方法会自动查找符合 TEST_PATTERN 模式的文件
    # 并加载其中的 unittest.TestCase 子类
    try:
        suite = loader.discover(start_dir=TEST_DIR, pattern=TEST_PATTERN)
    except ImportError as e:
        print(f"\n错误：无法导入测试模块。请确保您是从项目根目录运行此脚本，")
        print(f"并且 Python 环境可以找到 'app' 包及其子模块。")
        print(f"详细错误: {e}")
        return

    if suite.countTestCases() == 0:
        print(f"在 '{TEST_DIR}' 目录中没有找到符合 '{TEST_PATTERN}' 模式的测试。")
        return

    print(f"发现了 {suite.countTestCases()} 个测试用例。准备运行...")
    print("-"*70)

    # 创建一个测试运行器
    # verbosity=2 会输出更详细的测试结果
    runner = unittest.TextTestRunner(verbosity=2)

    # 运行测试套件
    result = runner.run(suite)

    print("-"*70)
    print("测试运行完毕。")

    # 可以根据 result 对象判断测试是否全部成功
    if result.wasSuccessful():
        print("所有测试通过！")
    else:
        print("部分测试失败。")

if __name__ == '__main__':
    # 确保脚本从项目根目录运行，以便正确导入 app 模块
    project_root = os.path.dirname(os.path.abspath(__file__))
    # 如果 tests 目录不在项目根目录下，需要调整 sys.path 或 TEST_DIR
    # import sys
    # sys.path.insert(0, project_root)

    run_all_tests() 