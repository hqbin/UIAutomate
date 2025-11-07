#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
运行数据埋点测试脚本

使用方法:
    python run_analytics_tests.py -m analytics  # 运行所有埋点测试
    python run_analytics_tests.py tests/cases/analytics/  # 运行指定目录的测试
    python run_analytics_tests.py tests/cases/analytics/test_remote_key_analytics.py  # 运行指定文件的测试
"""

import os
import sys
import argparse
import subprocess
import shutil
from datetime import datetime


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='运行数据埋点测试')
    parser.add_argument('test_path', nargs='?', default='tests/cases/analytics/',
                        help='测试文件或目录路径，默认运行所有埋点测试')
    parser.add_argument('-m', '--mark', default='analytics',
                        help='测试标记，默认使用analytics标记')
    parser.add_argument('--html', action='store_true',
                        help='生成HTML报告')
    parser.add_argument('--allure', action='store_true',
                        help='生成Allure报告')
    parser.add_argument('--clean', action='store_true',
                        help='清理之前的报告')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='显示详细输出')
    return parser.parse_args()


def ensure_directory(directory):
    """确保目录存在"""
    os.makedirs(directory, exist_ok=True)


def clean_reports():
    """清理之前的报告"""
    reports_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tests', 'reports')
    allure_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'allure-results')
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    
    for directory in [reports_dir, allure_dir, logs_dir]:
        if os.path.exists(directory):
            print(f"清理目录: {directory}")
            try:
                shutil.rmtree(directory)
                os.makedirs(directory, exist_ok=True)
            except Exception as e:
                print(f"清理目录 {directory} 时出错: {e}")


def run_tests(args):
    """运行测试"""
    # 获取项目根目录
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建pytest命令
    pytest_cmd = ['pytest']
    
    # 处理测试路径，支持使用::语法指定单个测试函数
    # 检查是否包含::语法
    if '::' in args.test_path:
        # 对于包含::的路径，直接添加到命令中，不进行路径检查
        pytest_cmd.append(args.test_path)
    else:
        # 对于普通路径，检查是否存在
        if os.path.exists(os.path.join(root_dir, args.test_path)):
            pytest_cmd.append(args.test_path)
        else:
            pytest_cmd.extend(['-m', args.mark])
    
    # 添加详细输出
    if args.verbose:
        pytest_cmd.append('-v')
    
    # 添加报告参数
    reports_dir = os.path.join(root_dir, 'tests', 'reports')
    ensure_directory(reports_dir)
    
    # 生成时间戳
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # 添加HTML报告
    if args.html:
        html_report = os.path.join(reports_dir, f'analytics_report_{timestamp}.html')
        pytest_cmd.extend(['--html', html_report, '--self-contained-html'])
    
    # 添加Allure报告
    if args.allure:
        allure_dir = os.path.join(root_dir, 'allure-results')
        ensure_directory(allure_dir)
        pytest_cmd.extend(['--alluredir', allure_dir])
    
    # 确保日志目录存在
    logs_dir = os.path.join(root_dir, 'logs')
    ensure_directory(logs_dir)
    
    print(f"执行命令: {' '.join(pytest_cmd)}")
    print(f"工作目录: {root_dir}")
    print("开始运行数据埋点测试...")
    
    try:
        # 运行测试
        result = subprocess.run(
            pytest_cmd,
            cwd=root_dir,
            capture_output=False,
            text=True
        )
        
        # 输出测试结果摘要
        print("\n" + "="*60)
        if result.returncode == 0:
            print("✅ 数据埋点测试全部通过!")
        else:
            print("❌ 数据埋点测试失败!")
        print("="*60)
        
        # 如果生成了Allure报告，提示如何查看
        if args.allure:
            print("\n生成Allure报告成功!")
            print("查看报告命令: allure serve allure-results")
        
        # 如果生成了HTML报告，显示报告路径
        if args.html:
            print(f"\nHTML报告已生成: {os.path.abspath(html_report)}")
        
        return result.returncode
    
    except Exception as e:
        print(f"运行测试时出错: {e}")
        return 1


def main():
    """主函数"""
    args = parse_args()
    
    # 清理报告
    if args.clean:
        clean_reports()
    
    # 运行测试
    return run_tests(args)


if __name__ == '__main__':
    sys.exit(main())