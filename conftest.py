import pytest
import logging
from reportportal_client import RPLogHandler
from appium_server import AppiumServer
from driver_manager import DriverManager
from helper.execute_method import ExecuteMethod


"""
Pytest의 Fixture 및 기본 파일
"""

def pytest_addoption(parser):
    """
    추가 파라미터 설정
    --os= 값 없는 경우 기본 ios 동작
    """
    parser.addoption("--os", action="store", default="ios", help="Select OS: ios or android")

@pytest.fixture(scope="session")
def os_type(request):
    """
    매 세션 마다 os_type를 위한 fixture
    """
    return request.config.getoption("--os")

@pytest.fixture(scope="session")
def appium_server():
    """
        매 세션 마다 os_type를 위한 fixture
        """

    server = AppiumServer()
    server.start()
    yield server
    server.stop()

@pytest.fixture(scope="function")
def driver(appium_server, os_type, rp_logger):
    """
    매 function 마다 driver 선언 및 앱 시작, 종료, 드라이버 종료
    """
    driver_manager = DriverManager(appium_server.port, os_type)
    driver = driver_manager.init_driver()
    execute_method = ExecuteMethod(driver, os_type, rp_logger)
    execute_method.launch_app()
    yield driver
    execute_method.terminate_app()
    driver_manager.quit_driver()

@pytest.fixture(scope="session")
def rp_logger():
    """
    매 세션 마다 로그 서러정 및 reportPortal 로그 핸들 설정
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    rp_handler = RPLogHandler()
    rp_handler.setLevel(logging.INFO)
    logger.addHandler(rp_handler)
    
    return logger