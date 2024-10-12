import pytest
import allure
import os
import logging
from reportportal_client import RPLogger, RPLogHandler
from appium import webdriver
from appium_server import AppiumServer
from driver_manager import DriverManager
from page.execute_method import ExecuteMethod

def pytest_addoption(parser):
    parser.addoption("--os", action="store", default="ios", help="Select OS: ios or android")

@pytest.fixture(scope="session")
def os_type(request):
    return request.config.getoption("--os")

@pytest.fixture(scope="session")
def appium_server():
    server = AppiumServer()
    server.start()
    yield server
    server.stop()

@pytest.fixture(scope="function")
def driver(appium_server, os_type, rp_logger):
    driver_manager = DriverManager(appium_server.port, os_type)
    driver = driver_manager.init_driver()
    execute_method = ExecuteMethod(driver, os_type, rp_logger)
    execute_method.launch_app()
    yield driver
    execute_method.terminate_app()
    driver_manager.quit_driver()

@pytest.fixture(scope="session")
def rp_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    
    rp_handler = RPLogHandler()
    rp_handler.setLevel(logging.INFO)
    logger.addHandler(rp_handler)
    
    return logger