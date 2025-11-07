import os
import time
import logging
from datetime import datetime
import re
import subprocess

class LogUtils:
    """日志工具类，用于数据埋点测试的日志管理"""
    
    def __init__(self, adb_utils, log_dir=None):
        """
        初始化日志工具
        
        Args:
            adb_utils: ADB工具实例
            log_dir: 日志保存目录，默认在logs目录
        """
        self.adb_utils = adb_utils
        self.log_dir = log_dir or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
        os.makedirs(self.log_dir, exist_ok=True)
        
        # 配置埋点日志记录器，精确到毫秒
        self.analytics_logger = logging.getLogger("analytics_tracker")
        self.analytics_logger.setLevel(logging.INFO)
        
        # 移除已存在的处理器
        for handler in self.analytics_logger.handlers[:]:
            self.analytics_logger.removeHandler(handler)
        
        # 创建文件处理器，使用毫秒级时间戳格式
        log_file = os.path.join(self.log_dir, f"analytics_tracking_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        
        # 添加处理器
        self.analytics_logger.addHandler(file_handler)
        self.analytics_logger.addHandler(console_handler)
        
        # 当前日志捕获进程和文件
        self.logcat_process = None
        self.current_log_file = None
        self.current_log_path = None
        self.log_level = 'I'  # 默认日志级别：INFO
    
    def clear_device_logs(self):
        """清除设备日志"""
        try:
            self.adb_utils._run_adb_command(['logcat', '-c'])
            self.analytics_logger.info("设备日志已清除")
        except Exception as e:
            self.analytics_logger.error(f"清除设备日志失败: {e}")
            raise
    
    def start_capturing_logs(self, log_tag=None, log_file=None):
        """
        开始捕获设备日志
        
        Args:
            log_tag: 要过滤的日志标签，如"Analytics"、"EventTracker"等
            log_file: 日志保存文件名，默认使用时间戳
        """
        # 先停止之前的日志捕获
        self.stop_capturing_logs()
        
        # 创建日志文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_log_file = log_file or f"device_logs_{timestamp}.log"
        self.current_log_path = os.path.join(self.log_dir, self.current_log_file)
        
        # 构建logcat命令
        cmd = ['adb', 'logcat']
        if log_tag:
            cmd.extend(['-s', log_tag])
        
        # 启动日志捕获进程
        try:
            self.analytics_logger.info(f"开始捕获设备日志，保存到: {self.current_log_path}")
            with open(self.current_log_path, 'w', encoding='utf-8') as f:
                self.logcat_process = subprocess.Popen(
                    cmd,
                    stdout=f,
                    stderr=subprocess.PIPE,
                    shell=False
                )
            time.sleep(1)  # 等待日志捕获进程启动
        except Exception as e:
            self.analytics_logger.error(f"启动日志捕获失败: {e}")
            self.logcat_process = None
            raise
    
    def stop_capturing_logs(self):
        """停止捕获设备日志"""
        if self.logcat_process:
            try:
                # 在Windows上使用Terminate
                if os.name == 'nt':
                    self.logcat_process.terminate()
                else:
                    self.logcat_process.send_signal(subprocess.signal.SIGINT)
                
                # 等待进程终止
                self.logcat_process.wait(timeout=5)
                self.analytics_logger.info(f"已停止日志捕获")
            except Exception as e:
                self.analytics_logger.error(f"停止日志捕获时出错: {e}")
            finally:
                self.logcat_process = None
    
    def track_event(self, event_id, action_description, additional_info=None):
        """
        记录埋点事件触发
        
        Args:
            event_id: 埋点事件ID
            action_description: 动作描述
            additional_info: 额外信息
        """
        timestamp_ms = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        log_message = f"埋点事件 [{event_id}] - {action_description}"
        
        if additional_info:
            log_message += f" - 额外信息: {additional_info}"
        
        self.analytics_logger.info(log_message)
        return timestamp_ms
    
    def search_events_in_logs(self, event_id, start_time=None, end_time=None):
        """
        在捕获的日志文件中搜索特定埋点事件
        
        Args:
            event_id: 要搜索的埋点事件ID
            start_time: 开始时间（可选）
            end_time: 结束时间（可选）
            
        Returns:
            list: 匹配的事件列表，包含时间戳和完整日志行
        """
        if not self.current_log_path or not os.path.exists(self.current_log_path):
            self.analytics_logger.warning("没有可用的日志文件进行搜索")
            return []
        
        matched_events = []
        event_pattern = re.compile(f".*{re.escape(event_id)}.*")
        
        try:
            with open(self.current_log_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    # 检查是否包含事件ID
                    if event_pattern.search(line):
                        # 提取logcat格式的时间戳 (例如: 03-15 14:23:45.123)
                        # 支持多种时间戳格式
                        log_time_match = re.search(r'(\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})|(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})', line)
                        if log_time_match:
                            log_time_str = log_time_match.group(1) or log_time_match.group(2)
                        else:
                            log_time_str = 'unknown'
                        
                        matched_events.append({
                            'timestamp': log_time_str,
                            'log_line': line.strip()
                        })
            
            self.analytics_logger.info(f"在日志文件中找到 {len(matched_events)} 个匹配事件 [{event_id}]")
            return matched_events
        
        except Exception as e:
            self.analytics_logger.error(f"搜索日志文件时出错: {e}")
            return []
    
    def search_events_in_live_logcat(self, event_id, max_lines=1000):
        """
        直接从设备的实时logcat中搜索特定埋点事件
        
        Args:
            event_id: 要搜索的埋点事件ID
            max_lines: 要搜索的最大行数
            
        Returns:
            list: 匹配的事件列表，包含时间戳和完整日志行
        """
        matched_events = []
        
        try:
            # 使用adb logcat -d获取最近的日志并搜索
            cmd = ['adb', 'logcat', '-d', f'*:{self.log_level}', f'*:S']
            result = self.adb_utils.execute_adb_command(cmd, timeout=10)
            
            if result and result.stdout:
                log_lines = result.stdout.splitlines()
                # 只处理最近的max_lines行
                recent_lines = log_lines[-max_lines:] if len(log_lines) > max_lines else log_lines
                
                for line in recent_lines:
                    if event_id in line:
                        # 提取时间戳
                        log_time_match = re.search(r'(\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})|(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})', line)
                        timestamp = log_time_match.group(1) or log_time_match.group(2) if log_time_match else 'unknown'
                        
                        matched_events.append({
                            'timestamp': timestamp,
                            'log_line': line.strip()
                        })
            
            self.analytics_logger.info(f"从实时logcat中找到 {len(matched_events)} 个匹配事件 [{event_id}]")
            return matched_events
        
        except Exception as e:
            self.analytics_logger.error(f"搜索实时logcat时出错: {e}")
            return []
    
    def __del__(self):
        """析构函数，确保日志捕获进程被正确终止"""
        self.stop_capturing_logs()


def get_log_utils(adb_utils, log_dir=None):
    """
    获取日志工具实例
    
    Args:
        adb_utils: ADB工具实例
        log_dir: 日志保存目录
        
    Returns:
        LogUtils: 日志工具实例
    """
    return LogUtils(adb_utils, log_dir)