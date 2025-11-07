import allure
import pytest
import time

wait_time = 60

@allure.feature("home打开应用等待1分钟退出埋点")
@allure.story("home打开应用等待1分钟退出埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230048(analytics_test):
    # 目标埋点事件ID
    app_duration = "110100003"
    
    with allure.step(f"home打开应用等待1分钟退出 [{app_duration}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=app_duration)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(3)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控右()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控右()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控右()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(70)
                
            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                pass

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=app_duration,
                path_operations=path_operations,
                target_action=last_action,
                path_description="home打开应用等待1分钟退出",
                target_description="home打开应用等待1分钟退出"
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
            assert success, f"埋点验证失败：未找到事件ID为 {app_duration} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(app_duration)

@allure.feature("apps打开应用等待1分钟退出埋点")
@allure.story("apps打开应用等待1分钟退出埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230058(analytics_test):
    # 目标埋点事件ID
    app_duration = "110100003"
    
    with allure.step(f"apps打开应用等待1分钟退出 [{app_duration}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=app_duration)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(3)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(5)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控右()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控右()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(70)


                
            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                pass

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=app_duration,
                path_operations=path_operations,
                target_action=last_action,
                path_description="apps打开应用等待1分钟退出",
                target_description="apps打开应用等待1分钟退出"
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
            assert success, f"埋点验证失败：未找到事件ID为 {app_duration} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(app_duration)