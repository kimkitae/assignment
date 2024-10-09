import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput


class ElementInteractionHandler:
    def __init__(self, driver):
        self.driver = driver

    def click_on(self, test_object, wait_time=1.5):
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(test_object)
            )
            element.click()
        except TimeoutException:
            raise Exception(f"{test_object} 오브젝트를 찾지 못함")
        except IndexError:
            raise Exception("입력한 index의 오브젝트가 존재하지 않습니다. Index 번호를 다시 한번 확인해주세요.")

    @staticmethod
    def tap_xy(x, y):
        actions = ActionChains(driver)
        finger = PointerInput(interaction.POINTER_TOUCH, "finger")
        actions.w3c_actions = ActionBuilder(driver, mouse=finger)
        actions.w3c_actions.pointer_action.move_to_location(x, y)
        actions.w3c_actions.pointer_action.click()
        actions.w3c_actions.perform()
        print(f"좌표 - {x} / {y}")

    @staticmethod
    def tap_test_object_xy(test_object, wait_time=3):
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located(test_object)
            )
            location = element.location
            size = element.size
            center_x = location['x'] + size['width'] // 2
            center_y = location['y'] + size['height'] // 2
            ElementInteractionHandler.tap_xy(center_x, center_y)
        except TimeoutException:
            raise Exception(f"{test_object} 오브젝트를 찾지 못함")

    @staticmethod
    def set_text(text_value, test_object, wait_time=1.5):
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located(test_object)
            )
            element.send_keys(text_value)
        except TimeoutException:
            raise Exception(f"{test_object} 오브젝트를 찾지 못함")

    @staticmethod
    def get_text(test_object, wait_time=3):
        try:
            element = WebDriverWait(driver, wait_time).until(
                EC.presence_of_element_located(test_object)
            )
            result = element.text
            print(result)
            return result
        except TimeoutException:
            raise Exception(f"{test_object} 오브젝트를 찾지 못함")

    @staticmethod
    def clean_text_field(element_type, wait_time=3):
        try:
            if element_type == "TEXT_FIELD":
                element = WebDriverWait(driver, wait_time).until(
                    EC.presence_of_element_located((AppiumBy.CLASS_NAME, "XCUIElementTypeTextField"))
                )
            elif element_type == "SECURE_TEXT_FIELD":
                element = WebDriverWait(driver, wait_time).until(
                    EC.presence_of_element_located((AppiumBy.CLASS_NAME, "XCUIElementTypeSecureTextField"))
                )
            else:
                raise ValueError("Invalid element_type")
            
            element.clear()
            print(f"{element_type} 클리어")
        except TimeoutException:
            raise Exception(f"{element_type} 오브젝트를 찾지 못함")

    @staticmethod
    def set_permission(permissions):
        permissions["bundleId"] = "com.rgpkorea.enp.yogiyo"
        driver.execute_script("mobile: setPermission", permissions)
