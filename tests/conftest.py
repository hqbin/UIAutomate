import pytest
import os
import allure
from datetime import datetime
import logging
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入自定义工具
from utils.adb_utils import get_adb_utils
from utils.image_recognition import get_image_recognition

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("stb_automation.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 自定义标记注册
# 这些标记可以在测试用例中使用@pytest.mark.xxx来标记测试用例
# 然后使用pytest -m xxx来运行特定标记的测试
# 注册的标记会在pytest --markers中显示
def pytest_configure(config):
    """注册自定义标记"""
    
    # 页面相关标记
    config.addinivalue_line(
        "markers", "Home: 测试Home页面相关功能"
    )
    # 测试类型标记
    config.addinivalue_line(
        "markers", "smoke: 冒烟测试用例"
    )
    # 页面相关标记
    config.addinivalue_line(
        "markers", "test: 测试使用"
    )

# Fixture: 获取ADB工具实例
@pytest.fixture(scope="session")
def adb_utils():
    """提供ADB工具实例，会话级别，整个测试会话只初始化一次"""
    logger.info("初始化ADB工具...")
    adb = get_adb_utils()
    try:
        # 检查设备连接
        device_info = adb.获取设备信息()
        logger.info(f"设备信息: {device_info}")
        yield adb
    except Exception as e:
        logger.error(f"ADB工具初始化失败: {e}")
        pytest.skip(f"ADB设备未连接或初始化失败: {e}")
    finally:
        logger.info("ADB工具会话结束")

# Fixture: 获取图像识别工具实例
@pytest.fixture(scope="session")
def image_recognition(adb_utils):
    """提供图像识别工具实例，会话级别"""
    logger.info("初始化图像识别工具...")
    try:
        # 使用image_recognition模块中已实现的自动检测机制
        ocr = get_image_recognition(adb_utils=adb_utils)
        logger.info("图像识别工具初始化成功")
        yield ocr
    except Exception as e:
        logger.error(f"图像识别工具初始化失败: {e}")
        pytest.skip(f"图像识别工具初始化失败: {e}")
    finally:
        logger.info("图像识别工具会话结束")

# Fixture: 测试用例执行前的准备
@pytest.fixture(scope="function")
def test_setup(adb_utils, image_recognition, request):
    """每个测试函数执行前的设置"""
    test_name = request.node.name
    logger.info(f"开始执行测试: {test_name}")
    
    # 创建测试结果目录
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_dir = os.path.join("tests", "reports", f"{test_name}_{timestamp}")
    os.makedirs(test_dir, exist_ok=True)
    
    # 记录测试开始时间
    start_time = datetime.now()
    
    # 添加测试环境信息到allure报告
    with allure.step("测试环境准备"):
        device_info = adb_utils.获取设备信息()
        allure.attach(str(device_info), name="设备信息", attachment_type=allure.attachment_type.TEXT)
        
    # 返回测试上下文
    context = {
        "adb": adb_utils,
        "test_name": test_name,
        "test_dir": test_dir,
        "start_time": start_time
    }
    
    yield context
    
    # 测试结束后的清理
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    logger.info(f"测试 {test_name} 执行完成，耗时: {duration:.2f}秒")

# Hook函数: 在测试失败时截图
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """在测试失败时自动截图"""
    outcome = yield
    report = outcome.get_result()
    
    # 只在测试失败时截图
    if report.when == "call" and report.failed:
        # 获取测试上下文
        if hasattr(item, "funcargs") and "test_setup" in item.funcargs:
            context = item.funcargs["test_setup"]
            adb = context["adb"]
            test_dir = context["test_dir"]
            
            try:
                # 截取设备屏幕
                screenshot_path = os.path.join(test_dir, "failure_screenshot.png")
                adb.截图(screenshot_path)
                
                # 添加截图到allure报告
                with open(screenshot_path, "rb") as f:
                    allure.attach(f.read(), name="失败截图", attachment_type=allure.attachment_type.PNG)
                
                logger.info(f"测试失败，已保存截图到: {screenshot_path}")
            except Exception as e:
                logger.error(f"保存失败截图时出错: {e}")