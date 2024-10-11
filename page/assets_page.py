

from page.common_page import CommonPage
from page.element_attribute_converter import ElementType, PropertyType


class AssetsPage:
    def __init__(self, driver, os_type):
        self.driver = driver
        self.os_type = os_type
        self.common_page = CommonPage(driver, os_type)

    
    """
    ========== Element 변수 ==========
    """
    def bottom_tab_assets_button(self):
        if self.os_type == "ios":
            return ElementType.STATIC_TEXT, PropertyType.LABEL, "Assets"
        else:
            return "market_button"
        
    

    """
    ========== 함수 변수 ==========
    """
     
    def click_assets_button(self):
        locator = self.bottom_tab_assets_button()
        self.common_page.click_element(locator)
