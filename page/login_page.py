

from page.common_page import CommonPage
from page.home_page import HomePage


class LoginPage:
    def __init__(self, driver, os_type):
        self.driver = driver
        self.os_type = os_type
        self.common_page = CommonPage(driver, os_type)
        self.home_page = HomePage(driver, os_type)

    def check_signed_up (self):
        
        try :
            self.common_page.click_element("menu_icon")
            assert self.common_page.is_visible("account_nick_value_01-tab_account_nick_edit"), "회원 닉네임 노출"
            nick_name = self.common_page.get_text("account_nick_value_01-tab_account_nick_edit")
            assert nick_name == "Automation_test", "회원 닉네임 'Automation_test' 일치"
            return True
        except Exception as e:
            print(f"예외 발생: {e}")
            return False
        

