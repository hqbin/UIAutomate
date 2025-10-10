#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
STB远程UI自动化测试运行脚本
用于简化测试执行和报告生成流程

allure serve allure-results 可以重新打开报告
"""
import os
import sys
import subprocess
import time
import argparse

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 获取当前目录
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# 测试结果目录
ALLURE_RESULTS_DIR = os.path.join(CURRENT_DIR, "allure-results")

# 解析命令行参数
def parse_arguments():
    parser = argparse.ArgumentParser(description='STBUI自动化测试运行脚本')
    parser.add_argument('-m', '--marker', type=str, help='指定要运行的测试标记（如stb_power, stb_channel等）')
    parser.add_argument('-k', '--keyword', type=str, help='通过关键字表达式过滤测试用例')
    parser.add_argument('-r', '--report', action='store_true', help='生成并打开Allure报告')
    parser.add_argument('-c', '--clean', action='store_true', help='清理旧的测试结果')
    parser.add_argument('-v', '--verbose', action='store_true', help='显示详细的测试输出')
    parser.add_argument('-n', '--reruns', type=int, default=3, help='失败测试重跑次数，默认为0（不重跑）')
    parser.add_argument('-t', '--rerun-delay', type=int, default=3, help='重跑间隔时间（秒），默认为0')
    return parser.parse_args()

# 清理旧的测试结果
def clean_old_results():
    if os.path.exists(ALLURE_RESULTS_DIR):
        print("清理旧的测试结果...")
        if sys.platform.startswith('win'):
            subprocess.run(f"rmdir /s /q {ALLURE_RESULTS_DIR}", shell=True)
        else:
            subprocess.run(f"rm -rf {ALLURE_RESULTS_DIR}", shell=True)
    
    # 确保结果目录存在
    os.makedirs(ALLURE_RESULTS_DIR, exist_ok=True)

# 运行测试
def run_tests(marker=None, keyword=None, verbose=False, reruns=0, rerun_delay=0):
    print(f"开始执行测试...")
    
    # 构建pytest命令
    pytest_cmd = ["pytest"]
    
    # 添加详细输出选项
    if verbose:
        pytest_cmd.append("-v")
    
    # 添加测试标记
    if marker:
        pytest_cmd.extend(["-m", marker])
    
    # 添加关键字过滤
    if keyword:
        pytest_cmd.extend(["-k", keyword])
    
    # 添加Allure报告选项
    pytest_cmd.extend(["--alluredir", ALLURE_RESULTS_DIR])
    
    # 添加失败重跑选项
    if reruns > 0:
        print(f"开启失败重跑功能，重跑次数: {reruns}")
        if rerun_delay > 0:
            print(f"重跑间隔时间: {rerun_delay}秒")
        pytest_cmd.extend(["--reruns", str(reruns)])
        if rerun_delay > 0:
            pytest_cmd.extend(["--reruns-delay", str(rerun_delay)])
    
    # 添加测试用例目录
    pytest_cmd.append("tests/cases/")
    
    try:
        # 执行测试
        result = subprocess.run(pytest_cmd)
        return result.returncode == 0
    except Exception as e:
        print(f"测试执行失败: {e}")
        return False

# 生成并打开Allure报告
def generate_and_open_report():
    print("生成Allure报告...")
    
    try:
        # 根据操作系统类型选择不同的命令执行方式
        if sys.platform.startswith('win'):
            # 在Windows上，使用shell=True来运行Allure命令
            print("检测到Windows系统，使用shell执行Allure命令...")
            # 检查Allure是否安装
            subprocess.run("allure --version", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # 打开Allure报告
            print("正在打开Allure报告，请稍候...")
            subprocess.run(f"allure serve {ALLURE_RESULTS_DIR}", shell=True)
        else:
            # 在非Windows系统上，使用标准方式
            # 检查Allure是否安装
            subprocess.run(["allure", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # 打开Allure报告
            print("正在打开Allure报告，请稍候...")
            subprocess.run(["allure", "serve", ALLURE_RESULTS_DIR])
        
        return True
    except FileNotFoundError:
        print("错误: 未找到Allure命令行工具，请先安装Allure")
        print("安装指南请参考 tests/pytest_allure_guide.md 文件")
        print("提示: 在Windows上，请确保Allure的bin目录已添加到系统PATH环境变量中，")
        print("      并尝试重新启动命令提示符或IDE后再运行脚本。")
        return False
    except Exception as e:
        print(f"生成报告失败: {e}")
        print("如果问题仍然存在，请尝试手动运行命令:")
        if sys.platform.startswith('win'):
            print(f"allure serve {ALLURE_RESULTS_DIR}")
        else:
            print(f"allure serve {ALLURE_RESULTS_DIR}")
        return False

# 主函数
def main():
    # 解析命令行参数
    args = parse_arguments()
    
    # 清理旧的测试结果（如果需要）
    if args.clean or args.report:
        clean_old_results()
    
    # 运行测试
    start_time = time.time()
    success = run_tests(args.marker, args.keyword, args.verbose, args.reruns, args.rerun_delay)
    end_time = time.time()
    
    # 显示测试执行时间
    print(f"测试执行时间: {end_time - start_time:.2f} 秒")
    
    # 生成并打开报告（如果需要）
    if args.report:
        report_success = generate_and_open_report()
        if not report_success:
            print("注意：虽然无法生成Allure报告，但测试本身已经完成。")
            print("如需生成Allure报告，请按照指南安装Allure命令行工具。")
    else:
        print("测试已完成。如需生成Allure报告，请使用 -r 或 --report 参数运行脚本。")
    
    # 根据测试结果设置退出码
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()