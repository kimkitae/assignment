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
    def __init__(self, driver):
        self.driver = driver
        self.visibility_checker = ElementVisibilityChecker(driver)
        self.interaction_handler = ElementInteractionHandler(driver)
        self.gesture_control = ElementGestureControl(driver)
        self.attribute_converter = ElementAttributeConverter()
        self.execute_method = ExecuteMethod(driver)
        self.regex_utility = RegexUtility(driver)
        self.execute_method.launch_app()

    def find_element(self, *args):
        locator = self.get_locator(*args)
        return self.driver.find_element(*locator)

    def click_element(self, *args):
        element = self.get_locator(*args)
        self.interaction_handler.click_on(element)

    def wait_for_element(self, *args, timeout=10):
        locator = self.get_locator(*args)
        return self.visibility_checker.wait_for(locator, timeout)

    def swipe(self, direction, percentage=50):
        self.gesture_control.swipe_from_center_to(percentage, direction)

    def set_text(self, text, *args):
        element = self.get_locator(*args)
        self.interaction_handler.set_text(element, text)

    def get_text(self, *args):
        element = self.get_locator(*args)
        return self.interaction_handler.get_text(element)

    def wait_for_seconds(self, seconds):
        sleep(seconds)
        print(f"{seconds}초 동안 대기합니다.")

    def is_visible(self, *args, timeout=3):
        locator = self.get_locator(*args)
        return self.visibility_checker.is_visible(locator, timeout)

    def scroll_to_text(self, text):
        return self.gesture_control.scroll_to_text(text)

    def get_locator(self, *args):
        if isinstance(args[0], ElementType):
            return self.attribute_converter.ios_predicate_object(*args)
        elif isinstance(args[0], str):
            if args[0].startswith("//"):
                return (AppiumBy.XPATH, args[0])
            else:
                return (AppiumBy.ID, args[0])
        raise ValueError(f"Invalid locator format: {args}")

    def create_ios_predicate(self, element_type, property_type, value):
        return self.attribute_converter.ios_predicate_object(element_type, property_type, value)

    def press_key(self, key: str):
        key_event = key.lower()
        if key_event == "search":
            self.interaction_handler.press_key(Keys.RETURN)
        elif key_event == "enter":
            self.interaction_handler.press_key(Keys.ENTER)
        else:
            print("지원하지 않는 키입니다.")

    def get_text_by_keyword(self, keyword=None, page_source=None,):
        return self.regex_utility.get_text_by_keyword(keyword, page_source)

    def get_matched_text(self, keyword=None, page_source=None):
        return self.regex_utility.matchered_text(keyword, page_source)
