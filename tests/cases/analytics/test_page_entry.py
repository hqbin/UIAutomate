import allure
import pytest
import time

wait_time = 10

@allure.feature("进入Home页面埋点")
@allure.story("打开Home页面埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230034(analytics_test):
    # 目标埋点事件ID
    page_entry = "110010004"
    
    with allure.step(f"打开Home页面 [{page_entry}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=page_entry)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(5)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控主页()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=page_entry,
                path_operations=path_operations,
                target_action=last_action,
                path_description="进入Home页面",
                target_description="进入Home页面"
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
            assert success, f"埋点验证失败：未找到事件ID为 {page_entry} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(page_entry)

@allure.feature("进入Apps页面埋点")
@allure.story("打开Apps页面埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230056(analytics_test):
    # 目标埋点事件ID
    page_entry = "110010004"
    
    with allure.step(f"使用遥控打开Apps页面 [{page_entry}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=page_entry)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=page_entry,
                path_operations=path_operations,
                target_action=last_action,
                path_description="进入Apps页面",
                target_description="进入Apps页面"
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
            assert success, f"埋点验证失败：未找到事件ID为 {page_entry} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(page_entry)

@allure.feature("进入Discovery页面埋点")
@allure.story("打开Discovery页面埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230074(analytics_test):
    # 目标埋点事件ID
    page_entry = "110010004"
    
    with allure.step(f"使用遥控打开Discovery页面 [{page_entry}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=page_entry)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=page_entry,
                path_operations=path_operations,
                target_action=last_action,
                path_description="进入Discovery页面",
                target_description="进入Discovery页面"
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
            assert success, f"埋点验证失败：未找到事件ID为 {page_entry} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(page_entry)

@allure.feature("进入FreeTV页面埋点")
@allure.story("打开FreeTV页面埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230097(analytics_test):
    # 目标埋点事件ID
    page_entry = "110010004"
    
    with allure.step(f"使用遥控打开FreeTV页面 [{page_entry}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=page_entry)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(2)

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=page_entry,
                path_operations=path_operations,
                target_action=last_action,
                path_description="进入FreeTV页面",
                target_description="进入FreeTV页面"
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
            assert success, f"埋点验证失败：未找到事件ID为 {page_entry} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(page_entry)

@allure.feature("进入全局Search页面埋点")
@allure.story("打开全局Search页面埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230126(analytics_test):
    # 目标埋点事件ID
    page_entry = "110010004"
    
    with allure.step(f"使用遥控打开全局Search页面 [{page_entry}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=page_entry)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(2)

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控上()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=page_entry,
                path_operations=path_operations,
                target_action=last_action,
                path_description="进入全局Search页面",
                target_description="进入全局Search页面"
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
            assert success, f"埋点验证失败：未找到事件ID为 {page_entry} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(page_entry)