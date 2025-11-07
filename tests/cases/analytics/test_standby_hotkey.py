import allure
import pytest
import time

wait_time = 10

@allure.feature("设备待机")
@allure.story("standby_hotkey 设备待机埋点")
@pytest.mark.analytics
def test_STB_FU_PO_2510230019(analytics_test):
    # 目标埋点事件ID
    standby_hotkey = "110100005"
    
    with allure.step(f"设备待机 [{standby_hotkey}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=standby_hotkey)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(2)
                

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控Power()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=standby_hotkey,
                path_operations=path_operations,
                target_action=last_action,
                path_description="设备待机",
                target_description="设备待机"
            )
            
            # 记录测试结果
            allure.attach(
                f"自定义操作测试结果: {'成功' if success else '失败'}\n"  
                f"操作序列步骤: {len(path_operations)}\n"  
                f"匹配事件数: {len(events)}",
                name="测试结果",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # 添加断言，确保在未找到埋点事件时测试失败
            assert success, f"埋点验证失败：未找到事件ID为 {standby_hotkey} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(standby_hotkey)

@allure.feature("设备开机")
@allure.story("standby_hotkey 设备开机埋点")
@pytest.mark.analytics
def test_STB_FU_PO_2510230018(analytics_test):
    # 目标埋点事件ID
    standby_hotkey = "110100005"
    
    with allure.step(f"设备开机 [{standby_hotkey}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=standby_hotkey)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(2)
                

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控Power()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=standby_hotkey,
                path_operations=path_operations,
                target_action=last_action,
                path_description="设备开机",
                target_description="设备开机"
            )
            
            # 记录测试结果
            allure.attach(
                f"自定义操作测试结果: {'成功' if success else '失败'}\n"  
                f"操作序列步骤: {len(path_operations)}\n"  
                f"匹配事件数: {len(events)}",
                name="测试结果",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # 添加断言，确保在未找到埋点事件时测试失败
            assert success, f"埋点验证失败：未找到事件ID为 {standby_hotkey} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(standby_hotkey)

@allure.feature("Netflix唤醒")
@allure.story("standby_hotkey Netflix唤醒埋点")
@pytest.mark.analytics
def test_STB_FU_PO_2510230020(analytics_test):
    # 目标埋点事件ID
    standby_hotkey = "110100005"
    
    with allure.step(f"Netflix唤醒 [{standby_hotkey}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=standby_hotkey)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控Power()
                time.sleep(2)
                

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控Netflix热键()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=standby_hotkey,
                path_operations=path_operations,
                target_action=last_action,
                path_description="Netflix唤醒",
                target_description="Netflix唤醒"
            )
            
            # 记录测试结果
            allure.attach(
                f"自定义操作测试结果: {'成功' if success else '失败'}\n"  
                f"操作序列步骤: {len(path_operations)}\n"  
                f"匹配事件数: {len(events)}",
                name="测试结果",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # 添加断言，确保在未找到埋点事件时测试失败
            assert success, f"埋点验证失败：未找到事件ID为 {standby_hotkey} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(standby_hotkey)

@allure.feature("SleepTimer待机")
@allure.story("standby_hotkey SleepTimer待机埋点")
@pytest.mark.analytics
def test_STB_FU_PO_2510230021(analytics_test):
    # 目标埋点事件ID
    standby_hotkey = "110100005"
    
    with allure.step(f"设备待机 [{standby_hotkey}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=standby_hotkey)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(2)
                analytics_test.adb_utils.打开PID菜单()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控右()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控右()
                time.sleep(430)

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控Power()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=standby_hotkey,
                path_operations=path_operations,
                target_action=last_action,
                path_description="设备待机",
                target_description="设备待机"
            )
            
            # 记录测试结果
            allure.attach(
                f"自定义操作测试结果: {'成功' if success else '失败'}\n"  
                f"操作序列步骤: {len(path_operations)}\n"  
                f"匹配事件数: {len(events)}",
                name="测试结果",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # 添加断言，确保在未找到埋点事件时测试失败
            assert success, f"埋点验证失败：未找到事件ID为 {standby_hotkey} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(standby_hotkey)