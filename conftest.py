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
import time
from appium.webdriver.common.appiumby import AppiumBy

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
def driver(appium_server, os_type, rp_logger, request):
    """
    매 function 마다 driver 선언 및 앱 시작, 종료, 드라이버 종료
    """
    driver_manager = DriverManager(appium_server.port, os_type)
    driver = driver_manager.init_driver()
    execute_method = ExecuteMethod(driver, os_type, rp_logger)
    
    try:
        driver.start_recording_screen(timeLimit=300)
        execute_method.launch_app()
        yield driver
    finally:
        try:
            # 스크린샷 촬영
            take_screenshot_and_log(driver, os_type, rp_logger, request.node)
        except Exception as e:
            rp_logger.error(f"스크린샷 촬영 실패: {e}")

        try:
            # 비디오 저장
            video = driver.stop_recording_screen()
            save_video(video, rp_logger)
        except Exception as e:
            rp_logger.error(f"비디오 저장 실패: {e}")

        try:
            # 앱 종료
            execute_method.terminate_app()
        except Exception as e:
            rp_logger.error(f"앱 종료 실패: {e}")

        try:
            # 드라이버 종료
            driver_manager.quit_driver()
        except Exception as e:
            rp_logger.error(f"드라이버 종료 실패: {e}")

        # 세션이 완전히 종료될 때까지 대기
        time.sleep(2)

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
    try:
        screenshot_name = f"screenshot_{os_type}_{item.name}.png"
        screenshot = driver.get_screenshot_as_png()
        rp_logger.info("스크린샷 확인", extra={"attachment":{
            'name': screenshot_name,
            'data': screenshot,
            'mime': 'image/png'
        }})
    except Exception as e:
        rp_logger.error(f"스크린샷 촬영 중 오류 발생: {e}")

def save_video(video_data, rp_logger):
    try:
        video_bytes = base64.b64decode(video_data)
        rp_logger.info("테스트 영상", extra= {"attachment" :{
            'name': "test_video.mp4",
            'data': video_bytes,
            'mime': 'video/mp4'
        }})
    except Exception as e:
        rp_logger.error(f"비디오 저장 중 오류 발생: {e}")
