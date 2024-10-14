from enum import Enum
from appium.webdriver.common.appiumby import AppiumBy

# Enum 클래스 정의: 문자열 검색 유형을 나타냅니다.
class StringType(Enum):
    EQUALS = "=="                # 값이 같은 경우
    BEGINS = "BEGINSWITH"        # 지정된 문자열로 시작하는 경우
    CONTAINS = "CONTAINS"        # 지정된 문자열을 포함하는 경우
    ENDS = "ENDSWITH"            # 지정된 문자열로 끝나는 경우

# Enum 클래스 정의: 다양한 iOS 요소 유형을 나타냅니다.
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

# Enum 클래스 정의: iOS 속성 유형을 나타냅니다.
class PropertyType(Enum):
    NAME = "name"  # 요소의 이름 속성
    LABEL = "label"  # 요소의 레이블 속성
    VALUE = "value"  # 요소의 값 속성

# Enum 클래스 정의: 요소의 가시성을 나타냅니다.
class VisibleType(Enum):
    TRUE = True  # 요소가 화면에 표시되는 경우
    FALSE = False  # 요소가 화면에 표시되지 않는 경우

# Enum 클래스 정의: 다양한 Android 요소 유형을 나타냅니다.
class AndroidElementType(Enum):
    BUTTON = "android.widget.Button"
    TEXT_VIEW = "android.widget.TextView"
    IMAGE_VIEW = "android.widget.ImageView"
    EDIT_TEXT = "android.widget.EditText"
    SWITCH = "android.widget.Switch"
    CHECK_BOX = "android.widget.CheckBox"
    RADIO_BUTTON = "android.widget.RadioButton"
    SPINNER = "android.widget.Spinner"
    LIST_VIEW = "android.widget.ListView"
    GRID_VIEW = "android.widget.GridView"
    VIEW = "android.view.View"

# Enum 클래스 정의: Android 속성 유형을 나타냅니다.
class AndroidPropertyType(Enum):
    DESC = "description"  # 요소의 설명 속성
    TEXT = "text"  # 요소의 텍스트 속성
    ACCESSIBILITY = "accessibilityId"  # 요소의 접근성 ID 속성


