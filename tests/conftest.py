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
from utils.log_utils import get_log_utils
from utils.analytics_test_base import AnalyticsTestBase

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
    # 埋点测试标记
    config.addinivalue_line(
        "markers", "analytics: 数据埋点测试用例"
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

# Fixture: 设置设备时区为上海
@pytest.fixture(scope="session", autouse=True)
def set_device_timezone(adb_utils):
    """设置设备时区为亚洲/上海，在整个测试会话开始时自动执行一次"""
    logger.info("设置设备时区为Asia/Shanghai...")
    try:
        adb_utils._run_adb_command(["shell", "setprop", "persist.sys.timezone", "Asia/Shanghai"])
        # 执行adb指令设置时区
        result = adb_utils._run_adb_command(["shell", "setprop", "persist.sys.timezone", "Asia/Shanghai"])
        logger.info(f"时区设置结果: {result}")
        # 验证时区设置是否成功
        verify_result = adb_utils._run_adb_command(["shell", "getprop", "persist.sys.timezone"])
        logger.info(f"当前设备时区: {verify_result.strip()}")
    except Exception as e:
        logger.error(f"设置设备时区失败: {e}")

# Fixture: 捕获logcat日志
@pytest.fixture(scope="session", autouse=True)
def capture_logcat(adb_utils):
    """在测试会话开始时捕获logcat日志，测试结束后停止捕获"""
    import subprocess
    import os
    import time
    adb_utils._run_adb_command(["root"])
    
    # 确保logs目录存在
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
    os.makedirs(logs_dir, exist_ok=True)
    
    # 生成日志文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(logs_dir, f"all_log_{timestamp}.txt")
    
    logger.info(f"开始捕获logcat日志到文件: {log_file}")
    
    # 清除之前的logcat缓存
    try:
        adb_utils._run_adb_command(["logcat", "-c"])
    except Exception as e:
        logger.warning(f"清除logcat缓存失败: {e}")
    
    # 启动logcat捕获进程
    logcat_process = None
    try:
        # 使用subprocess启动logcat进程并将输出重定向到文件
        cmd = ["adb", "logcat"]
        logcat_process = subprocess.Popen(
            cmd,
            stdout=open(log_file, "w", encoding="utf-8"),
            stderr=subprocess.STDOUT,
            text=True
        )
        logger.info(f"logcat进程已启动，PID: {logcat_process.pid}")
        
        # 等待一段时间确保logcat正常启动
        time.sleep(1)
        
        # 提供日志文件路径给测试
        yield log_file
        
    except Exception as e:
        logger.error(f"启动logcat捕获失败: {e}")
        yield None
    finally:
        # 测试会话结束后停止logcat捕获
        if logcat_process:
            try:
                logger.info("停止logcat捕获...")
                # 终止logcat进程
                logcat_process.terminate()
                # 等待进程结束，最多等待5秒
                logcat_process.wait(timeout=5)
                logger.info(f"logcat进程已停止，日志文件: {log_file}")
                
                # 检查文件大小
                if os.path.exists(log_file):
                    file_size = os.path.getsize(log_file) / 1024  # KB
                    logger.info(f"日志文件大小: {file_size:.2f} KB")
                else:
                    logger.warning(f"日志文件不存在: {log_file}")
                    
            except subprocess.TimeoutExpired:
                logger.warning("logcat进程终止超时，强制杀死...")
                logcat_process.kill()
            except Exception as e:
                logger.error(f"停止logcat进程时出错: {e}")

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

# Fixture: 获取日志工具实例
@pytest.fixture(scope="session")
def log_utils(adb_utils):
    """提供日志工具实例，会话级别"""
    logger.info("初始化日志工具...")
    try:
        log = get_log_utils(adb_utils)
        logger.info("日志工具初始化成功")
        yield log
    except Exception as e:
        logger.error(f"日志工具初始化失败: {e}")
        pytest.skip(f"日志工具初始化失败: {e}")
    finally:
        logger.info("日志工具会话结束")

# Fixture: 埋点测试基类实例
@pytest.fixture(scope="function")
def analytics_test(adb_utils, log_utils, test_setup):
    """提供埋点测试基类实例，函数级别"""
    logger.info("初始化埋点测试基类...")
    try:
        test_base = AnalyticsTestBase(adb_utils, log_utils, test_setup)
        logger.info("埋点测试基类初始化成功")
        yield test_base
    except Exception as e:
        logger.error(f"埋点测试基类初始化失败: {e}")
        pytest.skip(f"埋点测试基类初始化失败: {e}")
    finally:
        logger.info("埋点测试基类会话结束")

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

# Hook函数: 修改测试用例执行顺序
def pytest_collection_modifyitems(items):
    """
    修改测试用例执行顺序，确保:
    1. test_remote_hotkey.py 中的测试用例最先执行
    2. test_z_verification.py 中的测试用例最后执行
    3. 其他测试用例保持原来的相对顺序
    """
    # 初始化不同类型的测试列表
    remote_hotkey_tests = []
    z_verification_tests = []
    other_tests = []
    
    # 遍历所有测试用例，按照文件名分类
    for item in items:
        module_path = item.location[0]  # 获取测试模块的路径
        
        if 'test_remote_hotkey' in module_path:
            remote_hotkey_tests.append(item)
        elif 'test_z_verification' in module_path:
            z_verification_tests.append(item)
        else:
            other_tests.append(item)
    
    # 重新组织测试执行顺序
    items.clear()
    items.extend(remote_hotkey_tests)  # 先执行remote_hotkey测试
    items.extend(other_tests)          # 然后执行其他测试
    items.extend(z_verification_tests) # 最后执行z_verification测试
    
    # 记录测试执行顺序
    logger.info("测试用例执行顺序已调整:")
    for i, item in enumerate(items, 1):
        logger.info(f"{i}. {item.location[0]}::{item.name}")