import pytest
from page.common_page import CommonPage
from page.home_page import HomePage
from page.element_attribute_converter import ElementType, PropertyType
from appium.webdriver.common.appiumby import AppiumBy
import time

@pytest.mark.usefixtures("driver")
class TestApp:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.common_page = CommonPage(driver)
        self.home_page = HomePage(driver)

    def login_flow(self, driver):
        # iOS predicate 사용하 클릭
        self.common_page.click_element(ElementType.STATIC_TEXT, PropertyType.LABEL, "Trade")
        # ID 사용
        assert self.common_page.is_visible("order_form_text_field_no2_add_funds"), "Add funds 노출"
        # Add funds 클릭
        self.common_page.click_element("order_form_text_field_no2_add_funds")
        # OK 노출 확인 (강제 실패 유도)
        assert self.common_page.is_visible("OK"), "OK 노출"
        
    def scroll_and_swipe(self, driver):
        assert self.common_page.is_visible(ElementType.STATIC_TEXT, PropertyType.LABEL, "Verify identity now", timeout=10), "앱 실행 시 Verify identity now 노출"
        time.sleep(5)
        self.common_page.swipe("down")
        self.common_page.swipe("down")
        
        assert self.common_page.is_visible(ElementType.STATIC_TEXT, PropertyType.LABEL, "Trending categories", timeout=10), "Trending catgories 노출"

    def scroll_and_swipe2(self, driver):
        self.common_page.scroll_to_text("Trending categories")
        assert self.common_page.is_visible(ElementType.STATIC_TEXT, PropertyType.LABEL, "Trending categories", timeout=10), "Trending catgories 노출"

    def element_interactions(self, driver):
        reward_hub_text = self.common_page.get_text("tab_market_reward_hub")
        assert reward_hub_text == "Complete tasks and earn up to 150 USDT from reward hub", "Reward Hub 노출"
        self.common_page.click_element("search_icon")
        self.common_page.set_text("btc", ElementType.TEXT_FIELD)
        self.common_page.press_key("search")
        
        assert self.common_page.is_visible(ElementType.STATIC_TEXT, PropertyType.LABEL, "BTC", timeout=10), "BTC 노출"
        
    def test_regex_utility(self, driver):
        # reward_hub_text = self.common_page.get_text("tab_market_reward_hub")
        # assert reward_hub_text == "Complete tasks and earn up to 150 USDT from reward hub", "Reward Hub 노출"
        
        print(self.common_page.get_text_by_keyword("리워드문구"))
        assert self.common_page.get_text_by_keyword("리워드문구") == "Verify identity now", "리워드문구 노출"
        assert self.common_page.is_visible(ElementType.STATIC_TEXT, PropertyType.LABEL, self.common_page.get_text_by_keyword("코인수"))
        