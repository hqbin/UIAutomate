import allure
import time
import requests
import json
import re
from datetime import datetime

class AnalyticsTestBase:
    """数据埋点测试基类"""
    
    def __init__(self, adb_utils, log_utils, test_setup):
        """
        初始化埋点测试基类
        
        Args:
            adb_utils: ADB工具实例
            log_utils: 日志工具实例
            test_setup: 测试设置上下文
        """
        self.adb_utils = adb_utils
        self.log_utils = log_utils
        self.test_setup = test_setup
        self.test_dir = test_setup["test_dir"]
        self.event_records = []  # 记录所有触发的埋点事件
        self.successfully_verified_events = []  # 记录本地验证成功的埋点事件，用于后续远程验证
    
    def setup_for_event_test(self, event_id, log_tag=None):
        """
        为埋点事件测试设置环境
        
        Args:
            event_id: 埋点事件ID
            log_tag: 日志标签
        """
        with allure.step(f"准备测试埋点事件 [{event_id}]"):
            # 清除设备日志
            self.log_utils.clear_device_logs()
            
            # 开始捕获日志
            self.log_utils.start_capturing_logs(log_tag=log_tag)
            
            # 记录测试信息
            self.log_utils.analytics_logger.info(f"开始测试埋点事件: {event_id}")
    
    def trigger_event(self, event_id, action_func, action_description, **kwargs):
        """
        触发埋点事件并记录
        
        Args:
            event_id: 埋点事件ID
            action_func: 触发事件的函数
            action_description: 动作描述
            **kwargs: 传递给动作函数的参数
        """
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        
        with allure.step(f"触发埋点事件 [{event_id}] - {action_description}"):
            self.log_utils.analytics_logger.info(f"开始触发埋点事件: event_id={event_id}, action_description={action_description}")
            
            # 记录触发时间
            trigger_time = self.log_utils.track_event(event_id, action_description)
            
            # 执行触发动作
            try:
                result = action_func(**kwargs)
                time.sleep(1)  # 确保日志有足够时间被记录
                return result
            except Exception as e:
                self.log_utils.analytics_logger.error(f"执行动作时出错: {e}")
                raise
            finally:
                # 记录事件信息
                event_record = {
                    'event_id': event_id,
                    'trigger_time': trigger_time,
                    'start_time': start_time,
                    'action': action_description
                }
                self.event_records.append(event_record)

    
    def verify_event_triggered(self, event_id, timeout=3, retries=2):
        """
        验证埋点事件是否被触发 - 只从本地日志文件中查找并验证时间戳（精确到分钟）
        
        Args:
            event_id: 埋点事件ID
            timeout: 每次检查的超时时间（秒）
            retries: 重试次数
            
        Returns:
            bool: 是否成功触发
            list: 匹配的事件列表
        """
        with allure.step(f"验证埋点事件 [{event_id}] 是否被触发 (从日志文件中查找并验证时间到分钟)"):
            # 查找最近记录的该事件
            latest_record = None
            for record in reversed(self.event_records):
                if record['event_id'] == event_id:
                    latest_record = record
                    break
            
            if not latest_record:
                return False, []
            
            # 从日志文件中搜索事件
            for attempt in range(retries + 1):
                # 从本地日志文件中搜索
                self.log_utils.analytics_logger.info(f"正在日志文件中搜索事件 [{event_id}] (第{attempt+1}次尝试)")
                log_file_events = self.log_utils.search_events_in_logs(event_id)
                
                # 验证事件并检查时间戳
                matched_events = []
                action_time = latest_record['trigger_time']
                
                # 解析操作时间（精确到分钟）
                try:
                    action_time_dt = datetime.strptime(action_time, "%Y-%m-%d %H:%M:%S.%f")
                    # 格式化为统一的格式
                    action_time_min = action_time_dt.strftime("%Y-%m-%d %H:%M")
                except ValueError:
                    # 如果无法解析，尝试其他格式
                    try:
                        action_time_dt = datetime.strptime(action_time, "%m-%d %H:%M:%S.%f")
                        # 为logcat格式添加年份并格式化为统一格式
                        current_year = datetime.now().year
                        action_time_min = f"{current_year}-{action_time_dt.strftime('%m-%d %H:%M')}"
                    except ValueError:
                        # 如果无法解析，尝试直接提取时间部分
                        try:
                            # 检查是否包含年份
                            if len(action_time) >= 19 and '-' in action_time and ':' in action_time:
                                # 假设格式为 YYYY-MM-DD HH:MM:SS
                                action_time_min = action_time[:16]  # 提取到分钟
                            elif len(action_time) >= 17 and action_time.count('-') == 1:
                                # 假设格式为 MM-DD HH:MM:SS (logcat格式)
                                # 添加年份并格式化为统一格式
                                current_year = datetime.now().year
                                date_part = action_time[:5]  # MM-DD
                                time_part = action_time[6:11]  # HH:MM
                                action_time_min = f"{current_year}-{date_part} {time_part}"
                            else:
                                action_time_min = action_time[:16]  # 兜底截取
                        except:
                            action_time_min = action_time[:16]  # 最终兜底
                
                self.log_utils.analytics_logger.info(f"操作时间（精确到分钟）: {action_time_min}")
                
                for event in log_file_events:
                    event_time = event['timestamp']
                    
                    # 解析事件时间（从秒级转换到分钟级）
                    try:
                        # 尝试解析完整时间格式
                        if len(event_time) >= 19:
                            event_time_dt = datetime.strptime(event_time[:19], "%Y-%m-%d %H:%M:%S")
                            # 格式化为统一的格式
                            event_time_min = event_time_dt.strftime("%Y-%m-%d %H:%M")
                        else:
                            # 尝试解析logcat格式 (MM-DD HH:MM:SS)
                            event_time_dt = datetime.strptime(event_time[:17], "%m-%d %H:%M:%S")
                            # 为logcat格式添加年份并格式化为统一格式
                            current_year = datetime.now().year
                            event_time_min = f"{current_year}-{event_time_dt.strftime('%m-%d %H:%M')}"
                    except ValueError:
                        # 如果无法解析，尝试直接提取时间部分
                        try:
                            # 检查是否包含年份
                            if len(event_time) >= 19 and '-' in event_time and ':' in event_time:
                                # 假设格式为 YYYY-MM-DD HH:MM:SS
                                event_time_min = event_time[:16]  # 提取到分钟
                            elif len(event_time) >= 17 and event_time.count('-') == 1:
                                # 假设格式为 MM-DD HH:MM:SS (logcat格式)
                                # 添加年份并格式化为统一格式
                                current_year = datetime.now().year
                                date_part = event_time[:5]  # MM-DD
                                time_part = event_time[6:11]  # HH:MM
                                event_time_min = f"{current_year}-{date_part} {time_part}"
                            else:
                                event_time_min = event_time[:16]  # 兜底截取
                        except:
                            event_time_min = event_time[:16]  # 最终兜底
                    
                    self.log_utils.analytics_logger.info(f"事件时间（精确到分钟）: {event_time_min}")
                    
                    # 验证时间是否匹配（精确到分钟）
                    if event_time_min == action_time_min:
                        matched_events.append(event)
                        self.log_utils.analytics_logger.info(f"找到匹配的事件，时间一致（精确到分钟）: {event_time_min}")
                    else:
                        self.log_utils.analytics_logger.warning(f"时间不匹配：{action_time_min} != {event_time_min}（均已格式化为YYYY-MM-DD HH:MM格式）")
                
                if matched_events:
                    # 成功验证事件时的详细日志
                    self.log_utils.analytics_logger.info(f"成功验证事件 [{event_id}] 被触发，共 {len(matched_events)} 次（时间匹配）")
                    self.log_utils.analytics_logger.info(f"事件验证成功，将添加到successfully_verified_events列表，当前列表长度: {len(self.successfully_verified_events)}")
                    
                    # 将匹配的事件添加到allure报告
                    for event in matched_events:
                        allure.attach(
                            f"时间: {event['timestamp']}\n操作时间: {action_time}\n时间匹配(分钟级别): {action_time_min == event_time_min}\n统一格式化后操作时间: {action_time_min}\n统一格式化后事件时间: {event_time_min}\n日志: {event['log_line']}",
                            name=f"埋点事件 [{event_id}] - 触发记录（时间匹配到分钟）",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        # 记录每个匹配事件的详细信息到日志
                        self.log_utils.analytics_logger.info(f"Match Event Detail: event_id={event_id}, timestamp={event['timestamp']}, log_line={event['log_line']}")
                    
                    # 记录验证成功的事件，用于后续远程验证
                    # 查找对应的事件描述
                    event_description = ''
                    self.log_utils.analytics_logger.info(f"开始查找事件描述，event_records长度: {len(self.event_records)}")
                    # 遍历所有事件记录，不仅仅是反向遍历，确保找到所有可能的匹配
                    for record in self.event_records:
                        self.log_utils.analytics_logger.info(f"检查记录: event_id={record.get('event_id')}, action={record.get('action')}")
                        if str(record.get('event_id', '')) == str(event_id):
                            event_description = record.get('action', '')
                            self.log_utils.analytics_logger.info(f"找到匹配的事件描述: event_id={event_id}, description={event_description}, record={record}")
                            break
                    # 如果第一次查找失败，尝试反向遍历作为备份
                    if not event_description:
                        for record in reversed(self.event_records):
                            self.log_utils.analytics_logger.info(f"反向检查记录: event_id={record.get('event_id')}, action={record.get('action')}")
                            if str(record.get('event_id', '')) == str(event_id):
                                event_description = record.get('action', '')
                                self.log_utils.analytics_logger.info(f"反向查找找到匹配的事件描述: {event_description}")
                                break
                        else:
                            self.log_utils.analytics_logger.warning(f"未找到事件ID {event_id} 的描述，event_records内容: {self.event_records}")
                    
                    events_to_add = [
                        {'event_id': event_id, 'timestamp': event['timestamp'], 'log_line': event['log_line'], 'description': event_description}
                        for event in matched_events
                    ]
                    
                    # 添加调试日志
                    self.log_utils.analytics_logger.info(f"添加到successfully_verified_events的事件: {events_to_add}")
                    self.successfully_verified_events.extend(events_to_add)
                    self.log_utils.analytics_logger.info(f"添加了 {len(events_to_add)} 个事件到successfully_verified_events，更新后的长度: {len(self.successfully_verified_events)}")
                    # 再次确认已添加事件的描述
                    self.log_utils.analytics_logger.info(f"最近添加的事件描述: {self.successfully_verified_events[-1].get('description', '无') if self.successfully_verified_events else '无'}")
                    
                    return True, matched_events
                
                if attempt < retries:
                    self.log_utils.analytics_logger.info(f"第 {attempt + 1} 次尝试未找到事件 [{event_id}]，等待 {timeout} 秒后重试...")
                    time.sleep(timeout)
            
            self.log_utils.analytics_logger.warning(f"所有尝试均未从日志文件中找到事件 [{event_id}] 的触发记录，或时间不匹配（精确到分钟）")
            return False, []
    
    def teardown_event_test(self, event_id):
        """
        埋点事件测试结束清理
        
        Args:
            event_id: 埋点事件ID
        """
        with allure.step(f"结束测试埋点事件 [{event_id}]"):
            # 停止日志捕获
            self.log_utils.stop_capturing_logs()
            
            # 记录测试结束
            self.log_utils.analytics_logger.info(f"埋点事件测试 [{event_id}] 结束")
    
    
    def execute_path_operation_with_analytics(self, event_id, path_operations, target_action, 
                                             path_description="执行路径操作", 
                                             target_description="目标操作"):
        """
        执行一系列路径操作后触发目标动作，并验证埋点事件（只从日志文件验证并检查时间戳到分钟）
        
        Args:
            event_id: 目标埋点事件ID
            path_operations: 路径操作列表，每个元素为(函数, 描述, 参数字典)元组
                            或使用create_remote_key_operation创建的操作
            target_action: 触发埋点的目标动作函数
            path_description: 路径操作描述
            target_description: 目标动作描述
            
        Returns:
            bool: 是否成功验证埋点
            list: 匹配的事件列表
        """
        with allure.step(f"执行路径操作并验证埋点事件 [{event_id}] (时间验证到分钟)"):
            # 开始埋点验证前的准备
            self.log_utils.analytics_logger.info(f"开始执行埋点验证: 事件ID [{event_id}], 路径: {path_description}, 目标: {target_description}")
            
            # 路径操作开始前添加截图 - 路径初始化后
            self.adb_utils.添加截图到allure报告("路径初始化后", test_dir=self.test_dir)
            
            # 执行路径操作
            for i, operation in enumerate(path_operations):
                # 处理元组格式的操作 (函数, 描述, 参数)
                if isinstance(operation, tuple) and len(operation) >= 2:
                    func, desc, params = operation if len(operation) == 3 else (operation[0], operation[1], {})
                    
                    with allure.step(f"路径操作 {i+1}: {desc}"):
                        try:
                            self.log_utils.analytics_logger.info(f"执行路径操作 {i+1}: {desc}")
                            func(**params)
                            # 每个路径操作后添加短暂延迟
                            time.sleep(0.5)
                        except Exception as e:
                            self.log_utils.analytics_logger.error(f"执行路径操作 {i+1} 失败: {e}")
                            raise
                else:
                    # 未知格式，跳过
                    self.log_utils.analytics_logger.warning(f"跳过未知格式的路径操作: {operation}")
            time.sleep(1)
            # 路径操作完成后添加截图
            self.adb_utils.添加截图到allure报告("路径操作完成后", test_dir=self.test_dir)
            
            # 触发目标动作并记录埋点
            trigger_time = datetime.now()
            self.log_utils.analytics_logger.info(f"准备触发目标动作 [{target_description}]，事件ID: [{event_id}]")
            self.trigger_event(
                event_id=event_id,
                action_func=target_action,
                action_description=target_description
            )
            
            self.log_utils.analytics_logger.info(f"目标动作触发时间: {trigger_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 添加目标操作后的截图
            self.adb_utils.添加截图到allure报告("目标操作完成后", test_dir=self.test_dir)
            
            # 验证埋点事件是否触发（会自动验证时间戳）
            self.log_utils.analytics_logger.info(f"开始验证埋点事件 [{event_id}] 是否被触发")
            success, events = self.verify_event_triggered(event_id)
            
            if success:
                self.log_utils.analytics_logger.info(f"路径操作完成并成功验证埋点事件 [{event_id}]（时间匹配到分钟）")
                self.log_utils.analytics_logger.info(f"当前successfully_verified_events列表长度: {len(self.successfully_verified_events)}")
                # 打印最近添加的事件信息
                if events:
                    self.log_utils.analytics_logger.info(f"最近验证成功的事件详情: {events[-1]}")
            else:
                self.log_utils.analytics_logger.warning(f"路径操作完成但未能验证埋点事件 [{event_id}]，可能时间不匹配（精确到分钟）")
                # 记录失败原因
                self.log_utils.analytics_logger.warning(f"埋点验证失败 - 成功状态: {success}, 匹配事件数: {len(events)}")
                
            return success, events
    
    def create_remote_key_operation(self, key_name, key_function=None):
        """
        创建遥控器按键操作，用于构建路径操作序列
        
        Args:
            key_name: 按键名称
            key_function: 自定义按键函数
            
        Returns:
            tuple: (操作函数, 操作描述, 参数字典)
        """
        if key_function is None:
            key_functions = {
                'home': self.adb_utils.点击遥控主页,
                'ok': self.adb_utils.点击遥控OK,
                'back': self.adb_utils.点击遥控返回,
                'menu': self.adb_utils.点击遥控菜单,
                'up': self.adb_utils.点击遥控上,
                'down': self.adb_utils.点击遥控下,
                'left': self.adb_utils.点击遥控左,
                'right': self.adb_utils.点击遥控右
            }
            
            if key_name.lower() not in key_functions:
                raise ValueError(f"未知的按键名称: {key_name}")
            
            key_function = key_functions[key_name.lower()]
        
        return (key_function, f"按下遥控器 {key_name} 键", {})
    
    def verify_remote_analytics_data(self, mac_address, wait_minutes=15, csv_url=None):
        """
        等待指定时间后，从CSV链接获取埋点数据并验证本地成功的埋点是否已上报
        
        Args:
            mac_address: 设备MAC地址
            wait_minutes: 等待时间（分钟），默认15分钟
            csv_url: CSV文件的完整URL，如果为None则使用固定前缀+MAC地址生成
            
        Returns:
            tuple: (验证成功状态, 验证结果详情)
        """
        with allure.step(f"远程埋点数据验证（等待{wait_minutes}分钟后执行）"):
            # 检查是否有需要验证的事件
            if not self.successfully_verified_events:
                return False, {"error": "没有本地验证成功的埋点事件"}
            
            allure.attach(
                f"等待时间: {wait_minutes}分钟\n" +
                f"设备MAC: {mac_address}\n" +
                f"需要验证的事件数: {len(self.successfully_verified_events)}",
                name="远程验证配置",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # 等待指定时间
            for i in range(wait_minutes):
                self.log_utils.analytics_logger.info(f"等待中... {i+1}/{wait_minutes}分钟")
                time.sleep(60)  # 等待1分钟
            
            # 使用固定前缀的CSV URL
            if not csv_url:
                # 使用MAC地址生成一个固定的文件名（移除冒号并转换为小写）
                csv_filename = f"analytics_data_{mac_address.replace(':', '').lower()}.csv"
                csv_url = f"https://cdntest.zeasn.tv/AI_output/AI_athena_result/{csv_filename}"
            
            self.log_utils.analytics_logger.info(f"从CSV链接获取埋点数据: {csv_url}")
            
            # 从CSV链接获取远程埋点数据
            try:
                response = requests.get(
                    csv_url,
                    timeout=30
                )
                response.raise_for_status()
                remote_data = response.text
                self.log_utils.analytics_logger.info(f"成功获取远程CSV数据，响应长度: {len(remote_data)} 字符")
                
            except Exception as e:
                error_msg = f"获取远程CSV数据失败: {str(e)}"
                self.log_utils.analytics_logger.error(error_msg)
                allure.attach(
                    error_msg,
                    name="远程请求错误",
                    attachment_type=allure.attachment_type.TEXT
                )
                return False, {"error": error_msg}
            
            # 解析CSV数据，提取所有事件信息
            csv_events = []
            lines = remote_data.split('\n')
            headers = None
            
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                    
                if i == 0:
                    # 解析表头
                    headers = [h.strip() for h in line.split(',')]
                    continue
                    
                # 解析数据行
                values = line.split(',')
                if len(values) >= len(headers):
                    event_data = {}
                    for j, header in enumerate(headers):
                        if j < len(values):
                            event_data[header.lower()] = values[j].strip()
                    csv_events.append(event_data)
            
            self.log_utils.analytics_logger.info(f"从CSV中解析出 {len(csv_events)} 个事件")
            
            # 验证每个本地成功的埋点是否在CSV数据中存在
            verification_results = {
                "total": len(self.successfully_verified_events),
                "found": 0,
                "not_found": 0,
                "details": []
            }
            
            for event in self.successfully_verified_events:
                # 优先使用事件记录中的timestamp字段
                if 'timestamp' in event and event['timestamp']:
                    event_timestamp = event['timestamp']
                else:
                    # 如果没有timestamp字段，则尝试从log_line中提取
                    timestamp_match = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3})', event.get('log_line', ''))
                    if timestamp_match:
                        event_timestamp = timestamp_match.group(1)
                    else:
                        status = "NO_TIMESTAMP"
                        verification_results["not_found"] += 1
                        event_timestamp = "N/A"
                        verification_results["details"].append({
                            "event_id": event.get("event_id", "未知"),
                            "timestamp": event_timestamp,
                            "status": status
                        })
                        continue
                
                # 在CSV数据中查找匹配的时间戳
                found_match = False
                matched_event = None
                
                for csv_event in csv_events:
                    # 优先检查CSV文件的第一列（通过索引0获取）
                    # 因为headers[0]是第一列的列名
                    if headers and len(headers) > 0:
                        first_column_name = headers[0].lower()
                        if first_column_name in csv_event and csv_event[first_column_name]:
                            csv_timestamp = csv_event[first_column_name]
                            # 检查是否匹配
                            if event_timestamp in csv_timestamp:
                                found_match = True
                                matched_event = csv_event
                                break
                    
                    # 如果第一列匹配失败，再尝试其他可能的时间戳字段名
                    if not found_match:
                        csv_timestamp = None
                        for key in ['timestamp', '时间戳', 'event_time', 'event_timestamp']:
                            if key in csv_event and csv_event[key]:
                                csv_timestamp = csv_event[key]
                                if event_timestamp in csv_timestamp:
                                    found_match = True
                                    matched_event = csv_event
                                    break
                        if found_match:
                            break
                
                if found_match:
                    status = "找到"
                    verification_results["found"] += 1
                    
                    # 只记录对比成功的结果，使用@allure.story+event_id+timestamp格式
                    story_name = f"@allure.story+{event.get('event_id', '未知')}+{event_timestamp}"
                    
                    # 确保description正确提取
                    event_description = event.get('description', '')
                    self.log_utils.analytics_logger.info(f"匹配到本地事件: event_id={event.get('event_id', '未知')}, description={event_description}, event={event}")
                    
                    # 记录成功匹配的详情
                    match_details = {
                        "event_id": str(event.get("event_id", "未知")),  # 统一为字符串类型
                        "timestamp": event_timestamp,
                        "status": status,
                        "matched_csv_data": matched_event,
                        "data_fields": event.get("data_fields", []),  # 传递原始事件中的data_fields
                        "description": event_description  # 确保description字段存在
                    }
                    self.log_utils.analytics_logger.info(f"构建匹配详情: {match_details}")
                    verification_results["details"].append(match_details)
                    
                    # 记录到Allure报告中，使用指定格式的名称
                    allure.attach(
                        f"本地事件ID: {event.get('event_id', '未知')}\n" +
                        f"时间戳: {event_timestamp}\n" +
                        f"匹配的CSV数据: {json.dumps(matched_event, ensure_ascii=False)}",
                        name=story_name,
                        attachment_type=allure.attachment_type.TEXT
                    )
                    
                    self.log_utils.analytics_logger.info(f"远程验证成功: {story_name}")
                else:
                    status = "未找到"
                    verification_results["not_found"] += 1
                    self.log_utils.analytics_logger.warning(f"远程验证失败: 事件ID {event.get('event_id', '未知')} 的时间戳 {event_timestamp} 在CSV数据中未找到")
                    
                    # 确保description正确提取
                    event_description = event.get('description', '')
                    self.log_utils.analytics_logger.info(f"为未匹配事件找到描述: event_id={event.get('event_id', '未知')}, description={event_description}")
                    
                    # 如果在当前事件中没找到描述，尝试从原始event_records中获取
                    if not event_description:
                        for record in self.event_records:
                            if str(record.get('event_id', '')) == str(event.get('event_id', '')):
                                event_description = record.get('action', '')
                                self.log_utils.analytics_logger.info(f"从event_records获取描述: event_id={event.get('event_id', '未知')}, description={event_description}")
                                break
                    
                    no_match_detail = {
                        "event_id": str(event.get("event_id", "未知")),  # 统一为字符串类型
                        "timestamp": event_timestamp,
                        "status": status,
                        "description": event_description  # 确保description字段存在，即使为空
                    }
                    self.log_utils.analytics_logger.info(f"添加未匹配详情: {no_match_detail}")
                    verification_results["details"].append(no_match_detail)
            
            # 生成验证报告
            report_text = f"远程埋点数据验证报告:\n"
            report_text += f"总事件数: {verification_results['total']}\n"
            report_text += f"在远程数据中找到: {verification_results['found']}\n"
            report_text += f"在远程数据中未找到: {verification_results['not_found']}\n\n"
            report_text += "详细结果:\n"
            
            for detail in verification_results["details"]:
                report_text += f"- 事件ID: {detail['event_id']}, 时间戳: {detail['timestamp']}, 状态: {detail['status']}\n"
            
            self.log_utils.analytics_logger.info(report_text)
            allure.attach(
                report_text,
                name="远程埋点验证报告",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # 判断验证是否成功（所有事件都找到）
            is_success = verification_results["not_found"] == 0 and verification_results["total"] > 0
            
            return is_success, verification_results