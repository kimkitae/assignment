import base64
import os
from io import BytesIO
from PIL import Image
import pytest
import logging
from reportportal_client import RPLogHandler
from appium_server import AppiumServer
from driver_manager import DriverManager
from helper.execute_method import ExecuteMethod
from reportportal_client import RPLogger


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
    driver.start_recording_screen(timeLimit=300, video_quality="low")
    execute_method.launch_app()
    yield driver
    save_video(driver.stop_recording_screen(), rp_logger)
    execute_method.terminate_app()
    driver_manager.quit_driver()

@pytest.fixture(scope="session")
def rp_logger(request):
    """
    매 세션 마다 로그 서러정 및 reportPortal 로그 핸들 설정
    """
    # 기본 로거 설정
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logging.setLoggerClass(RPLogger)

    # python-dotenv의 WARNING 로그를 ERROR 이상으로만 출력되도록 설정
    logging.getLogger("dotenv.main").setLevel(logging.ERROR)
    # urllib3의 WARNING 로그를 ERROR 이상으로만 출력되도록 설정
    logging.getLogger("urllib3.connectionpool").setLevel(logging.ERROR)

    return logger


def take_screenshot_and_log(driver, os_type, rp_logger, item):
    """
    스크린샷 찍기 및 ReportPortal로 로그와 함께 전송
    """
    screenshot_name = f"screenshot_{os_type}_{item.name}.png"
    screenshot = driver.get_screenshot_as_png()

    rp_logger.info("스크린샷 확인:", attachment={
        'name': screenshot_name,
        'data': screenshot,
        'mime': 'image/png'
    })





@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call): 
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed or rep.passed:
        try:
            driver = item.funcargs['driver']
            os_type = item.funcargs['os_type']
            rp_logger = item.funcargs['rp_logger']
            take_screenshot_and_log(driver, os_type, rp_logger, item)

        except Exception as e:
            if "rp_logger" in item.funcargs:
                item.funcargs["rp_logger"].info(f"Failed to take screenshot: {e}")


def save_video(stop_recording_screen, rp_logger):
    """
    화면 녹화 종료 및 ReportPortal로 전송
    """

    video_data = base64.b64decode(stop_recording_screen)
    rp_logger.info("테스트 영상:", attachment={
        'name': "temp.mp4",
        'data': video_data,
        'mime': 'video/mpeg'
    })