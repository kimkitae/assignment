



from page.common_page import CommonPage
from helper.element_attribute_converter import ElementType, PropertyType


class EtcPage:
    def __init__(self, driver, os_type, rp_logger):
        self.logger = rp_logger
        self.driver = driver
        self.os_type = os_type
        self.common_page = CommonPage(driver, os_type, rp_logger)


    """
    ========= 변수 선언 =========
    """
    def web_open_messaging_windows_button(self):
        if self.os_type == "ios":
           return ElementType.BUTTON, PropertyType.LABEL, "Open messaging window"
        elif self.os_type == "android":
            return "Open messaging window"

    def web_close_messaging_windows_button(self):
        if self.os_type == "ios":
           return ElementType.BUTTON, PropertyType.LABEL, "Close"
        elif self.os_type == "android":
            return "Close"

    
    def web_chatbot_text(self):
        if self.os_type == "ios":
            return ElementType.STATIC_TEXT, PropertyType.LABEL, "Flippy v.2 says:"
        elif self.os_type == "android":
            return "Flippy v.2 says:"


    """
    ========= 메소드 =========
    """

    def click_open_messaging_windows(self):
        self.common_page.click_element(self.web_open_messaging_windows_button())

    def click_close_messaging_windows(self):
        self.common_page.click_element(self.web_close_messaging_windows_button())

    def is_visible_chatbot(self):
        return self.common_page.is_visible(self.web_chatbot_text())


