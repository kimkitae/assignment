import time
import pytest
import logging
from page.assets_page import AssetsPage
from page.challenge_page import ChallengePage
from page.etc_page import EtcPage
from helper.execute_method import ExecuteMethod
from page.market_page import MarketPage
from page.common_page import CommonPage
from page.login_page import LoginPage
from reportportal_client import RPLogger, RPLogHandler
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

        self.logger = rp_logger
    
    def test_validate_coin_up_down_count(self):
        """
        Market 화면 내 # Coins are up, # Coins are down 데이터 유효성 검사
        iOS는 현재 화면의 Page source 에서 정규식을 이용하여 검사
        Android는 카운트 영역, coins are up&down 영역이 별도이기 때문에 각각의 데이터를 가져와
        iOS와 동잉한 문자열로 조합 후 정규식을 이용하여 검사
        """
        self.market_page.click_market_button()
        up_coin_count, coin_down_count = self.market_page.get_text_coin_up_and_down()

        # 추출한 카운트 들이 0보다 같거나 높은지 확인
        assert up_coin_count >= 0, f"코인 상승 수가 0보다 같거나 높습니다.: {coin_down_count}"
        assert coin_down_count >= 0, f"코인 하락 수가 0보다 같거나 높습니다.: {coin_down_count}"


    def test_search_function(self):
        """
        Market 화면 내 검색 기능을 통해 유효한 검색결과 노출 여부 확인
        """
        self.common_page.click_element(self.market_page.search_icon())
        self.common_page.set_text("btc", self.market_page.search_input())

        assert self.market_page.is_search_result_coin("btc"), "검색 결과 코인 노출 확인"

    def test_notification_function(self):
        """
        알림창 진입 후 정상 노출 확인
        알림창 내 Promostion 및 System 알림를 정규식으로 추출하여 
        현재 페이지 이상없음을 확인
        """
        self.common_page.click_element(self.market_page.notification_button())
        notification_type = self.common_page.get_text_by_keyword("알림종류")
        self.logger.info(f"알림 종류 : {notification_type}")
        assert notification_type == "Promotions" or notification_type == "System", "알림 센터 내 알림 종류 노출 확인"