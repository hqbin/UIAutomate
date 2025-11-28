import allure
import pytest
import re
import os
import json
from datetime import datetime
import requests


def extract_events_from_log_file_fixed(log_file_path):
    results = []
    
    try:
        with open(log_file_path, "r", encoding="latin1") as f:
            for line in f:
                # 检查是否包含Match Event Detail
                if "Match Event Detail" in line:
                    # 提取event_id
                    event_match = re.search(r"event_id=(\d+)", line)
                    event = event_match.group(1) if event_match else "N/A"
                    
                    # 尝试提取时间戳和数据字段
                    timestamp = "N/A"
                    data_fields = []
                    
                    # 处理zeasn_HttpRequest格式: params:{"data":"时间戳,字段1,字段2,..."
                    if "zeasn_HttpRequest" in line:
                        data_match = re.search(r'params:\{"data":"([^"]*)","logType"', line)
                        if data_match:
                            data_content = data_match.group(1)
                            # 将data内容按逗号分割成多个字段
                            data_fields = data_content.split(',')
                            # 第一个字段是时间戳
                            if len(data_fields) > 0:
                                timestamp = data_fields[0]
                    
                    # 处理zeasn_db格式: EventBean{ data = 时间戳,字段1,字段2,...
                    elif "zeasn_db" in line:
                        data_match = re.search(r'EventBean\{ data = ([^,]*)', line)
                        if data_match:
                            # 提取整个data字符串
                            full_data = data_match.group(1)
                            # 分割数据字段
                            data_fields = full_data.split(',')
                            # 第一个字段是时间戳
                            if len(data_fields) > 0:
                                timestamp = data_fields[0]
                    
                    # 构建完整的事件信息
                    event_info = {
                        "event_id": event,
                        "timestamp": timestamp,
                        "data_fields": data_fields  # 包含所有逗号分隔的数据字段
                    }
                    
                    # 如果有更多字段，可以单独提取一些重要的字段
                    if len(data_fields) > 1:
                        event_info["timezone"] = data_fields[1] if data_fields[1] else "N/A"
                    if len(data_fields) > 5:
                        event_info["event_record_id"] = data_fields[5] if data_fields[5] else "N/A"
                    if len(data_fields) > 6:
                        event_info["device_mac"] = data_fields[6] if data_fields[6] else "N/A"
                    
                    results.append(event_info)
    except Exception as e:
        print(f"[DEBUG] 读取日志文件时出错: {e}")
    return results


