import time
import pytest

from page.account_page import AccountPage
from helper.execute_method import ExecuteMethod
from page.common_page import CommonPage
from page.login_page import LoginPage
from helper.element_attribute_converter import ElementType, PropertyType, StringType

class TestScenario:
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, os_type, rp_logger):
        self.common_page = CommonPage(driver, os_type, rp_logger)
        self.login_page = LoginPage(driver, os_type, rp_logger)
        self.account_page = AccountPage(driver, os_type, rp_logger)
        self.execute_method = ExecuteMethod(driver, os_type, rp_logger)
        self.logger = rp_logger


    def test_change_nickname(self):
        """
        Menu icon 클릭 후 닉네임 정상 노출 및 변경 확인
        """
        self.common_page.click_element(self.account_page.menu_icon())

        current_nickname = self.account_page.account_nickname_text()
        assert self.account_page.change_nickname(self.account_page.generate_random_nickname(current_nickname)), "닉네임 변경 확인"
        self.logger.info("닉네임 변경 확인")

    def test_weekly_leaderboard(self):
        """
        위클리 리더 보드 노출 및 페이지 진입 확인
        """
        self.common_page.click_element(self.account_page.menu_icon())
        assert self.account_page.is_weekly_leaderboard_count(), "위클리 리더보드 카운트 ##+ 형식 노출 확인"
        
        self.common_page.click_element(self.account_page.weekly_leaderboard_count())
        assert self.common_page.is_visible(self.account_page.weekly_page_title()), "위클리 리더보드 페이지 노출 확인"


    def test_account_info(self):
        """
        계정 정보 정상 노출 및 마스킹 정상 처리 확인
        """

        self.common_page.click_element(self.account_page.menu_icon())
        self.account_page.click_support_menu("Password / Authentication")
        # 마스킹 처리 해제
        self.common_page.click_element(self.account_page.hide_info_button())
        time.sleep(3)
        
        # 계정 정보 노출 확인
        assert self.common_page.is_visible(self.account_page.get_account_info("email")), "이메일 노출 확인"
        assert self.common_page.is_visible(self.account_page.get_account_info("phone")), "전화번호 노출 확인"
        assert self.common_page.is_visible(self.account_page.get_account_info("name")), "이름 노출 확인"
        assert self.common_page.is_visible(self.account_page.get_account_info('level')), "레벨 노출 확인"

        # 마스킹 처리
        self.common_page.click_element(self.account_page.hide_info_button())
        time.sleep(3)

        # 계정 정보 마스킹 처리
        masked_info, masked_element = self.account_page.get_masked_account_info()
        self.logger.info(f"email: {masked_info['email']}, phone: {masked_info['phone_first']}***{masked_info['phone_last']}, name: {masked_info['name_first']}***{masked_info['name_last']}")

        # 마스킹 처리된 계정 정보 노출 확인
        assert self.common_page.is_visible(masked_element['email']), "이메일 앞자리 2개 노출 확인"
        assert self.common_page.is_visible(masked_element['phone_first']), "전화번호 앞자리 3자리 노출 확인"
        assert self.common_page.is_visible(masked_element['phone_last']), "전화번호 뒷번호 2자리 노출 확인"
        assert self.common_page.is_visible(masked_element['name_first']), "이름 앞자리 2개 노출 확인"
        assert self.common_page.is_visible(masked_element['name_last']), "이름 뒷자리 2개 노출 확인"

