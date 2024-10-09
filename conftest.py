import pytest
import allure
import os
from appium import webdriver
from appium_server import AppiumServer
from driver_manager import DriverManager
from page.execute_method import ExecuteMethod

@pytest.fixture(scope="session")
def appium_server():
    server = AppiumServer()
    server.start()
    yield server
    server.stop()

@pytest.fixture(scope="function")
def driver(appium_server):
    driver_manager = DriverManager(appium_server.port)
    driver = driver_manager.init_driver()
    execute_method = ExecuteMethod(driver)
    execute_method.launch_app()
    yield driver
    execute_method.terminate_app()
    driver_manager.quit_driver()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        mode = 'a' if os.path.exists('failures') else 'w'
        try:
            with open('failures', mode) as f:
                if 'driver' in item.fixturenames:
                    web_driver = item.funcargs['driver']
                    allure.attach(
                        web_driver.get_screenshot_as_png(),
                        name='screenshot',
                        attachment_type=allure.attachment_type.PNG
                    )
        except Exception as e:
            print('Fail to take screenshot: {}'.format(e))