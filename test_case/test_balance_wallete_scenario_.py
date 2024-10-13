import time
import pytest

from page.assets_page import AssetsPage
from page.challenge_page import ChallengePage
from page.earn_page import EarnPage
from page.etc_page import EtcPage
from helper.execute_method import ExecuteMethod
from page.market_page import MarketPage
from page.common_page import CommonPage
from page.login_page import LoginPage

from helper.element_attribute_converter import ElementType, PropertyType, StringType

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
        self.earn_page = EarnPage(driver, os_type, rp_logger)
        self.os_type = os_type
        self.logger = rp_logger

        
    def test_heck_asset_portfolio(self):
        self.common_page.click_element(self.assets_page.bottom_tab_assets_button())
        balance_title = self.common_page.get_text(self.assets_page.portfolio_balance_title())
        balance_value = self.common_page.get_text(self.assets_page.portfolio_balance_value())
        assert balance_title == "Portfolio balance", "Portfolio balance 타이틀 노출 확인"
        assert balance_value == "0.00%", "0.00% 노출 확인"
        self.logger.info(f"Portfolio balance 타이틀 : {balance_title} / Portfolio balance 값 : {balance_value}")

        self.common_page.click_element(self.assets_page.portfolio_balance_value())
        assert self.assets_page.is_portfolio_detail_lists(), "Portfolio 상세 정보 노출 확인"
    
    def test_deposit_crypto(self):
        self.common_page.click_element(self.assets_page.bottom_tab_assets_button())
        self.common_page.click_element(self.assets_page.deposit_button())

        assert self.assets_page.is_valid_deposit_crypto_list(), "assets 리스트 데이터 유효성 검사"

    def test_withdraw_no_list(self):
        self.common_page.click_element(self.assets_page.bottom_tab_assets_button())
        self.common_page.click_element(self.assets_page.withdraw_button())
        assert self.common_page.is_visible(self.assets_page.withdraw_no_list_content()), "빈 리스트 노출"
        self.logger.info("출금 빈 리스트 노출 확인")

    def test_postions_open_pending(self):
        self.common_page.click_element(self.assets_page.bottom_tab_assets_button())
        self.common_page.swipe_to_element(self.assets_page.your_assets_title())
        
        self.common_page.click_element(self.assets_page.open_positions_button())
        open_positions_description = self.common_page.get_text(self.assets_page.positions_open_description())
        assert open_positions_description == "All effective orders and contracts you possess show here.", "positions open 설명 노출"
        self.logger.info(f"positions open 설명 문구 노출 : {open_positions_description}")
        time.sleep(1)

        self.common_page.click_element(self.assets_page.pending_positions_button())
        time.sleep(1)
        pending_positions_description = self.common_page.get_text(self.assets_page.positions_pending_description())
        assert pending_positions_description == "When you place a trigger order, orders that are still awaiting execution show here.", "positions pending 설명 노출"
        self.logger.info(f"positions pending 설명 문구 노출 : {pending_positions_description}")
        
    def test_your_assets(self):
        self.common_page.click_element(self.assets_page.bottom_tab_assets_button())
        self.common_page.swipe_to_element(self.assets_page.your_assets_value())
        self.common_page.swipe("down")
        your_assets_title = self.common_page.get_text(self.assets_page.your_assets_title())
        your_assets_value = self.common_page.get_text(self.assets_page.your_assets_value())
        usdt_bouns_value = self.common_page.get_text(self.assets_page.bottom_usdt_bouns_value())
        assert your_assets_title == "Your assets", "assets 타이틀 노출"
        assert your_assets_value == "0.00", "assets 0.00 확인"

        if self.os_type == "ios":
            assert usdt_bouns_value == "0,  USDT", "USDT 보너스 금액 노출"
        else:
            assert usdt_bouns_value == "0.00", "USDT 보너스 금액 노출"

        self.logger.info(f"assets 타이틀 : {your_assets_title} / assets 값 : {your_assets_value} / USDT 보너스 금액 : {usdt_bouns_value}")
        

    def test_earn(self):
        self.common_page.click_element(self.earn_page.bottom_tab_earn_button())
        self.common_page.click_element(self.earn_page.earn_way_to_no_button())

        self.earn_page.set_default_first_network()
        time.sleep(1)

        assert self.common_page.is_visible(self.earn_page.deposit_address()), "주소 노출 확인"
        assert self.common_page.is_visible(self.earn_page.deposit_memo_value()), "메모 노출 확인"
        self.logger.info("주소 노출 확인 / 메모 노출 확인")

        self.earn_page.change_network_button(1)
        time.sleep(1)
        assert self.common_page.is_visible(self.earn_page.deposit_memo_value(), timeout=1) == False, "메모 값 비노출 확인"
        self.logger.info("메모 값 비노출 확인")
        self.common_page.click_element(self.earn_page.deposit_copy_address_button())
        time.sleep(1)
        assert self.earn_page.validate_toast_message(), "복사 토스트 메시지 노출 확인"
        