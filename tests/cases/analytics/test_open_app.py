import allure
import pytest
import time


@allure.feature("从home页进入其他page页埋点")
@allure.story("从home页进入其他page页埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230032(analytics_test):
    # 目标埋点事件ID
    open_app = "110010003"
    
    with allure.step(f"从home页进入其他page页 [{open_app}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=open_app)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(130)
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
                analytics_test.adb_utils.点击遥控OK()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=open_app,
                path_operations=path_operations,
                target_action=last_action,
                path_description="从home页进入其他page页",
                target_description="从home页进入其他page页"
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
            assert success, f"埋点验证失败：未找到事件ID为 {open_app} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(60)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(open_app)

@allure.feature("从home页进入第三方应用埋点")
@allure.story("从home页进入第三方应用埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230033(analytics_test):
    # 目标埋点事件ID
    open_app = "110010003"
    
    with allure.step(f"从home页进入其他page页 [{open_app}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=open_app)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(70)
                analytics_test.adb_utils.点击遥控下()
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
                event_id=open_app,
                path_operations=path_operations,
                target_action=last_action,
                path_description="从home页进入第三方应用",
                target_description="从home页进入第三方应用"
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
            assert success, f"埋点验证失败：未找到事件ID为 {open_app} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(60)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(open_app)

@allure.feature("退出Apps页面埋点")
@allure.story("退出Apps页面埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230055(analytics_test):
    # 目标埋点事件ID
    open_app = "110010003"
    
    with allure.step(f"退出Apps页面 [{open_app}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=open_app)
        
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
                analytics_test.adb_utils.点击遥控下()
                time.sleep(5)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(70)

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控主页()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=open_app,
                path_operations=path_operations,
                target_action=last_action,
                path_description="退出Apps页面",
                target_description="退出Apps页面"
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
            assert success, f"埋点验证失败：未找到事件ID为 {open_app} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(60)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(open_app)

@allure.feature("退出Discovery页面埋点")
@allure.story("退出Discovery页面埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230073(analytics_test):
    # 目标埋点事件ID
    open_app = "110010003"
    
    with allure.step(f"退出Discovery页面 [{open_app}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=open_app)
        
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
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(60)

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控主页()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=open_app,
                path_operations=path_operations,
                target_action=last_action,
                path_description="退出Discovery页面",
                target_description="退出Discovery页面"
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
            assert success, f"埋点验证失败：未找到事件ID为 {open_app} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(60)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(open_app)

@allure.feature("退出Free TV页面埋点")
@allure.story("退出Free TV页面埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230096(analytics_test):
    # 目标埋点事件ID
    open_app = "110010003"
    
    with allure.step(f"退出Free TV页面 [{open_app}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=open_app)
        
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
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(60)

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控主页()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=open_app,
                path_operations=path_operations,
                target_action=last_action,
                path_description="退出Free TV页面",
                target_description="退出Free TV页面"
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
            assert success, f"埋点验证失败：未找到事件ID为 {open_app} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(60)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(open_app)

@allure.feature("退出Free TV页面埋点")
@allure.story("退出Free TV页面埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230101(analytics_test):
    # 目标埋点事件ID
    open_app = "110010003"
    
    with allure.step(f"退出Free TV页面 [{open_app}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=open_app)
        
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
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(60)

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控主页()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=open_app,
                path_operations=path_operations,
                target_action=last_action,
                path_description="退出Free TV页面",
                target_description="退出Free TV页面"
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
            assert success, f"埋点验证失败：未找到事件ID为 {open_app} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(60)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(open_app)

@allure.feature("离开free TV埋点")
@allure.story("离开Free TV页面埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230102(analytics_test):
    # 目标埋点事件ID
    open_app = "110010003"
    
    with allure.step(f"离开free TV [{open_app}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=open_app)
        
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
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(5)

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控主页()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=open_app,
                path_operations=path_operations,
                target_action=last_action,
                path_description="离开Free TV页面",
                target_description="离开Free TV页面"
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
            assert success, f"埋点验证失败：未找到事件ID为 {open_app} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(60)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(open_app)

@allure.feature("退出全局Search页面埋点")
@allure.story("退出全局Search页面埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230125(analytics_test):
    # 目标埋点事件ID
    open_app = "110010003"
    
    with allure.step(f"退出全局Search页面 [{open_app}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=open_app)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控上()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(60)

            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控主页()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=open_app,
                path_operations=path_operations,
                target_action=last_action,
                path_description="退出全局Search页面",
                target_description="退出全局Search页面"
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
            assert success, f"埋点验证失败：未找到事件ID为 {open_app} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(60)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(open_app)