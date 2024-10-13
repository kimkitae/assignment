import time
from selenium.webdriver.common.keys import Keys
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput


class ElementInteractionHandler:
    def __init__(self, driver, os_type, rp_logger):
        self.logger = rp_logger
        self.driver = driver
        self.os_type = os_type

    def click_on(self, test_object, wait_time=5):
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.element_to_be_clickable(test_object)
    )
            element.click()
            self.logger.info(f"{test_object} 클릭")
        except TimeoutException:
            self.logger.info(f"{test_object} 오브젝트를 찾지 못함")
            raise Exception(f"{test_object} 오브젝트를 찾지 못함")
        except IndexError:
            self.logger.info("입력한 index의 오브젝트가 존재하지 않습니다. Index 번호를 다시 한번 확인해주세요.")
            raise Exception("입력한 index의 오브젝트가 존재하지 않습니다. Index 번호를 다시 한번 확인해주세요.")

    def tap_xy(self, x, y):
        actions = ActionChains(self.driver)
        finger = PointerInput(interaction.POINTER_TOUCH, "finger")
        actions.w3c_actions = ActionBuilder(self.driver, mouse=finger)
        actions.w3c_actions.pointer_action.move_to_location(x, y)
        actions.w3c_actions.pointer_action.click()
        actions.w3c_actions.perform()
        self.logger.info(f"좌표 - {x} / {y} 클릭")

    def tap_test_object_xy(self, test_object, wait_time=3):
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(test_object)
            )
            location = element.location
            size = element.size
            center_x = location['x'] + size['width'] // 2
            center_y = location['y'] + size['height'] // 2
            self.tap_xy(center_x, center_y)
        except TimeoutException:
            self.logger.info(f"{test_object} 오브젝트를 찾지 못함")
            raise Exception(f"{test_object} 오브젝트를 찾지 못함")

    def set_text(self, test_object, text_value, wait_time=1.5):
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(test_object)
            )

            element.send_keys(text_value)
            self.logger.info(f"{test_object}에 {text_value} 입력")
        except TimeoutException:
            self.logger.info(f"{test_object} 오브젝트를 찾지 못함")
            raise Exception(f"{test_object} 오브젝트를 찾지 못함")

    def get_text(self, test_object, wait_time=3):
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(test_object)
            )
            result = element.text
            self.logger.info(f"{test_object}의 텍스트: {result}")
            return result
        except TimeoutException:
            self.logger.info(f"{test_object} 오브젝트를 찾지 못함")
            raise Exception(f"{test_object} 오브젝트를 찾지 못함")

    def clean_text_field(self, element_type, wait_time=3):
        try:
            if self.os_type == "ios":
                if element_type == "TEXT_FIELD":
                    element = WebDriverWait(self.driver, wait_time).until(
                        EC.presence_of_element_located((AppiumBy.CLASS_NAME, "XCUIElementTypeTextField"))
                    )
                elif element_type == "SECURE_TEXT_FIELD":
                    element = WebDriverWait(self.driver, wait_time).until(
                        EC.presence_of_element_located((AppiumBy.CLASS_NAME, "XCUIElementTypeSecureTextField"))
                    )
                else:
                    self.logger.info("Invalid element_type")
                    raise ValueError("Invalid element_type")
            elif self.os_type == "android":
                # Android에 맞는 로직 추가
                element = WebDriverWait(self.driver, wait_time).until(
                    EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
                )
            else:
                self.logger.info("Invalid OS type")
                raise ValueError("Invalid OS type")
            
            element.clear()
            self.logger.info(f"{element_type} 텍스트 필드 클리어")
        except TimeoutException:
            self.logger.info(f"{element_type} 오브젝트를 찾지 못함")
            raise Exception(f"{element_type} 오브젝트를 찾지 못함")

    def press_key(self, key):

        if self.os_type == "ios":
            try:
                actions = ActionChains(self.driver)
                actions.send_keys(key)
                actions.perform()
                self.logger.info(f"{key} 키를 누름")
            except TimeoutException:
                self.logger.info(f"{key} 키를 찾지 못함")
                raise Exception(f"{key} 키를 찾지 못함")
        else :
            try:
                if isinstance(key, str):
                    key_value = key.lower()
                    if key_value in ['search', 'enter']:
                        key_code = 66
                    else:
                        self.logger.info(f"지원하지 않는 키: {key_value}")
                        raise ValueError(f"지원하지 않는 키: {key_value}")
                elif isinstance(key, int):
                    key_code = key
                else:
                    self.logger.info("키는 문자열 또는 정수여야 합니다.")
                    raise TypeError("키는 문자열 또는 정수여야 합니다.")

                self.driver.press_keycode(key_code)
                self.logger.info(f"{key} 키를 누름")
            except TimeoutException:
                self.logger.info(f"{key} 키를 찾지 못함")
                raise Exception(f"{key} 키를 찾지 못함")