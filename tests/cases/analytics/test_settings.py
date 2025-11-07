import allure
import pytest
import time

wait_time = 10

@allure.feature("进入Setting页面")
@allure.story("setting 进入Setting页面埋点")
@pytest.mark.analytics
def test_STB_FU_PO_2510230062(analytics_test):
    # 目标埋点事件ID
    setting = "110090001"
    
    with allure.step(f"Setting页面埋点 [{setting}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=setting)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(3)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控OK()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=setting,
                path_operations=path_operations,
                target_action=last_action,
                path_description="进入Setting页面",
                target_description="进入Setting页面"
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
            assert success, f"埋点验证失败：未找到事件ID为 {setting} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(event_id=setting)

@allure.feature("焦点移动到Device Preference")
@allure.story("setting 焦点移动到Device Preference埋点")
@pytest.mark.analytics
def test_STB_FU_PO_2510230063(analytics_test):
    # 目标埋点事件ID
    setting = "110090001"
    
    with allure.step(f"Device Preference埋点 [{setting}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=setting)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(3)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控下()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=setting,
                path_operations=path_operations,
                target_action=last_action,
                path_description="焦点移动到Device Preference",
                target_description="焦点移动到Device Preference"
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
            assert success, f"埋点验证失败：未找到事件ID为 {setting} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(event_id=setting)

@allure.feature("焦点移动到Accessibility")
@allure.story("setting 焦点移动到Accessibility埋点")
@pytest.mark.analytics
def test_STB_FU_PO_2510230064(analytics_test):
    # 目标埋点事件ID
    setting = "110090001"
    
    with allure.step(f"Accessibility埋点 [{setting}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=setting)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(3)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控下()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=setting,
                path_operations=path_operations,
                target_action=last_action,
                path_description="焦点移动到Accessibility",
                target_description="焦点移动到Accessibility"
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
            assert success, f"埋点验证失败：未找到事件ID为 {setting} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(event_id=setting)

@allure.feature("焦点移动到Voice Service")
@allure.story("setting 焦点移动到Voice Service埋点")
@pytest.mark.analytics
def test_STB_FU_PO_2510230065(analytics_test):
    # 目标埋点事件ID
    setting = "110090001"
    
    with allure.step(f"Voice Service埋点 [{setting}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=setting)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(3)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控下()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=setting,
                path_operations=path_operations,
                target_action=last_action,
                path_description="焦点移动到Voice Service",
                target_description="焦点移动到Voice Service"
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
            assert success, f"埋点验证失败：未找到事件ID为 {setting} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(event_id=setting)

@allure.feature("焦点移动到Software Update")
@allure.story("setting 焦点移动到Software Update埋点")
@pytest.mark.analytics
def test_STB_FU_PO_2510230066(analytics_test):
    # 目标埋点事件ID
    setting = "110090001"
    
    with allure.step(f"Software Update埋点 [{setting}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=setting)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(3)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控下()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=setting,
                path_operations=path_operations,
                target_action=last_action,
                path_description="焦点移动到Software Update",
                target_description="焦点移动到Software Update"
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
            assert success, f"埋点验证失败：未找到事件ID为 {setting} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(event_id=setting)

@allure.feature("焦点移动到App Setting")
@allure.story("setting 焦点移动到App Setting埋点")
@pytest.mark.analytics
def test_STB_FU_PO_2510230067(analytics_test):
    # 目标埋点事件ID
    setting = "110090001"
    
    with allure.step(f"App Setting埋点 [{setting}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=setting)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(3)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控下()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=setting,
                path_operations=path_operations,
                target_action=last_action,
                path_description="焦点移动到App Setting",
                target_description="焦点移动到App Setting"
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
            assert success, f"埋点验证失败：未找到事件ID为 {setting} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(event_id=setting)

@allure.feature("焦点移动到Display&Sound")
@allure.story("setting 焦点移动到Display&Sound埋点")
@pytest.mark.analytics
def test_STB_FU_PO_2510230069(analytics_test):
    # 目标埋点事件ID
    setting = "110090001"
    
    with allure.step(f"Display&Sound Setting埋点 [{setting}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=setting)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(3)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控下()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=setting,
                path_operations=path_operations,
                target_action=last_action,
                path_description="焦点移动到Display&Sound",
                target_description="焦点移动到Display&Sound"
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
            assert success, f"埋点验证失败：未找到事件ID为 {setting} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(event_id=setting)

@allure.feature("焦点移动到Network&Connection")
@allure.story("setting 焦点移动到Network&Connection埋点")
@pytest.mark.analytics
def test_STB_FU_PO_2510230070(analytics_test):
    # 目标埋点事件ID
    setting = "110090001"
    
    with allure.step(f"Network&Connection Setting埋点 [{setting}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=setting)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(3)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控OK()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=setting,
                path_operations=path_operations,
                target_action=last_action,
                path_description="焦点移动到Network&Connection",
                target_description="焦点移动到Network&Connection"
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
            assert success, f"埋点验证失败：未找到事件ID为 {setting} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(event_id=setting)

@allure.feature("焦点移动到Hotel Mode")
@allure.story("setting 焦点移动到Hotel Mode埋点")
@pytest.mark.analytics
def test_STB_FU_PO_2510230068(analytics_test):
    # 目标埋点事件ID
    setting = "110090001"
    
    with allure.step(f"Hotel Mode埋点 [{setting}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=setting)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(3)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(1)



            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控下()
                time.sleep(0.5)
                analytics_test.adb_utils.点击遥控右()
                time.sleep(0.5)
                analytics_test.adb_utils.点击遥控上()
                time.sleep(0.5)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(0.5)
                analytics_test.adb_utils.点击遥控上()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=setting,
                path_operations=path_operations,
                target_action=last_action,
                path_description="焦点移动到Hotel Mode",
                target_description="焦点移动到Hotel Mode"
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
            assert success, f"埋点验证失败：未找到事件ID为 {setting} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(wait_time)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(event_id=setting)