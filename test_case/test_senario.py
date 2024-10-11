import time
import pytest

from page.assets_page import AssetsPage
from page.challenge_page import ChallengePage
from page.etc_page import EtcPage
from page.execute_method import ExecuteMethod
from page.market_page import MarketPage
from page.common_page import CommonPage
from page.login_page import LoginPage
from page.element_attribute_converter import ElementType, PropertyType, StringType

class TestSenario:
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, os_type):
        self.common_page = CommonPage(driver, os_type)
        self.login_page = LoginPage(driver, os_type)
        self.market_page = MarketPage(driver, os_type)
        self.challenge_page = ChallengePage(driver, os_type)
        self.assets_page = AssetsPage(driver, os_type)
        self.etc_page = EtcPage(driver, os_type)
        self.execute_method = ExecuteMethod(driver, os_type)
    
    # 로그인 정상 여부 확인
    def login_normal(self):
        assert self.login_page.check_signed_up(), "로그인 정상 여부 확인"

    # Test Case 1: High volume 카테고리 코인 데이터 유효성 검사
    def test_market_trade_normal(self):
        self.market_page.click_market_button()
        self.market_page.swipe_to_title("High volume")
        self.market_page.click_see_all_button("High volume")
        time.sleep(3)

        assert self.market_page.is_valid_coin_information(), "코인 데이터 유효성 검사"

    def test_challenge_event(self):
        self.challenge_page.click_challenge_button()
        self.challenge_page.click_launch_airdrop_button()
        compare_date = self.challenge_page.get_event_info()
        assert compare_date, "이벤트 정상 노출 및 데이터 유효성 검사 확인"

    def test_assets(self):
        self.login_page.logout()
        self.assets_page.click_assets_button()
        self.login_page.click_setting_icon()
        self.login_page.click_support_menu("Announcement")
        time.sleep(5)
        self.etc_page.click_open_messaging_windows()
        time.sleep(5)
        assert self.etc_page.is_visible_chatbot(), "챗봇 노출 확인"
        self.etc_page.click_close_messaging_windows()
        self.execute_method.activate_app()
        assert self.common_page.is_visible("account_main_title"), "Account"

    



