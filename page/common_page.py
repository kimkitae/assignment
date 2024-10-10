from selenium.common.exceptions import NoSuchElementException
from time import sleep
from page.element_visibility_checker import ElementVisibilityChecker
from page.element_interaction_handle import ElementInteractionHandler
from page.element_gesture_control import ElementGestureControl
from page.execute_method import ExecuteMethod
from page.element_attribute_converter import ElementAttributeConverter, ElementType, PropertyType, StringType
from page.regex_utility import RegexUtility
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.keys import Keys


class CommonPage:
    def __init__(self, driver, os_type):
        self.driver = driver
        self.os_type = os_type
        self.visibility_checker = ElementVisibilityChecker(driver)
        self.gesture_control = ElementGestureControl(driver, os_type)
        self.attribute_converter = ElementAttributeConverter(os_type)
        self.interaction_handler = ElementInteractionHandler(driver, os_type)
        self.execute_method = ExecuteMethod(driver, os_type)
        self.regex_utility = RegexUtility(driver, os_type)

    def get_locator(self, *args):
        return self.attribute_converter.create_locator(*args)


    def wait_for(self, *args, timeout=10):
        locator = self.get_locator(*args)
        return self.visibility_checker.wait_for(locator, timeout)

    def find_element(self, *args):
        locator = self.get_locator(*args)
        return self.driver.find_element(*locator)

    def find_elements(self, *args):
        locator = self.get_locator(*args)
        return self.driver.find_elements(*locator)

    def click_element(self, *args):
        locator = self.get_locator(*args)
        self.interaction_handler.click_on(locator)

    def is_visible(self, *args, timeout=10):
        locator = self.get_locator(*args)
        return self.visibility_checker.wait_for(locator, timeout)

    def swipe(self, direction, percentage=50):
        self.gesture_control.swipe_from_center_to(percentage, direction)

    def set_text(self, text, *args):
        locator = self.get_locator(*args)
        self.interaction_handler.set_text(locator, text)

    def get_text(self, *args):
        locator = self.get_locator(*args)
        return self.interaction_handler.get_text(locator)

    def scroll_to_text(self, text):
        self.gesture_control.scroll_to_text(text)

    def swipe_to_element(self, *args):
        locator = self.find_element(*args)
        self.gesture_control.swipe_to_element(locator)

    def press_key(self, key):
        self.interaction_handler.press_key(key)

    def get_text_by_keyword(self, keyword, page_source=None):
        return self.regex_utility.get_text_by_keyword(keyword, page_source)
    
    def get_pagesource(self):
        return self.execute_method.get_page_source_in_json()
    
    def is_locators(self, *locator):
        """
        주어진 인자가 로케이터인지 확인하는 함수입니다.
        
        Args:
            *locator: 확인할 인자들
        
        Returns:
            bool: 로케이터이면 True, 아니면 False
        """
        # 인자가 하나만 있고, 그것이 문자열인 경우 locator, 그 외 locators 
        if isinstance(locator[0], str):
            return False
        return True