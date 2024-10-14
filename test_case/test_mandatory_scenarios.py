import time
import pytest

from page.account_page import AccountPage
from page.assets_page import AssetsPage
from page.challenge_page import ChallengePage
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
        self.account_page = AccountPage(driver, os_type, rp_logger)
        self.os_type = os_type
        self.driver = driver
        self.logger = rp_logger
        
    def test_market_trade_normal(self):
        """
        High volume 내 가상화폐 리스트 데이터 유효성 검사
        총 20개의 각 코인별 데이터 추출 및 유효성 검사
        """
        self.market_page.click_market_button()

        # High volume 페이지로 이동
        self.market_page.swipe_to_title("High volume")
        self.market_page.click_see_all_button("High volume")
        time.sleep(3)

        # 코인 리스트 데이터 유효성 검사
        assert self.market_page.is_valid_coin_list(), "코인 데이터 유효성 검사"

    def test_challenge_event(self):
        """
        challenge 페이지 내 이벤트 노출 확인
        OS 차이로 iOS는 ID 기준으로 이벤트 날짜, 상태 추출,
        Android는 현재 화면의 Page source를 통해 이벤트 날짜 형태의 데이터 추출,
        이전 데이터와 비교하여 마지막 이벤트 정보인지 확인
        각 이벤트 날짜, 상태에 대한 유효성 검사
        """
        self.challenge_page.click_challenge_button()
        self.challenge_page.click_launch_airdrop_button()

        # 이벤트 정보 추출
        compare_date = self.challenge_page.get_event_info()
        assert compare_date, "이벤트 정상 노출 및 데이터 유효성 검사 확인"

    def test_assets(self):
        """
        로그아웃 후 Announcement 페이지 진입 시 챗봇 노출 확인
        iOS는 Native 형태로 접근 가능하나 Android는 WebView 형태로만 접근 가능
        해당 웹페이지의 휴먼 판독 해제 불가로 이슈 발생
        """

        self.login_page.logout()
        self.assets_page.click_assets_button()
        self.assets_page.click_setting_button()
        self.account_page.click_support_menu("Announcement")
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

    



