from page.element_attribute_converter import ElementAttributeConverter
from page.element_gesture_control import ElementGestureControl
from page.element_interaction_handle import ElementInteractionHandler
from page.element_visibility_checker import ElementVisibilityChecker
from page.execute_method import ExecuteMethod
from page.regex_utility import RegexUtility


class CommonPage:
    def __init__(self, driver, os_type):
        self.driver = driver
        self.os_type = os_type
        self.visibility_checker = ElementVisibilityChecker(driver)
        self.gesture_control = ElementGestureControl(driver, os_type)
        self.attribute_converter = ElementAttributeConverter(driver, os_type)
        self.interaction_handler = ElementInteractionHandler(driver, os_type)
        self.execute_method = ExecuteMethod(driver, os_type)
        self.regex_utility = RegexUtility(driver, os_type)

    def handle_locator(self, locator):
        """
        주어진 로케이터를 처리하여 적절한 포맷으로 반환.
        """
        print(f"handle_locator - {locator}")
        if self.is_locators(locator):
            print("is_locators")
            return self.attribute_converter.create_locator(*locator)
        else:
            print("not is_locators")
            # locator가 문자열일 경우, 이를 풀지 않고 그대로 전달
            if isinstance(locator, str):
                return self.attribute_converter.create_locator(locator)
            else:
                return self.attribute_converter.create_locator(*locator)  # 튜플일 경우 풀어서 전달

    def get_locator(self, *args):
        return self.attribute_converter.create_locator(*args)

    def wait_for(self, *args, timeout=10):
        locator = self.handle_locator(*args)
        return self.visibility_checker.wait_for(locator, timeout)

    def find_element(self, *args):
        locator = self.handle_locator(*args)
        return self.attribute_converter.find_element(locator)

    def find_elements(self, *args):
        locator = self.handle_locator(*args)
        return self.attribute_converter.find_elements(locator)

    def click_element(self, *args):
        locator = self.handle_locator(*args)
        print(f"click_element - {locator}")
        self.interaction_handler.click_on(locator)

    def is_visible(self, *args, timeout=10):
        locator = self.handle_locator(*args)
        return self.visibility_checker.wait_for(locator, timeout)

    def swipe(self, direction, percentage=50):
        self.gesture_control.swipe_from_center_to(percentage, direction)

    def set_text(self, text, *args):
        locator = self.handle_locator(*args)
        self.interaction_handler.set_text(locator, text)

    def get_text(self, *args):
        locator = self.handle_locator(*args)
        return self.interaction_handler.get_text(locator)

    def scroll_to_text(self, text):
        self.gesture_control.scroll_to_text(text)

    def swipe_to_element(self, *args):
        locator = self.handle_locator(*args)
        print(f"swipe_element - {locator}")
        self.gesture_control.swipe_to_element(locator)

    def press_key(self, key):
        self.interaction_handler.press_key(key)

    def get_text_by_keyword(self, keyword, page_source=None):
        return self.regex_utility.get_text_by_keyword(keyword, page_source)

    def get_pagesource(self):
        return self.execute_method.get_page_source_in_json()

    def is_locators(self, locator):
        """
        주어진 인자가 복수 로케이터인지 여부를 확인합니다.
        Args:
            locator: 로케이터 인자
        
        Returns:
            bool: 여러 로케이터이면 True, 아니면 False
        """
        return isinstance(locator, tuple) and len(locator) > 1
