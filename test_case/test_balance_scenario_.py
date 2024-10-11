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

class TestScenario:
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, os_type):
        self.common_page = CommonPage(driver, os_type)
        self.login_page = LoginPage(driver, os_type)
        self.market_page = MarketPage(driver, os_type)
        self.challenge_page = ChallengePage(driver, os_type)
        self.assets_page = AssetsPage(driver, os_type)
        self.etc_page = EtcPage(driver, os_type)
        self.execute_method = ExecuteMethod(driver, os_type)
    

    """
    1. 잔고 확인
    assets 진입 후 portfoli 발란스 정보 확인
    3. 디파짓 크립토, 출금, 변환 버튼 동작
    2. your positions 변경 적용 여부
    4. toal value 0.00USDT
    Convert to USDT 버튼 동작 확인
    

    """
    def test_market_trade_normal(self):





