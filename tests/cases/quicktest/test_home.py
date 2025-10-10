
import allure
import time
import pytest
import logging
from utils.adb_utils import get_adb_utils


# 获取logger
handlers = [logging.FileHandler("stb_automation.log"), logging.StreamHandler()]
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', handlers=handlers)
logger = logging.getLogger(__name__)
device = get_adb_utils()

# 测试Search入口功能
@allure.feature("Home")
@allure.story("entrance")
@pytest.mark.smoke
def test_goto_search(test_setup):
    """测试从Home页面进入Search页面"""
    test_dir = test_setup["test_dir"]
    
    with allure.step("步骤1: 按点击遥控Home键到Home页面"):
        logger.info("按Home键")
        device.点击遥控主页()
        time.sleep(2)  # 增加等待时间，确保动作完成
        device.添加截图到allure报告("Home", test_dir=test_dir)
    
    with allure.step("步骤2: 焦点移动到Search入口"):
        logger.info("向左移动焦点")
        device.点击遥控左()
        time.sleep(2)  # 增加等待时间，确保动作完成
        logger.info("向上移动焦点到Search入口")
        device.点击遥控上()
        device.添加截图到allure报告("焦点在Search入口", test_dir=test_dir)
        time.sleep(2)  # 增加等待时间，确保动作完成
        logger.info("点击点击遥控OK键进入Search页面")
        device.点击遥控OK()
        time.sleep(2)  # 增加等待时间，确保动作完成
        device.添加截图到allure报告("Search页面", test_dir=test_dir)
    
    with allure.step("步骤3: 验证进入Search页面"):
        # 验证截图中是否包含Popular Search
        # find_text方法返回布尔值，找到返回True，未找到返回False
        text_found = device.查找文字("Popular Search", test_dir=test_dir)
        logger.info(f"文字查找结果: {text_found}")
        assert text_found, "未能找到Popular Search文本"

# 测试Search搜索功能
@allure.feature("Home")
@allure.story("entrance")
@pytest.mark.test
def test_keyword_search(test_setup):
    """测试Search页面关键字搜索"""
    test_dir = test_setup["test_dir"]
    
    with allure.step("步骤1: 进入Search页面"):
        logger.info("使用adb指令进入Search页面")
        device.启动应用("com.whaletv.launcher","com.zeasn.whaletv.module.home.page.HomeSearchActivity")
        time.sleep(2)  # 增加等待时间，确保动作完成
        device.添加截图到allure报告("Search页面", test_dir=test_dir)
    
    with allure.step("步骤2: 点击遥控OK键激活输入框"):
        logger.info("点击遥控OK键")
        device.点击遥控OK()
        time.sleep(2)  # 增加等待时间，确保动作完成
        device.添加截图到allure报告("激活输入框", test_dir=test_dir)
        time.sleep(2)  # 增加等待时间，确保动作完成
        logger.info("输入搜索关键词")
        device.输入文本("cat")
        time.sleep(2)  # 增加等待时间，确保动作完成
        device.添加截图到allure报告("输入cat关键词", test_dir=test_dir)
        time.sleep(2)  # 增加等待时间，确保动作完成
        device.点击键盘回车()
        time.sleep(2)  # 增加等待时间，确保动作完成
        device.添加截图到allure报告("搜索结果", test_dir=test_dir)
    
    with allure.step("步骤3: 验证进入Search页面"):
        time.sleep(10) 
        device.点击遥控下()
        time.sleep(2)  # 增加等待时间，确保动作完成
        device.添加截图到allure报告("搜索结果", test_dir=test_dir)
        # 验证截图中是否包含Popular Search
        # find_text方法返回布尔值，找到返回True，未找到返回False
        text_found = device.查找文字("cat", test_dir=test_dir)
        logger.info(f"文字查找结果: {text_found}")
        assert text_found, "未能找到cat关键字"