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
    Notification 정상 랜딩
    

    2. price Alerts 이 두번 눌러야 상태 변경 (UX 개선 필요)
    3. 검색 화면 정상 노출 확인
    4. 검색을 통한 상세 트레이드 화면 노출
    5. earn 진입 후 디파짓 동작 확인
    history 
    """
    def test_market_trade_normal(self):




