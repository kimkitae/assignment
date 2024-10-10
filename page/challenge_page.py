

from page.element_attribute_converter import ElementType, PropertyType


class ChallengePage:
    def __init__(self, driver, os_type):
        self.driver = driver
        self.os_type = os_type
        self.common_page = CommonPage(driver, os_type)



    """
    ============ 변수 선언 영역 ============
    """

    def bottom_tab_challenge_button(self):
        if self.os_type == "ios":
            return ElementType.STATIC_TEXT, PropertyType.LABEL, "Challenge"
        else:
            return "market_button"


    """
    ============ 변수 선언 영역 ============
    """

    def click_challenge_button(self):
        locator = self.bottom_tab_challenge_button()
        if self.common_page.is_locators(locator):
            self.common_page.click_element(*locator)
        else :
            self.common_page.click_element(locator)

