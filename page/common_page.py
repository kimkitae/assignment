import time
from helper.element_attribute_converter import AndroidElementType, AndroidPropertyType, ElementAttributeConverter
from helper.element_gesture_control import ElementGestureControl
from helper.element_interaction_handle import ElementInteractionHandler
from helper.element_visibility_checker import ElementVisibilityChecker
from helper.execute_method import ExecuteMethod
from helper.regex_utility import RegexUtility


class CommonPage:
    """
    CommonPage 클래스는 공용 기능들을 관리하는 클래스입니다.
    """

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

    def handle_locator(self, *locator):
        """
        주어진 로케이터를 처리하여 적절한 포맷으로 반환.
        """
        # locator가 하나만 전달된 경우 해당 값으로 처리
        if len(locator) == 1:
            single_locator = locator[0]
            if isinstance(single_locator, (str, AndroidElementType, AndroidPropertyType)):
                return self.attribute_converter.create_locator(single_locator)
            elif isinstance(single_locator, (list, tuple)):
                return self.attribute_converter.create_locator(*single_locator)
            else:
                raise TypeError(f"지원하지 않는 locator 타입입니다: {type(single_locator)}")

        # locator가 여러 개 전달된 경우 그대로 풀어서 처리
        elif len(locator) > 1:
            if self.is_locators(locator):
                return self.attribute_converter.create_locator(*locator)
            else:
                raise ValueError("올바르지 않은 다중 로케이터 형식입니다.")

        # 만약 locator가 비어 있을 경우 예외 처리
        else:
            raise ValueError("로케이터가 제공되지 않았습니다.")

    def get_locator(self, *args):
        """
        로케이터 반환
        """
        return self.attribute_converter.create_locator(*args)

    def wait_for(self, *args, timeout=10):
        """
        지정 시간 만큼 해당 오브젝트 wait
        기본 값 10초
        """
        locator = self.handle_locator(*args)
        return self.visibility_checker.wait_for(locator, timeout)

    def find_element(self, *args):
        """
        오브젝트 찾기
        """
        locator = self.handle_locator(*args)
        return self.attribute_converter.find_element(locator)

    def find_elements(self, *args):
        """
        오브젝트 리스트 반환
        """
        locator = self.handle_locator(*args)
        return self.attribute_converter.find_elements(locator)

    def click_element(self, *args):
        """
        오브젝트 클릭
        """
        locator = self.handle_locator(*args)
        self.interaction_handler.click_on(locator)

    def is_visible(self, *args, timeout=10):
        """
        오브젝트 노출 확인
        """
        locator = self.handle_locator(*args)
        return self.visibility_checker.wait_for(locator, timeout)

    def swipe(self, direction, percentage=50):
        """
        지정 방향으로 1회 스와이프
        """
        self.gesture_control.swipe_from_center_to(percentage, direction)

    def set_text(self, text, *args):
        """
        해당 오브젝트 Text 값 입력
        """
        locator = self.handle_locator(*args)
        self.interaction_handler.set_text(locator, text)

    def get_text(self, *args):
        """
        해당 오브젝트 Text 값 반환
        """
        locator = self.handle_locator(*args)
        return self.interaction_handler.get_text(locator)

    def clean_text_field(self, element_type):
        """
        텍스트 필드 입력 초기화
        """
        self.interaction_handler.clean_text_field(element_type)

    def scroll_to_text(self, text):
        """
        StaticText의 특정 Text 찾을때까지 스와이프
        """
        self.gesture_control.scroll_to_text(text)

    def swipe_to_element(self, *args):
        """
        오브젝트 찾을때까지 스와이프
        """
        locator = self.handle_locator(*args)
        self.gesture_control.swipe_to_element(locator)

    def press_key(self, key):
        """
        키 이벤트 발생
        search, enter 사용
        """
        self.interaction_handler.press_key(key)

    def get_text_by_keyword(self, keyword, page_source=None):
        """
        기 정의된 Regex 노출 여부 확인
        """
        return self.regex_utility.get_text_by_keyword(keyword, page_source)

    def get_page_source(self):
        """
        현재 페이지 소스 반환
        """
        return self.execute_method.get_page_source_in_json()

    def is_locators(self, locator):
        """
        주어진 인자가 복수 로케이터인지 여부를 확인
        Args:
            locator: 로케이터 인자
        
        Returns:
            bool: 여러 로케이터이면 True, 아니면 False
        """
        return isinstance(locator, tuple) and len(locator) > 1

    def swtiching_context(self, context_name):
        """
        해당 Context_name 으로 Context 변경
        """

        #최대 3초 까지 해당 Context 노출 확인 및 변환
        for _ in range(3):
            contexts = self.driver.contexts
            if any("WEBVIEW" in context for context in contexts) and context_name in contexts:
                self.driver.switch_to.context(context_name)
                self.logger.info(f"{context_name}으로 Context 변경")
                return True
            time.sleep(1)
        
        self.logger.warning(f"{context_name}이 3초 내에 나타나지 않았습니다.")
        return False

    def is_webview_context(self):
        """
        현재 WebView Context 여부 반환
        """
        is_webview = "WEBVIEW" in self.driver.context
        self.logger.info(f"현재 Context: {self.driver.context}")
        return is_webview 