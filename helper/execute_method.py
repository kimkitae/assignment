import os
from selenium.webdriver import ActionChains
from dotenv import load_dotenv

# W3C 기능 클래스 정의
class ExecuteMethod:
    def __init__(self, driver, os_type, rp_logger):
        # 드라이버와 OS 타입, 로거를 초기화
        self.logger = rp_logger
        self.driver = driver
        self.os_type = os_type
        load_dotenv()

    def activate_app(self):
        # 앱을 활성화하는 메서드 (iOS와 Android의 실행 방식이 다름)
        if self.os_type == "ios":
            self.driver.execute_script("mobile: activateApp", {"bundleId": os.getenv("APP_BUNDLE")})
        elif self.os_type == "android":
            self.driver.execute_script("mobile: activateApp", {"appId": os.getenv("APP_PACKAGE")})

    def launch_app(self):
        # 앱을 실행하는 메서드 (iOS와 Android 모두)
        if self.os_type == "ios":
            self.driver.execute_script("mobile: launchApp", {"bundleId": os.getenv("APP_BUNDLE")})
        elif self.os_type == "android":
            self.driver.execute_script("mobile: activateApp", {"appId": os.getenv("APP_PACKAGE")})

    def terminate_app(self):
        # 앱을 종료하는 메서드
        if self.os_type == "ios":
            self.driver.execute_script("mobile: terminateApp", {"bundleId": os.getenv("APP_BUNDLE")})
        elif self.os_type == "android":
            self.driver.execute_script("mobile: terminateApp", {"appId": os.getenv("APP_PACKAGE")})

    def swipe(self,direction):
        # 화면을 스와이프하는 메서드 (지정한 방향으로)
        self.driver.execute_script("mobile: swipe", {"direction": direction, "velocity": 250})

    def swipe_on_element(self, element, direction):
        # 특정 요소를 기준으로 스와이프하는 메서드
        self.driver.execute_script("mobile: swipe", {"element": element.id, "direction": direction, "velocity": 250})

    def drag_from_to(self, start_x, start_y, end_x, end_y, duration_time):
        # 드래그 앤 드롭을 수행하는 메서드
        duration = duration_time / 1000.0
        if self.os_type == "ios":
            # iOS 드래그 앤 드롭 방식
            self.driver.execute_script("mobile: dragFromToForDuration", {
                "duration": duration,
                "fromX": start_x,
                "fromY": start_y,
                "toX": end_x,
                "toY": end_y
            })
        else:
            # Android 드래그 앤 드롭 방식
            actions = ActionChains(self.driver)
            actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
            actions.w3c_actions.pointer_action.pointer_down()
            actions.w3c_actions.pointer_action.pause(duration)
            actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
            actions.w3c_actions.pointer_action.release()
            actions.perform()

    def get_page_source_in_json(self):
        # 페이지 소스를 JSON 형식으로 가져오는 메서드 (iOS만 JSON 지원)
        if self.os_type == "ios":
            return self.driver.execute_script("mobile: source", {"format": "json", "recursive": True})
        elif self.os_type == "android":
            return self.driver.page_source

    def hide_keyboard(self):
        # 키보드를 숨기는 메서드
        self.driver.execute_script("mobile: hideKeyboard", {"keys": ["done", "완료"]})

    def is_keyboard_shown(self):
        # 키보드가 표시되어 있는지 확인하는 메서드
        return self.driver.execute_script("mobile: isKeyboardShown")

    def scroll_to_element(self, element_id):
        # 특정 요소까지 스크롤하는 메서드
        self.driver.execute_script("mobile: scrollToElement", {"elementId": element_id})

    def scroll(self, direction, predicate_string):
        # 주어진 방향과 조건(predicate)에 따라 화면을 스크롤하는 메서드
        self.driver.execute_script("mobile: scroll", {
            "direction": direction,
            "predicateString": predicate_string,
            "toVisible": True
        })