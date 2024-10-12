import time
import pytest

from page.account_page import AccountPage
from page.execute_method import ExecuteMethod
from page.common_page import CommonPage
from page.login_page import LoginPage
from page.element_attribute_converter import ElementType, PropertyType, StringType

class TestScenario:
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, os_type, rp_logger):
        self.common_page = CommonPage(driver, os_type, rp_logger)
        self.login_page = LoginPage(driver, os_type, rp_logger)
        self.account_page = AccountPage(driver, os_type, rp_logger)
        self.execute_method = ExecuteMethod(driver, os_type, rp_logger)
        self.logger = rp_logger


    def test_change_nickname(self):
        self.common_page.click_element(self.account_page.menu_icon())

        current_nickname = self.account_page.account_nickname_text()
        assert self.account_page.change_nickname(self.account_page.generate_random_nickname(current_nickname)), "닉네임 변경 확인"
        self.logger.info("닉네임 변경 확인")

    def test_weekly_leaderboard(self):
        self.common_page.click_element(self.account_page.menu_icon())
        assert self.account_page.is_weekly_leaderboard_count(), "위클리 리더보드 카운트 ##+ 형식 노출 확인"
        
        self.common_page.click_element(self.account_page.weekly_leaderboard_count())
        assert self.common_page.is_visible(self.account_page.weekly_page_title()), "위클리 리더보드 페이지 노출 확인"


    def test_account_info(self):

        email: str = "daearcdo@gmail.com"
        phone: str = "+8201040681506"
        name: str = "kitae kim"
        level: str = "Level 2"

        self.common_page.click_element(self.account_page.menu_icon())
        self.account_page.click_support_menu("Password / Authentication")
        self.common_page.click_element(self.account_page.hide_info_button())
        assert self.common_page.is_visible(email), "이메일 노출 확인"
        assert self.common_page.is_visible(phone), "전화번호 노출 확인"
        assert self.common_page.is_visible(name), "이름 노출 확인"

        self.common_page.click_element(self.account_page.hide_info_button())
        self.logger.info(f"email: {email[:2]}***, phone: +82***{phone[-2:]}, name: {name[:2]}***{name[-2:]}, level: {level}")
        assert self.common_page.is_visible(email[:2]), "이메일 앞자리 2개 노출 확인"
        assert self.common_page.is_visible("+82"), "전화번호 +82 노출 확인"
        assert self.common_page.is_visible(phone[-2:]), "전화번호 뒷번호 2자리 노출 확인"
        assert self.common_page.is_visible(name[:2]), "이름 앞자리 2개 노출 확인"
        assert self.common_page.is_visible(name[-2:]), "이름 뒷자리 2개 노출 확인"
        assert self.common_page.is_visible(level), "레벨 노출 확인"

