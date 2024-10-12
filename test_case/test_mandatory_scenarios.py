import time
import pytest

from page.assets_page import AssetsPage
from page.challenge_page import ChallengePage
from page.etc_page import EtcPage
from helper.execute_method import ExecuteMethod
from page.market_page import MarketPage
from page.common_page import CommonPage
from page.login_page import LoginPage
from page.element_attribute_converter import ElementType, PropertyType, StringType

class TestScenario:
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, os_type, rp_logger):
        self.common_page = CommonPage(driver, os_type, rp_logger)
        self.login_page = LoginPage(driver, os_type, rp_logger)
        self.market_page = MarketPage(driver, os_type, rp_logger)
        self.challenge_page = ChallengePage(driver, os_type, rp_logger)
        self.assets_page = AssetsPage(driver, os_type, rp_logger)
        self.etc_page = EtcPage(driver, os_type, rp_logger)
        self.execute_method = ExecuteMethod(driver, os_type, rp_logger)
        self.logger = rp_logger
    # Test Case 1: High volume 카테고리 코인 데이터 유효성 검사
    def test_market_trade_normal(self):
        self.market_page.click_market_button()
        self.market_page.swipe_to_title("High volume")
        self.market_page.click_see_all_button("High volume")
        time.sleep(3)

        assert self.market_page.is_valid_coin_information(), "코인 데이터 유효성 검사"

    # Test Case 2: Challenge 이벤트 데이터 유효성 검사
    def test_challenge_event(self):
        self.challenge_page.click_challenge_button()
        self.challenge_page.click_launch_airdrop_button()
        compare_date = self.challenge_page.get_event_info()
        assert compare_date, "이벤트 정상 노출 및 데이터 유효성 검사 확인"

    # Test Case 3: Assets 화면 정상 노출 확인
    def test_assets(self):
        self.login_page.logout()
        self.assets_page.click_assets_button()
        self.login_page.click_setting_icon()
        self.login_page.click_support_menu("Announcement")
        self.logger.info("Announcement 선택 후 웹페이지 로딩을 위해 5초 대기")
        time.sleep(5)
        self.etc_page.click_open_messaging_windows()
        self.logger.info("open messaging windows 선택 후 챗봇 불러오기 위해 5초 대기")
        time.sleep(5)
        assert self.etc_page.is_visible_chatbot(), "챗봇 노출 확인"
        self.logger.info("챗봇 노출 확인 후 챗봇 닫기 버튼 선택")
        self.etc_page.click_close_messaging_windows()
        self.execute_method.activate_app()
        self.logger.info("앱 전환 후 Account 화면 정상 노출 확인")
        assert self.common_page.is_visible(self.login_page.account_main_title()), "Account 화면 정상 노출 확인"

    



