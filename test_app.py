import time
import pytest
from page.common_page import CommonPage
from page.home_page import HomePage
from page.element_attribute_converter import ElementType, PropertyType


@pytest.mark.usefixtures("driver")
class TestApp:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.common_page = CommonPage(driver)
        self.home_page = HomePage(driver)

    def test_move_trade_fail_forcely(self, driver):
        # iOS predicate 사용하여 클릭
        self.common_page.click_element(ElementType.STATIC_TEXT, PropertyType.LABEL, "Trade")
        # ID 사용하여 오브젝트 노출 확인 
        assert self.common_page.is_visible("order_form_text_field_no2_add_funds"), "Add funds 노출"
        # ID 사용하여 클릭
        self.common_page.click_element("order_form_text_field_no2_add_funds")
        # OK 노출 확인 (강제 실패 유도)
        assert self.common_page.is_visible("OK"), "OK 노출"
        
    def test_scroll_and_swipe1(self, driver):
        # 앱 실행 시 Verify identity now 노출 확인
        assert self.common_page.is_visible(ElementType.STATIC_TEXT, PropertyType.LABEL, "Verify identity now", timeout=10), "앱 실행 시 Verify identity now 노출"
        time.sleep(5)
        # 아래로 스와이프 2번 수행
        self.common_page.swipe("down")
        self.common_page.swipe("down")
        
        assert self.common_page.is_visible(ElementType.STATIC_TEXT, PropertyType.LABEL, "Trending categories", timeout=10), "Trending catgories 노출"

    def test_scroll_and_swipe2(self, driver):
        # Trending categories 노출 할때까지 스와이프
        self.common_page.scroll_to_text("Trending categories")
        # Trending categories 노출 확인
        assert self.common_page.is_visible(ElementType.STATIC_TEXT, PropertyType.LABEL, "Trending categories", timeout=10), "Trending catgories 노출"

    def test_element_interactions(self, driver):
        # tab_market_reward_hub ID의 오브젝트의 Text 값 가져오기
        reward_hub_text = self.common_page.get_text("tab_market_reward_hub")
        # Complete tasks and earn up to 150 USDT from reward hub 노출 확인
        assert reward_hub_text == "Complete tasks and earn up to 150 USDT from reward hub", "Reward Hub 노출"
        # search_icon 클릭
        self.common_page.click_element("search_icon")
        # 검색창에 btc 입력 후 검색 버튼 클릭
        self.common_page.set_text("btc", ElementType.TEXT_FIELD)
        self.common_page.press_key("search")
        # BTC 노출 확인
        assert self.common_page.is_visible(ElementType.STATIC_TEXT, PropertyType.LABEL, "BTC", timeout=10), "BTC 노출"
        
    def test_regex_utility(self, driver):
        # 리워드문구(Verify identity now) 패턴의 정규식 문구 노출 확인
        assert self.common_page.get_text_by_keyword("리워드문구") == "Verify identity now", "리워드문구 노출"
        # 코인수(10) 패턴의 정규식 문구 노출 확인
        assert self.common_page.is_visible(ElementType.STATIC_TEXT, PropertyType.LABEL, self.common_page.get_text_by_keyword("코인수"))
        