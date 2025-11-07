import allure
import pytest
import time

@allure.feature("distcovery切换TAB埋点")
@allure.story("distcovery切换TAB埋点测试")
@pytest.mark.analytics
def test_STB_FU_PO_2510230075(analytics_test):
    # 目标埋点事件ID
    discovery_cut_tab = "110030004"
    
    with allure.step(f"distcovery切换TAB [{discovery_cut_tab}]"):
        # 设置测试环境
        analytics_test.setup_for_event_test(event_id=discovery_cut_tab)
        
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
                time.sleep(5)
                analytics_test.adb_utils.点击遥控OK()
                time.sleep(3)
                analytics_test.adb_utils.点击遥控上()
                time.sleep(3)


                
            # 构建自定义路径操作序列
            path_operations = [
                (init_path, "初始化路径", {})
            ]
            
            # 定义目标动作函数
            def last_action():
                analytics_test.adb_utils.点击遥控右()
                time.sleep(1)
                analytics_test.adb_utils.点击遥控右()

            # 执行复杂路径操作并验证埋点
            success, events = analytics_test.execute_path_operation_with_analytics(
                event_id=discovery_cut_tab,
                path_operations=path_operations,
                target_action=last_action,
                path_description="distcovery切换TAB",
                target_description="distcovery切换TAB"
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
            assert success, f"埋点验证失败：未找到事件ID为 {discovery_cut_tab} 的触发记录，或时间不匹配"
            assert len(events) > 0, f"埋点验证失败：未找到匹配的事件记录"
            
        finally:
            # 清理测试环境
            try:
                analytics_test.adb_utils.点击遥控主页()
                time.sleep(60)
            except Exception as e:
                analytics_test.log_utils.analytics_logger.warning(f"清理操作失败: {e}")
            finally:
                analytics_test.teardown_event_test(discovery_cut_tab)