# 修改测试函数中的路径处理部分
@allure.feature("大数据日志")
@allure.story("远程埋点验证")
@pytest.mark.analytics
def test_analytics_verification(analytics_test):
    """
    从程序执行日志中提取对比成功的埋点数据，并与远程CSV数据进行验证
    """
    # 设备MAC地址，根据用户提供的信息
    DEVICE_MAC_ADDRESS = "98:C9:BE:1B:19:F2"
    
    # 修正日志目录路径 - 使用绝对路径或相对项目根目录的路径
    LOG_DIR = "logs"  # 直接使用相对路径
    # 或者使用项目根目录的相对路径
    # LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
    
    # 等待时间（分钟），用于远程验证
    WAIT_MINUTES = 0
    
    with allure.step("从程序执行日志中提取埋点事件信息"):
        analytics_test.log_utils.analytics_logger.info(f"开始从日志目录 {LOG_DIR} 中提取埋点事件信息")
        
        # 定义程序执行日志文件路径模式
        # "analytics_tracking_\d{8}_\d{6}\.log"
        
        log_file_pattern = re.compile(r"analytics_tracking_\d{8}_\d{6}\.log")
        
        # 从日志中提取的事件列表
        extracted_events = []
        
        try:
            # 检查日志目录是否存在
            if not os.path.exists(LOG_DIR):
                analytics_test.log_utils.analytics_logger.warning(f"日志目录不存在: {LOG_DIR}")
                # 尝试创建目录或使用其他路径
                return
            
            # 获取目录中的所有日志文件
            log_files = []
            for filename in os.listdir(LOG_DIR):
                if log_file_pattern.match(filename):
                    full_path = os.path.join(LOG_DIR, filename)
                    log_files.append(full_path)
            
            # 按修改时间排序，获取最新的日志文件
            log_files.sort(key=os.path.getmtime, reverse=True)
            
            analytics_test.log_utils.analytics_logger.info(f"找到 {len(log_files)} 个analytics_tracking日志文件")
            
            if not log_files:
                analytics_test.log_utils.analytics_logger.warning("未找到匹配的程序执行日志文件")
                return
            
            # 处理所有找到的日志文件
            for log_file in log_files:
                analytics_test.log_utils.analytics_logger.info(f"开始处理程序执行日志文件: {log_file}")
                
                try:
                    file_events = extract_events_from_log_file_fixed(log_file)
                    # 转换提取的事件格式并直接添加到验证列表（不去重）
                    for event in file_events:
                        timestamp = event.get('timestamp', 'N/A')
                        # 从params:data提取的时间戳已经是ISO格式，直接使用
                        iso_timestamp = timestamp
                            
                        # 直接创建analytics_test_event格式并添加到验证列表
                        # 创建更详细的log_line格式，包含完整的事件信息
                        # 添加data_fields的详细信息到log_line
                        data_fields_str = ", ".join([f"field_{i}={field}" for i, field in enumerate(event.get('data_fields', [])) if field])
                        
                        analytics_test_event = {
                            'event_id': event['event_id'],
                            'log_line': f"event_id={event['event_id']}, timestamp={timestamp}, extracted_from_params_data, {data_fields_str}",
                            'timestamp': iso_timestamp,
                            'data_fields': event.get('data_fields', [])  # 保存完整的数据字段
                        }
                        analytics_test.successfully_verified_events.append(analytics_test_event)
                    
                except Exception as e:
                    analytics_test.log_utils.analytics_logger.error(f"处理程序执行日志文件失败 {log_file}: {e}")
            
            analytics_test.log_utils.analytics_logger.info(f"已将 {len(analytics_test.successfully_verified_events)} 个事件添加到验证列表")
            
            # 如果提取到事件，添加到Allure报告作为附件
            if analytics_test.successfully_verified_events:
                allure.attach(
                    json.dumps(analytics_test.successfully_verified_events, ensure_ascii=False, indent=2),
                    name="提取的埋点事件详情",
                    attachment_type=allure.attachment_type.JSON
                )
            
        except Exception as e:
            analytics_test.log_utils.analytics_logger.error(f"日志提取过程中发生错误: {e}")
    
    with allure.step("开始远程埋点数据验证"):
        
        # 预先初始化csv_url变量，避免UnboundLocalError
        csv_url = None
        
        try:
            # 创建一个会话来保存cookies和headers
            session = requests.Session()
            
            # 1. 访问passport URL以获取可能的授权信息
            workflow_url = "https://dify.zeasn.com/api/passport"
            
            # 设置请求头参数
            headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9",
            "content-type": "application/json",
            "referer": "https://dify.zeasn.com/workflow/90PLBPz8X0kyP4Jt",
            "sec-ch-ua": '"Chromium";v="142", "Microsoft Edge";v="142", "Not_A Brand";v="99"',
            "sec-ch-ua-mobile": "?1",
            "sec-ch-ua-platform": '"Android"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Mobile Safari/537.36 Edg/142.0.0.0",
            "x-app-code": "90PLBPz8X0kyP4Jt"
        }
            
            # 发送GET请求访问passport页面
            workflow_response = session.get(workflow_url, headers=headers, allow_redirects=True)
            
            # 解析响应文本获取access_token
            try:
                token_data = workflow_response.json()
                if 'access_token' in token_data:
                    access_token = token_data['access_token']
                else:
                    access_token = None
            except Exception as e:
                access_token = None
            
            # 2. 使用获取到的授权信息调用API
            dify_url = "https://dify.zeasn.com/api/workflows/run"
            
            # 准备请求参数，使用当前日期和前一天日期的年月日格式，用英文逗号分隔
            from datetime import datetime, timedelta
            # 获取当前日期
            today = datetime.now()
            # 获取前一天日期
            yesterday = today - timedelta(days=1)
            # 格式化为YYYY-MM-DD,YYYY-MM-DD格式
            current_date = f"{today.strftime('%Y-%m-%d')},{yesterday.strftime('%Y-%m-%d')}"
            
            payload = {
                "inputs": {
                    "date": current_date,
                    "mac": DEVICE_MAC_ADDRESS
                },
                "response_mode": "streaming"
            }
            
            # 构建headers，保留浏览器相关的headers并添加Content-Type和authorization
            request_headers = headers.copy()
            request_headers["Content-Type"] = "application/json"
            if access_token:
                request_headers["authorization"] = f"Bearer {access_token}"
            elif 'authorization' in locals():
                request_headers["authorization"] = access_token
            
            
            
            # 使用session发送请求，这样会自动携带cookies和相关headers
            response = session.post(dify_url, headers=request_headers, data=json.dumps(payload))
            
            try:
                response_data = response.json()
                
                import time
                time.sleep(5)
                
                # 从响应中提取 CSV 下载链接
                csv_url = None
                response_text = json.dumps(response_data, ensure_ascii=False)
            except Exception as e:
                response_text = response.text
            # 打印响应文本以调试

        except Exception as e:
            response_text = response.text
        
        # 三级CSV链接提取逻辑
        csv_url = None
        
        # 第一级：尝试直接从响应中查找随机生成的CSV文件名格式（UUID格式）
        if not csv_url and response_text:
            # 匹配UUID格式的CSV文件名：xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.csv
            match = re.search(r'https://cdntest\.zeasn\.tv/[^"\']*/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.csv', response_text)
            if match:
                csv_url = match.group(0)
        
        # 第二级：使用更通用的正则表达式匹配任意CSV链接
        if not csv_url and response_text:
            match = re.search(r'https://cdntest\.zeasn\.tv/[^"\']*\.csv', response_text)
            if match:
                csv_url = match.group(0)
        
        
        # 下载CSV文件并备份到logs目录
        if csv_url:
            try:
                # 生成带时间戳的文件名
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                csv_filename = f"analytics_backup_{timestamp}.csv"
                csv_backup_path = os.path.join(LOG_DIR, csv_filename)
                
                # 确保logs目录存在
                os.makedirs(LOG_DIR, exist_ok=True)
                
                # 下载CSV文件
                csv_response = requests.get(csv_url, timeout=30)
                csv_response.raise_for_status()  # 检查请求是否成功
                
                # 保存文件
                with open(csv_backup_path, 'wb') as f:
                    f.write(csv_response.content)
                analytics_test.log_utils.analytics_logger.info(f"CSV文件已成功备份到: {csv_backup_path}")
                
                # 添加到Allure报告作为附件
                allure.attach(
                    csv_response.content,
                    name=f"备份CSV数据_{timestamp}",
                    attachment_type=allure.attachment_type.CSV
                )
            except Exception as e:
                analytics_test.log_utils.analytics_logger.error(f"备份CSV文件失败: {str(e)}")
    # 外层try-except已在前面处理
    
    # 使用获取到的 CSV 链接进行远程埋点验证
    success, results = analytics_test.verify_remote_analytics_data(
        mac_address=DEVICE_MAC_ADDRESS,
        wait_minutes=WAIT_MINUTES,
        csv_url=csv_url
    )
    
    # 记录总体验证结果到Allure报告
    allure.attach(
        f"验证结果: {'成功' if success else '失败'}\n" +
        (f"找到事件数: {results.get('found', 0)}\n" if 'found' in results else "") +
        (f"未找到事件数: {results.get('not_found', 0)}\n" if 'not_found' in results else "") +
        (f"错误信息: {results.get('error', '')}\n" if 'error' in results else ""),
        name="远程埋点验证总结果",
        attachment_type=allure.attachment_type.TEXT
    )
    
    # 添加数据字段验证步骤
    data_field_verification_results = []
    verification_success = True  # 初始假设验证成功
    
    # 添加调试信息，确保验证步骤执行
    analytics_test.log_utils.analytics_logger.info(f"开始数据字段验证，results结构: {list(results.keys())}")
    
    # 为每个事件单独创建Allure报告条目，并在其中进行数据字段验证
    if 'details' in results and results['details']:
        analytics_test.log_utils.analytics_logger.info(f"验证结果详情数量: {len(results['details'])}")
        for event in results['details']:
            event_id = event.get('event_id', '未知ID')
            status = event.get('status', '未知')  # 直接使用原始状态值，已经是中文的'找到'或'未找到'
            timestamp = event.get('timestamp', '未知时间戳')
            
            # 为每个事件创建独立的Allure步骤，添加事件描述
            description = event.get('description', '')
            
            # 增强调试信息，记录完整的事件对象
            analytics_test.log_utils.analytics_logger.info(f"处理事件详情: event_id={event_id}, description={description}, status={status}")
            analytics_test.log_utils.analytics_logger.info(f"事件对象完整信息: {event}")
            
            # 构建步骤名称
            analytics_test.log_utils.analytics_logger.info(f"事件对象详情: event_id={event_id}, description={description}")
            
            # 根据是否有描述构建不同的步骤名称
            if description:
                step_name = f"事件 {event_id} - {description} 验证 - {status}"
            else:
                step_name = f"事件 {event_id} 验证 - {status}"
            analytics_test.log_utils.analytics_logger.info(f"使用步骤名称: {step_name}")
            with allure.step(step_name):
                # 添加事件基本信息
                allure.attach(f"事件ID: {event_id}", "事件信息", allure.attachment_type.TEXT)
                allure.attach(f"时间戳: {timestamp}", "事件信息", allure.attachment_type.TEXT)
                allure.attach(f"状态: {status}", "事件信息", allure.attachment_type.TEXT)
                
                # 如果事件已在CSV中找到，进行数据字段验证
                if status == '找到':
                    # 获取事件的data_fields和matched_csv_data
                    # 注意：data_fields[0]是时间戳，已经用来匹配了，不需要重复验证
                    data_fields = event.get('data_fields', [])
                    matched_csv_data = event.get('matched_csv_data', {})
                    
                    # 在Allure报告中添加提取的数据字段信息
                    allure.attach(f"提取的数据字段总数: {len(data_fields)}", "提取数据", allure.attachment_type.TEXT)
                    
                    # 格式化展示提取的数据字段
                    extracted_fields_str = "提取的数据字段:\n"
                    # 直接遍历data_fields中的所有字段，确保不会遗漏任何数据
                    for i, field in enumerate(data_fields):
                        field_value = str(field).strip() if field is not None else "None"
                        field_type = "时间戳" if i == 0 else f"数据字段{i}"
                        extracted_fields_str += f"{field_type}: {field_value}\n"
                    allure.attach(extracted_fields_str, "提取的数据字段详情", allure.attachment_type.TEXT)
                    
                    # 格式化展示匹配的CSV数据
                    matched_csv_str = "匹配的CSV数据:\n"
                    # 直接遍历所有键值对，确保不会遗漏任何数据
                    for key, value in matched_csv_data.items():
                        value_str = str(value).strip() if value is not None else "None"
                        matched_csv_str += f"{key}: {value_str}\n"
                    allure.attach(matched_csv_str, "匹配的CSV数据详情", allure.attachment_type.TEXT)
                    
                    # 获取CSV数据中所有的值（忽略键名）
                    csv_values = []
                    for value in matched_csv_data.values():
                        if value and isinstance(value, str):
                            csv_values.append(value.strip())
                    
                    # 将CSV值列表转换为单个字符串以进行搜索
                    csv_data_str = ' '.join(csv_values)
                    
                    # 验证数据字段（跳过第一个时间戳字段）
                    missing_fields = []
                    found_fields = []
                    
                    # 从索引1开始遍历，跳过时间戳字段
                    for i, field in enumerate(data_fields):
                        if i == 0:  # 跳过第一个时间戳字段
                            continue
                        
                        if field and field.strip():
                            field_value = field.strip()
                            # 检查字段是否在CSV数据中存在
                            field_found = False
                            # 1. 先检查是否作为完整值存在
                            for csv_val in csv_values:
                                if field_value == csv_val:
                                    field_found = True
                                    break
                            # 2. 如果不是完整值，再检查是否是子字符串
                            if not field_found and field_value in csv_data_str:
                                field_found = True
                            
                            if field_found:
                                found_fields.append(f"字段{i}: {field_value}")
                            else:
                                missing_fields.append(f"字段{i}: {field_value}")
                    
                    # 记录验证结果
                    field_verification_status = len(missing_fields) == 0
                    verification_success = verification_success and field_verification_status
                    
                    # 在每个事件的独立步骤中添加验证结果信息
                    allure.attach(f"验证状态: {'通过' if field_verification_status else '失败'}", "验证结果", allure.attachment_type.TEXT)
                    allure.attach(f"验证字段总数: {len(found_fields) + len(missing_fields)}", "验证统计", allure.attachment_type.TEXT)
                    allure.attach(f"找到字段数: {len(found_fields)}", "验证统计", allure.attachment_type.TEXT)
                    allure.attach(f"缺失字段数: {len(missing_fields)}", "验证统计", allure.attachment_type.TEXT)
                    
                    # 总是添加找到的字段和缺失的字段，即使为空
                    found_fields_str = "\n".join(found_fields) if found_fields else "无"
                    missing_fields_str = "\n".join(missing_fields) if missing_fields else "无"
                    
                    allure.attach(found_fields_str, "找到的字段", allure.attachment_type.TEXT)
                    allure.attach(missing_fields_str, "缺失的字段", allure.attachment_type.TEXT)
                    
                    # 构建字段验证结果报告
                    field_verification_report = {
                        'event_id': event_id,
                        'timestamp': timestamp,
                        'status': '通过' if field_verification_status else '失败',
                        'missing_fields': missing_fields,
                        'found_fields': found_fields,
                        'total_fields_verified': len(found_fields) + len(missing_fields)
                    }
                    data_field_verification_results.append(field_verification_report)
                
                # 构建详细的报告内容，包含所有数据字段
                report_content = (
                    f"事件ID: {event_id}\n"
                    f"状态: {status}\n"
                    f"时间戳: {timestamp}\n"
                )
                
                # 添加匹配的CSV数据
                if 'matched_csv_data' in event:
                    report_content += f"匹配的CSV数据: {json.dumps(event.get('matched_csv_data', {}), ensure_ascii=False)}\n"
                
                # 如果有data_fields信息，也添加到报告中
                if 'data_fields' in event:
                    data_fields = event.get('data_fields', [])
                    if data_fields:
                        report_content += "提取的数据字段:\n"
                        for i, field in enumerate(data_fields):
                            if field:  # 只显示非空字段
                                report_content += f"  字段{i}: {field}\n"
                
                # 添加数据字段验证结果
                if status == '找到':
                    # 查找对应的字段验证报告
                    field_report = next((r for r in data_field_verification_results if r['event_id'] == event_id), None)
                    if field_report:
                        report_content += f"数据字段验证状态: {field_report['status']}\n"
                        if field_report['missing_fields']:
                            report_content += "未找到的字段:\n"
                            for field in field_report['missing_fields']:
                                report_content += f"  {field}\n"
                        if field_report['found_fields']:
                            report_content += "找到的字段:\n"
                            for field in field_report['found_fields']:
                                report_content += f"  {field}\n"
                
                allure.attach(
                    report_content,
                    name=f"事件_{event_id}_验证结果",
                    attachment_type=allure.attachment_type.TEXT
                )
        
    # 验证结果 - 综合考虑事件匹配和数据字段验证结果
    if 'error' in results:
        assert success and verification_success, f"远程埋点验证失败: {results['error']} (事件记录数: {results.get('event_records_count', 0)})"
    else:
        # 构建错误信息
        error_messages = []
        if not success:
            error_messages.append(f"事件匹配失败: 找到 {results.get('found', 0)} 个事件，未找到 {results.get('not_found', 0)} 个事件")
        
        if not verification_success:
            # 收集数据字段验证失败的事件信息
            failed_events = [r for r in data_field_verification_results if r['status'] == '失败']
            error_messages.append(f"数据字段验证失败: {len(failed_events)} 个事件的数据字段不完整")
            
            # 添加详细的失败字段信息
            for failed_event in failed_events:
                missing_count = len(failed_event['missing_fields'])
                total_fields = failed_event.get('total_fields_verified', 0)
                error_messages.append(f"  事件 {failed_event['event_id']} (时间戳: {failed_event['timestamp']}) 缺少 {missing_count}/{total_fields} 个字段")
                # 添加具体缺少的字段信息
                for missing_field in failed_event['missing_fields']:
                    error_messages.append(f"    - {missing_field}")
        
        # 执行断言
        analytics_test.log_utils.analytics_logger.info(f"验证完成，success={success}, verification_success={verification_success}")
        assert success and verification_success, "\n".join(error_messages)
    
    return success and verification_success, results



