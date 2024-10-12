from helper.element_attribute_converter import AndroidElementType, AndroidPropertyType, ElementAttributeConverter, ElementType
from helper.element_gesture_control import ElementGestureControl
from helper.element_interaction_handle import ElementInteractionHandler
from helper.element_visibility_checker import ElementVisibilityChecker
from helper.execute_method import ExecuteMethod
from helper.regex_utility import RegexUtility


class CommonPage:
    def __init__(self, driver, os_type, rp_logger):
        self.driver = driver
        self.os_type = os_type
        self.visibility_checker = ElementVisibilityChecker(driver, rp_logger)
        self.gesture_control = ElementGestureControl(driver, os_type, rp_logger)
        self.attribute_converter = ElementAttributeConverter(driver, os_type, rp_logger)
        self.interaction_handler = ElementInteractionHandler(driver, os_type, rp_logger)
        self.execute_method = ExecuteMethod(driver, os_type, rp_logger)
        self.regex_utility = RegexUtility(driver, os_type, rp_logger)
        self.logger = rp_logger

    def handle_locator(self, locator):
        """
        주어진 로케이터를 처리하여 적절한 포맷으로 반환.
        """
        if self.is_locators(locator):
            return self.attribute_converter.create_locator(*locator)
        else:
            # locator가 문자열, AndroidElementType, AndroidPropertyType일 경우 처리
            if isinstance(locator, (str, AndroidElementType, AndroidPropertyType)):
                return self.attribute_converter.create_locator(locator)
            # locator가 리스트나 튜플일 경우 풀어서 처리
            elif isinstance(locator, (list, tuple)):
                return self.attribute_converter.create_locator(*locator)
            else:
                raise TypeError(f"지원하지 않는 locator 타입입니다: {type(locator)}")

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
        self.interaction_handler.click_on(locator)

    def is_visible(self, *args, timeout=10):
        locator = self.handle_locator(*args)
        return self.visibility_checker.wait_for(locator, timeout)

    def swipe(self, direction, percentage=50):
        self.gesture_control.swipe_from_center_to(percentage, direction)

    def set_text(self, text, *args):
        locator = self.handle_locator(*args)
        print(locator)
        self.interaction_handler.set_text(locator, text)

    def get_text(self, *args):
        locator = self.handle_locator(*args)
        return self.interaction_handler.get_text(locator)

    def clean_text_field(self, element_type):
        self.interaction_handler.clean_text_field(element_type)

    def scroll_to_text(self, text):
        self.gesture_control.scroll_to_text(text)

    def swipe_to_element(self, *args):
        locator = self.handle_locator(*args)
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
