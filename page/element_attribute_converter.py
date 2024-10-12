from enum import Enum
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class StringType(Enum):
    EQUALS = "=="
    BEGINS = "BEGINSWITH"
    CONTAINS = "CONTAINS"
    ENDS = "ENDSWITH"


class ElementType(Enum):
    BUTTON = "XCUIElementTypeButton"
    STATIC_TEXT = "XCUIElementTypeStaticText"
    OTHER = "XCUIElementTypeOther"
    IMAGE = "XCUIElementTypeImage"
    CELL = "XCUIElementTypeCell"
    NAVIGATION_BAR = "XCUIElementTypeNavigationBar"
    SWITCH = "XCUIElementTypeSwitch"
    WEB_VIEW = "XCUIElementTypeWebView"
    WINDOW = "XCUIElementTypeWindow"
    SECURE_TEXT_FIELD = "XCUIElementTypeSecureTextField"
    TEXT_FIELD = "XCUIElementTypeTextField"
    SEARCH_FIELD = "XCUIElementTypeSearchField"
    LINK = "XCUIElementTypeLink"
    TEXT_VIEW = "XCUIElementTypeTextView"
    KEYBOARD = "XCUIElementTypeKeyboard"
    APPLICATION = "XCUIElementTypeApplication"
    TYPE_KEY = "XCUIElementTypeKey"


class PropertyType(Enum):
    NAME = "name"
    LABEL = "label"
    VALUE = "value"


class VisibleType(Enum):
    TRUE = True
    FALSE = False


class ElementAttributeConverter:
    
    def __init__(self, driver, os_type, rp_logger):
        self.driver = driver
        self.os_type = os_type
        self.logger = rp_logger

    def create_locator(self, *args):
        if self.os_type == "ios":
            if len(args) == 1 and isinstance(args[0], str):
                if args[0].startswith("//"):
                    return self.xpath_object(args[0])
                elif ":" not in args[0]:  # ID로 간주
                    return self.id_object(args[0])
            return self.ios_predicate_object(*args)
        elif self.os_type == "android":
            return self.android_ui_automator_object(*args)
        else:
            raise ValueError(f"Unsupported OS type: {self.os_type}")
    
    def xpath_object(self, xpath):
        return AppiumBy.XPATH, xpath
    
    def id_object(self, id, index=0):
        if index == 0:
            return AppiumBy.ID, id
        else:
            return self.find_elements_by_id(id, index)
    

    def xpath_object_with_args(self, *args):
        visible_type = VisibleType.FALSE
        string_type = StringType.EQUALS
        element_type = ElementType.BUTTON
        property_type = PropertyType.NAME
        property_value = ""
        element_index = 0
        
        for arg in args:
            if isinstance(arg, StringType):
                string_type = arg
            elif isinstance(arg, ElementType):
                element_type = arg
            elif isinstance(arg, PropertyType):
                property_type = arg
            elif isinstance(arg, str):
                property_value = arg
            elif isinstance(arg, int):
                element_index = arg
            elif isinstance(arg, VisibleType):
                visible_type = arg
        
        if element_index == 0:
            xpath = f"//*[@type='{element_type.value}' and @{property_type.value} = '{property_value}']"
            if visible_type == VisibleType.TRUE:
                xpath += " and @visible='true'"
            return AppiumBy.XPATH, xpath
        else:
            return self.find_elements_by_xpath(element_type, element_index, property_type, property_value)
    
    def ios_predicate_object(self, *args):
        visible_type = VisibleType.FALSE
        string_type = StringType.EQUALS
        element_type = ElementType.BUTTON
        property_type = PropertyType.NAME
        property_value = ""
        element_index = 0
        
        for arg in args:
            if isinstance(arg, StringType):
                string_type = arg
            elif isinstance(arg, ElementType):
                element_type = arg
            elif isinstance(arg, PropertyType):
                property_type = arg
            elif isinstance(arg, str):
                property_value = arg
            elif isinstance(arg, int):
                element_index = arg
            elif isinstance(arg, VisibleType):
                visible_type = arg

        predicate = f"type == '{element_type.value}'"
        
        if property_value:
            predicate += f" AND {property_type.value} {string_type.value} '{property_value}'"
        
        if visible_type == VisibleType.TRUE:
            predicate += " AND visible == true"
        
        if element_index == 0:
            return AppiumBy.IOS_PREDICATE, predicate
        else:
            return AppiumBy.IOS_PREDICATE, f"({predicate})[{element_index + 1}]"
            # return self.list_test_objects(predicate, element_type, element_index, property_value)
    
    def find_elements_by_xpath(self, element_type, index, property_type, property_value):
        xpath = (f"//*[@type='{element_type.value}' and "
                 f"@{property_type.value} = '{property_value}']")
        return AppiumBy.XPATH, xpath
    
    def find_elements_by_id(self, id, index):
        return AppiumBy.ID, id
    
    def list_test_objects(self, predicate, element_type, index, property_value):
        return AppiumBy.IOS_PREDICATE, f"({predicate})[{index + 1}]"
    

    def android_ui_automator_object(self, *args):
        if len(args) == 1 and isinstance(args[0], str):
            # 단일 문자열 인자인 경우 XPath로 간주
            if args[0].startswith("//"):
                return AppiumBy.XPATH, args[0]
            # 그 외의 경우 resource-id로 간주
            else:
                return AppiumBy.ID, args[0]
        elif len(args) == 2 and isinstance(args[0], str) and isinstance(args[1], int):
            # 문자열과 인덱스가 주어진 경우
            locator, index = args
            if locator.startswith("//"):
                return AppiumBy.XPATH, f"({locator})[{index + 1}]"
            else:
                return AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("{locator}").instance({index})'
        else:
            raise ValueError("Invalid arguments for Android locator")

    def find_element(self, args):
        return self.driver.find_element(*args)

    def find_elements(self, args):
        return self.driver.find_elements(*args)