# 오브젝트 생성 클래스 정의
class ElementAttributeConverter:
    
    def __init__(self, driver, os_type, rp_logger):
        """
       ElementAttributeConverter 클래스의 생성자.
       :param driver: Appium WebDriver 객체
       :param os_type: 운영체제 유형 (iOS 또는 Android)
       :param rp_logger: 로깅을 위한 Report Portal 로거 객체
       """
        self.driver = driver
        self.os_type = os_type
        self.logger = rp_logger


    def create_locator(self, *args):
        """
        다양한 요소 정의에 기반하여 적절한 locator를 생성합니다.
        :param args: 요소를 정의하기 위한 인수 (iOS 또는 Android에 따라 다름)
        :return: Appium locator 튜플 (locator 유형, 값)
        """
        if self.os_type == "ios":
            if len(args) == 1 and isinstance(args[0], str):
                # 문자열이 XPath로 시작할 경우
                if args[0].startswith("//"):
                    return self.xpath_object(args[0])
                # 문자열에 ':'가 없을 경우 ID로 간주
                elif ":" not in args[0]:
                    return self.id_object(args[0])
                # 그 외 iOS NS PREDICATE로 간주
            return self.ios_predicate_object(*args)
        else:
            # 안드로이드는 모두 android_locator로 전달
            return self.android_locator(*args)

    
    def find_element(self, args):
        """
        지정된 locator를 사용하여 단일 요소를 찾습니다.
        :param args: 요소 locator 인수
        :return: 요소 객체
        """
        return self.driver.find_element(*args)

    def find_elements(self, args):
        """
        지정된 locator를 사용하여 여러 요소를 찾습니다.
        :param args: 요소 locator 인수
        :return: 요소 객체 리스트
        """
        return self.driver.find_elements(*args)


    """
    # === iOS 관련 메서드 ===
    """

    
    def xpath_object(self, xpath):
        """
       XPath를 사용하여 요소를 정의합니다.
       :param xpath: XPath 표현식
       :return: Appium locator 튜플 (XPATH, 값)
       """
        return AppiumBy.XPATH, xpath
    
    def id_object(self, id, index=0):
        """
        ID를 사용하여 요소를 정의합니다.
        :param id: 요소의 ID
        :param index: 요소의 인덱스 (기본값은 0)
        :return: Appium locator 튜플 (ID, 값)
        """
        if index == 0:
            return AppiumBy.ID, id
        else:
            return self.find_elements_by_id(id, index)
    

    def xpath_object_with_args(self, *args):
        """
       다양한 속성을 기반으로 XPath를 생성합니다.
       :param args: 요소를 정의하기 위한 인수
       :return: Appium locator 튜플 (XPATH, 값)
       """
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
        """
        iOS에서 사용되는 NSPredicate를 기반으로 요소를 찾습니다.
        :param args: 요소를 정의하기 위한 인수
        :return: Appium locator 튜플 (IOS_PREDICATE, 값)
        """
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

    def find_elements_by_xpath(self, element_type, index, property_type, property_value):
        xpath = (f"//*[@type='{element_type.value}' and "
                 f"@{property_type.value} = '{property_value}']")
        return AppiumBy.XPATH, xpath
    
    def find_elements_by_id(self, id, index):
        return AppiumBy.ID, id
    
    def list_test_objects(self, predicate, element_type, index, property_value):
        return AppiumBy.IOS_PREDICATE, f"({predicate})[{index + 1}]"




    """
    # === Android 관련 메서드 ===
    """

    
    def android_locator(self, *args):
        """
        Android에서 사용되는 다양한 인수에 기반하여 요소 locator를 생성합니다.
        :param args: 요소를 정의하기 위한 인수
        :return: Appium locator 튜플
        """
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, str):
                # XPath로 요소를 찾을 경우
                if arg.startswith("//"):
                    return AppiumBy.XPATH, arg
                # ':'가 포함되어 있는 경우 ID로 간주
                elif ":" in arg:
                    return AppiumBy.ID, arg
                else:
                    # 접근성 ID로 간주
                    return AppiumBy.ACCESSIBILITY_ID, arg
            elif isinstance(arg, AndroidElementType):
                return AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().className("{arg.value}")'
            elif isinstance(arg, AndroidPropertyType):
                return AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().{arg.value}()'
        # 다양한 인수 조합에 따른 locator 생성 로직들 (인수의 개수와 유형에 따라 다름)
        elif len(args) == 2:
            if isinstance(args[0], AndroidElementType) and isinstance(args[1], str):
                return AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().className("{args[0].value}").text("{args[1]}")'
            elif isinstance(args[0], AndroidPropertyType) and isinstance(args[1], str):
                return AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().{args[0].value}("{args[1]}")'
            elif isinstance(args[0], AndroidElementType) and isinstance(args[1], int):
                return AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().className("{args[0].value}").instance({args[1]})'
            elif args[0] == "uiautomator":
                return AppiumBy.ANDROID_UIAUTOMATOR, args[1]

        elif len(args) == 3:
            if isinstance(args[0], AndroidElementType) and isinstance(args[1], AndroidPropertyType) and isinstance(args[2], str):
                return AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().className("{args[0].value}").{args[1].value}("{args[2]}")'
            elif isinstance(args[0], AndroidPropertyType) and isinstance(args[1], str) and isinstance(args[2], int):
                return AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().{args[0].value}("{args[1]}").instance({args[2]})'

        elif len(args) == 4:
            if isinstance(args[0], AndroidElementType) and isinstance(args[1], AndroidPropertyType) and isinstance(args[2], str) and isinstance(args[3], int):
                return AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().className("{args[0].value}").{args[1].value}("{args[2]}").instance({args[3]})'

        self.logger.error(f"올바르지 않은 값 입니다. : {args}")
        raise ValueError("올바르지 않은 값 입니다.")