import csv
import glob

def verify_csv_results(analytics_test, compare_column=23):
    """
    验证备份CSV文件中第一列和指定列的组合是否有重复
    只有当第一列（时间戳）和指定的第X列都相同时，才认为是重复上报
    
    Args:
        analytics_test: 分析测试对象
        compare_column: 要对比的列索引（从0开始计数，默认为1表示第二列）
    
    Returns:
        bool: True表示测试通过，False表示测试失败
    """
    # 简化路径计算，直接使用项目根目录
    # 1. 获取当前文件的绝对路径
    current_file = os.path.abspath(__file__)
    analytics_test.log_utils.analytics_logger.info(f"当前文件路径: {current_file}")
    
    # 2. 计算项目根目录 - 从当前文件向上四级目录（修复路径层级错误）
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file))))
    analytics_test.log_utils.analytics_logger.info(f"计算得到的项目根目录: {project_root}")
    
    # 3. 构建logs目录路径
    logs_dir = os.path.join(project_root, 'logs')
    analytics_test.log_utils.analytics_logger.info(f"logs目录路径: {logs_dir}")
    
    # 4. 检查logs目录是否存在
    if os.path.exists(logs_dir):
        analytics_test.log_utils.analytics_logger.info(f"logs目录存在: {logs_dir}")
        # 列出目录内容，帮助调试
        try:
            dir_contents = os.listdir(logs_dir)
            analytics_test.log_utils.analytics_logger.info(f"logs目录内容: {dir_contents}")
        except Exception as e:
            analytics_test.log_utils.analytics_logger.error(f"无法读取logs目录内容: {str(e)}")
    else:
        analytics_test.log_utils.analytics_logger.error(f"logs目录不存在: {logs_dir}")
    
    # 5. 查找CSV文件，使用更宽松的匹配模式
    csv_pattern = os.path.join(logs_dir, 'analytics_backup*.csv')  # 去掉下划线，更宽松的匹配
    analytics_test.log_utils.analytics_logger.info(f"使用的文件匹配模式: {csv_pattern}")
    
    try:
        csv_files = glob.glob(csv_pattern)
        analytics_test.log_utils.analytics_logger.info(f"找到的CSV文件数量: {len(csv_files)}")
        if csv_files:
            analytics_test.log_utils.analytics_logger.info(f"找到的CSV文件列表: {csv_files}")
    except Exception as e:
        analytics_test.log_utils.analytics_logger.error(f"执行文件查找时出错: {str(e)}")
        csv_files = []
    
    if not csv_files:
        error_message = f"在logs目录下未找到任何CSV备份文件: {logs_dir}"
        analytics_test.log_utils.analytics_logger.error(error_message)
        allure.attach(body=error_message, name="CSV文件未找到", attachment_type=allure.attachment_type.TEXT)
        return False
    
    # 按文件名排序，获取最新的文件（假设文件名包含时间戳，格式如analytics_backup_20251107_135221.csv）
    csv_files.sort(reverse=True)
    csv_file_path = csv_files[0]
    
    analytics_test.log_utils.analytics_logger.info(f"找到最新的CSV备份文件: {csv_file_path}")
    
    combination_count = {}
    duplicate_combinations = []
    
    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # 跳过表头并保存表头用于日志
            
            analytics_test.log_utils.analytics_logger.info(f"使用列索引{compare_column}进行对比，列名为：{header[compare_column] if len(header) > compare_column else '未知'}")
            
            for row_idx, row in enumerate(reader, 2):  # 从第2行开始计数
                if row:
                    if len(row) > max(0, compare_column):  # 确保行有足够的列
                        timestamp = row[0]  # 第一列是时间戳
                        compare_value = row[compare_column]  # 指定列的值
                        
                        # 创建组合键
                        combination_key = f"{timestamp}|{compare_value}"
                        
                        if combination_key in combination_count:
                            combination_count[combination_key] += 1
                            if combination_count[combination_key] == 2:  # 第一次发现重复
                                duplicate_combinations.append((timestamp, compare_value, combination_count[combination_key]))
                        else:
                            combination_count[combination_key] = 1
                    else:
                        analytics_test.log_utils.analytics_logger.warning(f"第{row_idx}行数据不足，跳过: {row}")
        
        # 检查是否有重复的组合
        if duplicate_combinations:
            error_message = f"发现{len(duplicate_combinations)}个重复的时间戳和指定列组合:\n"
            for ts, compare_val, count in duplicate_combinations:
                error_message += f"  时间戳: {ts}, 列{compare_column}值: {compare_val}, 出现次数: {count}\n"
            
            analytics_test.log_utils.analytics_logger.error(error_message)
            allure.attach(body=error_message, name="重复组合报告", attachment_type=allure.attachment_type.TEXT)
            return False
        
        analytics_test.log_utils.analytics_logger.info(f"时间戳和列{compare_column}组合唯一性验证通过，未发现重复")
        allure.attach(body=f"所有时间戳和列{compare_column}组合唯一，无重复上报", name="组合验证结果", attachment_type=allure.attachment_type.TEXT)
        return True
        
    except Exception as e:
        error_message = f"验证CSV文件时发生错误: {str(e)}"
        analytics_test.log_utils.analytics_logger.error(error_message)
        allure.attach(body=error_message, name="CSV验证错误", attachment_type=allure.attachment_type.TEXT)
        return False


@allure.feature("大数据日志")
@allure.story("埋点上报唯一性验证")
@pytest.mark.analytics
def test_timestamp_uniqueness_verification(analytics_test, compare_column=23):
    """
    验证备份CSV文件中时间戳和指定列的组合唯一性
    只有当时间戳和指定列都相同时，才认为是重复上报
    
    Args:
        analytics_test: 分析测试对象
        compare_column: 要对比的列索引（从0开始计数，默认为1表示第二列）
    """
    allure.dynamic.title(f"验证埋点上报唯一性（对比列{compare_column}）")
    
    # 调用verify_csv_results函数进行时间戳和指定列组合唯一性验证
    success = verify_csv_results(analytics_test, compare_column)
    
    # 执行断言
    assert success, f"时间戳和列{compare_column}组合唯一性验证失败，存在重复上报的埋点数据"
 