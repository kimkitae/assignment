import time
import pytest

from page.challenge_page import ChallengePage
from page.market_page import MarketPage
from page.common_page import CommonPage
from page.home_page import HomePage
from page.login_page import LoginPage
from page.element_attribute_converter import ElementType, PropertyType, StringType

class TestSenario:
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, os_type):
        self.common_page = CommonPage(driver, os_type)
        self.home_page = HomePage(driver, os_type)
        self.login_page = LoginPage(driver, os_type)
        self.market_page = MarketPage(driver, os_type)
        self.challenge_page = ChallengePage(driver, os_type)
    
    # 로그인 정상 여부 확인
    def login_normal(self, driver):
        assert self.login_page.check_signed_up(), "로그인 정상 여부 확인"

    # Test Case 1: High volume 카테고리 코인 데이터 유효성 검사
    def market_trade_normal(self, driver):
        self.market_page.click_market_button()
        self.market_page.swipe_to_title("High volume")
        self.market_page.click_see_all_button("High volume")
        time.sleep(3)

        coins_data = self.market_page.gather_information_coin_lists(ElementType.BUTTON, StringType.BEGINS, "carousel_no5_image")
        assert len(coins_data) > 0, "코인 데이터 1개이상 노출 확인"

        for coin_data in coins_data:
            is_valid = self.market_page.validata_coin_data(coin_data)
            print(f"코인 정보: {coin_data}, 일치 여부: {is_valid}")
            assert is_valid, f"유효하지 않은 코인 데이터: {coin_data}"

    def test_challenge_event(self, driver):
        self.challenge_page.click_challenge_button()
        self.challenge_page.click_launch_airdrop_button()
        compare_date = self.challenge_page.get_event_info()
        assert compare_date, "이벤트 정상 노출 및 데이터 유효성 검사 확인"

