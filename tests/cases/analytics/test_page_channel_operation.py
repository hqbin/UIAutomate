import allure
import pytest
import time


@allure.feature("discovery对影片进行点赞埋点")
@allure.story("discovery对影片进行点赞埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230089(analytics_test):
    # 目标埋点事件ID
    page_channel_operation = "110030013"
    
    with allure.step(f"discovery对影片进行点赞 [{page_channel_operation}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=page_channel_operation)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(5)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(5)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控右()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控右()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控右()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控右()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控左()
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
                event_id=page_channel_operation,
                path_operations=path_operations,
                target_action=last_action,
                path_description="discovery对影片进行点赞",
                target_description="discovery对影片进行点赞"
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
            assert success, f"埋点验证失败：未找到事件ID为 {page_channel_operation} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(60)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(page_channel_operation)

@allure.feature("discovery对影片取消点赞埋点")
@allure.story(" 对影片取消点赞埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230090(analytics_test):
    # 目标埋点事件ID
    page_channel_operation = "110030013"
    
    with allure.step(f"discovery对影片取消点赞 [{page_channel_operation}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=page_channel_operation)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(5)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控右()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控右()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控右()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控右()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控左()
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
                event_id=page_channel_operation,
                path_operations=path_operations,
                target_action=last_action,
                path_description="discovery对影片取消点赞",
                target_description="discovery对影片取消点赞"
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
            assert success, f"埋点验证失败：未找到事件ID为 {page_channel_operation} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(60)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(page_channel_operation)

@allure.feature("freetv对Live Now进行点赞埋点")
@allure.story("freetv对Live Now进行点赞埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230108(analytics_test):
    # 目标埋点事件ID
    page_channel_operation = "110030013"
    
    with allure.step(f"freetv对Live Now进行点赞 [{page_channel_operation}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=page_channel_operation)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(5)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控右()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
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
                event_id=page_channel_operation,
                path_operations=path_operations,
                target_action=last_action,
                path_description="freetv对Live Now进行点赞",
                target_description="freetv对Live Now进行点赞"
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
            assert success, f"埋点验证失败：未找到事件ID为 {page_channel_operation} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(60)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(page_channel_operation)

@allure.feature("freetv对Live Now取消点赞埋点")
@allure.story("freetv对Live Now取消点赞埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230111(analytics_test):
    # 目标埋点事件ID
    page_channel_operation = "110030013"
    
    with allure.step(f"freetv对Live Now取消点赞 [{page_channel_operation}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=page_channel_operation)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(5)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控右()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
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
                event_id=page_channel_operation,
                path_operations=path_operations,
                target_action=last_action,
                path_description="freetv对Live Now取消点赞",
                target_description="freetv对Live Now取消点赞"
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
            assert success, f"埋点验证失败：未找到事件ID为 {page_channel_operation} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(60)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(page_channel_operation)

@allure.feature("freetv对Recommended Channels进行点赞埋点")
@allure.story("freetv对Recommended Channels进行点赞埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230109(analytics_test):
    # 目标埋点事件ID
    page_channel_operation = "110030013"
    
    with allure.step(f"freetv对Recommended Channels进行点赞 [{page_channel_operation}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=page_channel_operation)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(5)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
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
                event_id=page_channel_operation,
                path_operations=path_operations,
                target_action=last_action,
                path_description="freetv对Recommended Channels进行点赞",
                target_description="freetv对Recommended Channels进行点赞"
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
            assert success, f"埋点验证失败：未找到事件ID为 {page_channel_operation} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(60)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(page_channel_operation)

@allure.feature("freetv对Recommended Channels取消点赞埋点")
@allure.story("freetv对Recommended Channels取消点赞埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230112(analytics_test):
    # 目标埋点事件ID
    page_channel_operation = "110030013"
    
    with allure.step(f"freetv对Recommended Channels取消点赞 [{page_channel_operation}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=page_channel_operation)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(5)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
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
                event_id=page_channel_operation,
                path_operations=path_operations,
                target_action=last_action,
                path_description="freetv对Recommended Channels取消点赞",
                target_description="freetv对Recommended Channels取消点赞"
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
            assert success, f"埋点验证失败：未找到事件ID为 {page_channel_operation} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(60)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(page_channel_operation)

@allure.feature("freetv对Trending Movies进行点赞埋点")
@allure.story("freetv对Trending Movies进行点赞埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230110(analytics_test):
    # 目标埋点事件ID
    page_channel_operation = "110030013"
    
    with allure.step(f"freetv对Trending Movies进行点赞 [{page_channel_operation}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=page_channel_operation)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(5)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
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
                event_id=page_channel_operation,
                path_operations=path_operations,
                target_action=last_action,
                path_description="freetv对Trending Movies进行点赞",
                target_description="freetv对Trending Movies进行点赞"
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
            assert success, f"埋点验证失败：未找到事件ID为 {page_channel_operation} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(60)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(page_channel_operation)

@allure.feature("freetv对Trending Movies取消点赞埋点")
@allure.story("freetv对Trending Movies取消点赞埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230111(analytics_test):
    # 目标埋点事件ID
    page_channel_operation = "110030013"
    
    with allure.step(f"freetv对Trending Movies取消点赞 [{page_channel_operation}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=page_channel_operation)
        
        try:
             # 定义自定义操作函数
            def init_path():
                """初始化路径"""
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(5)
                analytics_test.adb_utils.点击遥控左()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控下()
                time.sleep(2)
                analytics_test.adb_utils.点击遥控OK()
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
                event_id=page_channel_operation,
                path_operations=path_operations,
                target_action=last_action,
                path_description="freetv对Trending Movies取消点赞",
                target_description="freetv对Trending Movies取消点赞"
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
            assert success, f"埋点验证失败：未找到事件ID为 {page_channel_operation} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(60)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(page_channel_operation)