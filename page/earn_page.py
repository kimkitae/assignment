
import random
import string
import time
from page.common_page import CommonPage
from helper.element_attribute_converter import ElementType, StringType
from helper.regex_utility import RegexUtility


class EarnPage:
    def __init__(self, driver, os_type, rp_logger):
        self.driver = driver
        self.os_type = os_type
        self.common_page = CommonPage(driver, os_type, rp_logger)
        self.regex_utility = RegexUtility(driver, os_type, rp_logger)
        self.logger = rp_logger


    """
    ========== 함수 변수 ==========
    """

    def bottom_tab_earn_button(self):
        if self.os_type == "ios":
            return "Earn"
        else:
            return "earn_button"


    def earn_way_to_no_button(self):
        if self.os_type == "ios":
            return ElementType.BUTTON, StringType.BEGINS, "earn_way_to_no"
        else:
            return "earn_way_to_no1_btn_usdt"


    def deposit_copy_address_button(self):
        if self.os_type == "ios":
            return "deposit_copy_address"
        else:
            return "deposit_address_copy_no1"
        
    def copied_toast_message(self):
        if self.os_type == "ios":
            return "deposit_address_copied_no1"
        else:
            return "Copied"
        
    def deposit_memo_value(self):
        if self.os_type == "ios":
            return "deposit_memo_value"
        else:
            return "deposit_memo_value"
    
    def deposit_address(self):
        if self.os_type == "ios":
            return "deposit_address"
        else:
            return "deposit_address"
    """
    ------
    """


    """
    ------
    """


    """
    =========== 함수 구현 ==========
    """

    def is_address(self):
        if self.os_type == "ios":
            if self.common_page.is_visible(self.deposit_address()):
                return self.common_page.get_text(self.deposit_address())
            else:
                return False
        else:
            if self.common_page.is_visible("deposit_address"):
                return self.common_page.get_text("deposit_address")
            else:
                return False
    
    def is_memo_value(self):
        if self.os_type == "ios":
            if self.common_page.is_visible(self.deposit_memo_value()):
                return self.common_page.get_text(self.deposit_memo_value())
            else:
                return False
        else:
            if self.common_page.is_visible("deposit_memo_value"):
                return self.common_page.get_text("deposit_memo_value")
            else:
                return False


    def change_network_button(self, index):
        self.common_page.click_element("chevron-down")
        self.common_page.click_element(f"btms_select_network_no_{index + 1}")

    def set_default_first_network(self):
        self.common_page.click_element("chevron-down")
        self.common_page.click_element("btms_select_network_no_1")
    