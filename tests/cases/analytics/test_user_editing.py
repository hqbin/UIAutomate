import allure
import pytest
import time

wait_time = 10

@allure.feature("用户编辑后返回埋点")
@allure.story("用户编辑后返回埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230118(analytics_test):
    # 目标埋点事件ID
    user_editing = "110110010"
    
    with allure.step(f"用户编辑后返回 [{user_editing}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=user_editing)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(5)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控上()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控上()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控返回()
                time.sleep(2)
            
            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控OK()
            
            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=user_editing,
                path_operations=path_operations,
                target_action=last_action,
                path_description="用户编辑后返回",
                target_description="用户编辑后返回"
            )
            
            # 记录测试结果
            test_passed = not success and len(events) == 0
            allure.attach(
                f"自定义操作测试结果: {'成功' if test_passed else '失败'}\n"  
                f"操作序列步骤: {len(path_operations)}\n"  
                f"匹配事件数: {len(events)}\n"  
                f"验证目标: 未找到埋点事件则判定成功",
                name="测试结果",
                attachment_type=allure.attachment_type.TEXT
            )
            
            # 使用allure动态标签标记测试结果
            allure.dynamic.label('status', 'passed' if test_passed else 'failed')
            
            # 添加断言，确保在未找到埋点事件时测试成功
            assert test_passed, f"埋点验证失败：{'找到事件ID为 ' + user_editing + ' 的触发记录' if success else f'找到 {len(events)} 条匹配的事件记录'}"
            
        finally:
            # 清理测试环境
            try:
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(user_editing)

@allure.feature("用户编辑埋点")
@allure.story("用户编辑埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230119(analytics_test):
    # 目标埋点事件ID
    user_editing = "110110010"
    
    with allure.step(f"用户编辑 [{user_editing}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=user_editing) 
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(5)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控上()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控上()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控返回()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控右()
                time.sleep(2)

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控OK()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=user_editing,
                path_operations=path_operations,
                target_action=last_action,
                path_description="用户编辑",
                target_description="用户编辑"
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
            assert success, f"埋点验证失败：未找到事件ID为 {user_editing} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(user_editing)
