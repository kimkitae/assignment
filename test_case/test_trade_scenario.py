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
    

    def test_market_trade_normal(self):




