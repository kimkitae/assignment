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
