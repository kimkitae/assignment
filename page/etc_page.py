import time
from page.common_page import CommonPage
from helper.element_attribute_converter import ElementType, PropertyType
from selenium.webdriver.common.by import By

class EtcPage:
    """
    EtcPage 클래스는 특정 화면이 아닌 정보와 동작을 관리하는 클래스입니다.
    """

    def __init__(self, driver, os_type, rp_logger):
        self.logger = rp_logger
        self.driver = driver
        self.os_type = os_type
        self.common_page = CommonPage(driver, os_type, rp_logger)


    """
    ========= 객체 반환 함수 =========
    """

    # 웹뷰 내 Open Messaging windows 버튼
    def web_open_messaging_windows_button(self):
        if self.os_type == "ios":
           return ElementType.BUTTON, PropertyType.LABEL, "Open messaging window"
        elif self.os_type == "android":
            return "Open messaging window"

    # 웹뷰 내 닫기 버튼
    def web_close_messaging_windows_button(self):
        if self.os_type == "ios":
           return ElementType.BUTTON, PropertyType.LABEL, "Close"
        elif self.os_type == "android":
            return "Close"

    # 웹뷰 내 챗봇 텍스트 영역
    def web_chatbot_text(self):
        if self.os_type == "ios":
            return ElementType.STATIC_TEXT, PropertyType.LABEL, "Flippy v.2 says:"
        elif self.os_type == "android":
            return "Flippy v.2 says:"

    """
    ========= 기능 함수 ===========
    """

    def click_open_messaging_windows(self):
        """
        open messaging 버튼 선택
        Android는 WebView 전환 시도, 실패 시 Native 형태로 해당 버튼 클릭
        """
        if self.os_type == "ios":
            self.common_page.click_element(self.web_open_messaging_windows_button())
        else:
            time.sleep(2)
            # 웹뷰 컨텍스트 인 경우
            if self.common_page.is_webview_context():
                element = self.driver.find_element(By.XPATH, '//button[@aria-label="Open messaging window"]')
                element.click()
                self.logger.info("웹뷰에서 Open messaging window 버튼을 iframe id를 사용하여 클릭했습니다.")
            else:
                is_webivew = self.common_page.swtiching_context("WEBVIEW_chrome")
                if is_webivew:
                    element = self.driver.find_element(By.XPATH, '//button[@aria-label="Open messaging window"]')
                    element.click()
                    self.logger.info("웹뷰에서 Open messaging window 버튼을 iframe id를 사용하여 클릭했습니다.")
                else :
                    self.common_page.click_element('uiautomator', 'new UiSelector().text("Open messaging window")')
                    self.logger.info("네이티브에서 Open messaging window 버튼을 text를 사용하여 클릭했습니다.")


    def click_close_messaging_windows(self):
        """
        웹뷰 내 채팅창 닫기 버튼 클릭
        Android는 웹뷰 컨텍스트로 시도 하나 실패 시 Native로 버튼 클릭
        """
        if self.os_type == "ios":
            self.common_page.click_element(self.web_close_messaging_windows_button())
        else:
            if self.common_page.is_webview_context():
                # 웹뷰 컨텍스트인 경우
                element = self.driver.find_element(By.XPATH, "//button[@aria-label='Close']")
                element.click()
                self.logger.info("웹뷰에서 Close 버튼을 aria-label을 사용하여 클릭했습니다.")
            else:
                # 웹뷰 컨텍스트가 아닌 경우
                is_switched = self.common_page.swtiching_context("WEBVIEW_chrome")
                if is_switched:
                    element = self.driver.find_element(By.XPATH, "//button[@aria-label='Close']")
                    element.click()
                    self.logger.info("웹뷰에서 Close 버튼을 aria-label을 사용하여 클릭했습니다.")
                else:
                    # 웹뷰로 전환 실패 시 네이티브 형태로 시도
                    self.common_page.click_element('uiautomator', 'new UiSelector().text("Close")')
                    self.logger.info("네이티브에서 Close 버튼을 text를 사용하여 클릭했습니다.")

    def is_visible_chatbot(self):
        """
        현재 웹뷰 화면 내 챗봇의 텍스트 영역으로 노출 여부 확인
        Android는 웹뷰 컨텍스트로 시도 ㅎ나 실패 시 Native로 접근
        """
        if self.os_type == "ios":
            return self.common_page.is_visible(self.web_chatbot_text())
        else:
            if self.common_page.is_webview_context():
                element = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Hi there. Got a question?')]")
                return element.is_displayed()
            else:
                is_webivew = self.common_page.swtiching_context("WEBVIEW_chrome")
                if is_webivew:
                    element = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Hi there. Got a question?)]")
                    return element.is_displayed()
                else :
                    return self.common_page.is_visible('uiautomator', 'new UiSelector().textStartsWith("Hi there. Got a")')

