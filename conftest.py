import pytest
from appium_server import AppiumServer
from driver_manager import DriverManager

@pytest.fixture(scope='class')
def appium_server():
    # Appium 서버를 클래스 시작 전에 실행
    server = AppiumServer()
    server.start()
    print(f"Appium 서버가 포트 {server.port}에서 시작되었습니다.")
    yield server
    server.stop()  # 클래스 종료 후 서버 종료

@pytest.fixture(scope='class')
def driver(appium_server):
    # Driver 초기화 (Appium 서버가 실행된 후에 포트를 사용)
    print(f"Appium 서버 포트: {appium_server.port}")
    driver_manager = DriverManager(appium_server.port)
    driver_manager.init_driver()
    yield driver_manager.driver
    driver_manager.quit_driver()  # 클래스 종료 후 드라이버 종료
