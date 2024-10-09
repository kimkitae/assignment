from enum import Enum
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import driver


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
    
    @staticmethod
    def xpath_object(xpath):
        return AppiumBy.XPATH, xpath
    
    @staticmethod
    def id_object(id, index=0):
        if index == 0:
            return AppiumBy.ID, id
        else:
            return ElementAttributeConverter.find_elements_by_id(id, index)
    
    @staticmethod
    def xpath_object_with_args(*args):
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
            return ElementAttributeConverter.find_elements_by_xpath(element_type, element_index, property_type, property_value)
    
    @staticmethod
    def ios_predicate_object(*args):
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
        
        print(f"Generated iOS Predicate: {predicate}")  # 디버깅을 위한 출력
        
        if element_index == 0:
            return AppiumBy.IOS_PREDICATE, predicate
        else:
            return ElementAttributeConverter.list_test_objects(predicate, element_type, element_index, property_value)
    
    @staticmethod
    def find_elements_by_xpath(element_type, index, property_type, property_value):
        xpath = (f"//*[@type='{element_type.value}' and "
                 f"@{property_type.value} = '{property_value}']")
        return AppiumBy.XPATH, xpath
    
    @staticmethod
    def find_elements_by_id(id, index):
        return AppiumBy.ID, id
    
    @staticmethod
    def list_test_objects(predicate, element_type, index, property_value):
        return AppiumBy.IOS_PREDICATE, predicate

