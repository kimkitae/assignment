

import time
from page.common_page import CommonPage


class LoginPage:
    def __init__(self, driver, os_type, rp_logger):
        self.logger = rp_logger
        self.driver = driver
        self.os_type = os_type
        self.common_page = CommonPage(driver, os_type, rp_logger)


    """
    ========== 함수 변수 ==========
    """

    def menu_icon(self):
        if self.os_type == "ios":
            return "menu_icon"
        else:
            return "prex_signin_menu"

    def account_nickname_text(self):
        if self.os_type == "ios":
            return "account_nick_value_01-tab_account_nick_edit"
        else:
            return "account_nick_value_01"

    def account_main_title(self):
        if self.os_type == "ios":
            return "account_main_title"
        else:
            return "account_main_title"


    def account_sign_out_button(self):
        if self.os_type == "ios":
            return "account_sign_out"
        else:
            return "account_sign_out"
    
    def signin_setting_button(self):
        if self.os_type == "ios":
            return "prex_signin_settings"
        else:
            return "prex_signin_settings"

    def back_icon(self):
        if self.os_type == "ios":
            return "back_icon"
        else:
            return "back_icon"

    """
    =========== 함수 구현 ==========
    """

    def check_signed_up (self):
        try :
            self.common_page.click_element(self.menu_icon())
            assert self.common_page.is_visible(self.account_nickname_text()), "회원 닉네임 노출"
            nick_name = self.common_page.get_text(self.account_nickname_text())
            self.logger.info(f"회원 닉네임: {nick_name}")
            assert nick_name == "Automation_test", "회원 닉네임 'Automation_test' 일치"
            return True
        except Exception as e:
            self.logger.info(f"예외 발생: {e}")
            return False

    def logout(self):
        self.common_page.click_element(self.menu_icon())
        assert self.common_page.is_visible(self.account_main_title()), "Account 화면 진입 확인"
        if self.common_page.is_visible(self.account_nickname_text()):
            self.common_page.swipe_to_element(self.account_sign_out_button())
            self.common_page.click_element(self.account_sign_out_button())
            self.common_page.wait_for(self.menu_icon(), timeout=3)
            assert self.common_page.is_visible(self.menu_icon()), "로그아웃 성공"
        else:
            self.logger.info("이미 로그아웃 상태입니다.")
            self.common_page.click_element(self.back_icon())
            time.sleep(1)
    
    def click_menu_icon(self):
        locator = self.menu_icon()
        self.common_page.click_element(locator)

    def click_support_menu(self, title):
        if self.os_type == "ios":
            self.common_page.click_element(f"Setting_{title}")
        else:
            self.common_page.click_element(f"Setting_{title}")

    def click_setting_icon(self):
        locator = self.signin_setting_button()
        self.common_page.click_element(locator)


    def logout_test(self):
        self.common_page.click_element(self.menu_icon())
        assert self.common_page.is_visible(self.account_main_title()), "Account 화면 진입 확인"
        if self.common_page.is_visible(self.account_nickname_text()):
            self.common_page.swipe_to_element(self.account_sign_out_button())
            self.common_page.click_element(self.account_sign_out_button())
            self.common_page.wait_for(self.menu_icon(), timeout=3)
            assert self.common_page.is_visible(self.menu_icon()), "로그아웃 성공"
        else:
            self.logger.info("이미 로그아웃 상태입니다.")
            self.common_page.click_element(self.back_icon())
            time.sleep(1)

