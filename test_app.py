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
        
    def test_scroll_and_swipe(self, driver):
        assert self.common_page.is_visible(ElementType.BUTTON, PropertyType.LABEL, "Verify", timeout=10), "Verify 노출"
        self.common_page.swipe("up")

        self.common_page.scroll_to_text("Trending catgories")
        assert self.common_page.is_visible(ElementType.STATIC_TEXT, PropertyType.LABEL, "Trending catgories", timeout=10), "Trending catgories 노출"

        # 앱 실행


    def element_interactions(self, driver):
        # 앱 실행

        # 요소 클릭
        menu_button = self.common_page.create_ios_predicate(ElementType.BUTTON, PropertyType.NAME, "메뉴")
        self.common_page.click_element("ios_predicate", menu_button)

        # 텍스트 입력
        search_field = self.common_page.create_ios_predicate(ElementType.SEARCH_FIELD, PropertyType.NAME, "검색")
        self.common_page.set_text("ios_predicate", search_field, "테스트 검색어")

        # 텍스트 가져오기
        result_text = self.common_page.create_ios_predicate(ElementType.STATIC_TEXT, PropertyType.NAME, "검색 결과")
        text = self.common_page.get_text("ios_predicate", result_text)
        print(f"검색 결과: {text}")

        # 요소 대기
        loading_indicator = self.common_page.create_ios_predicate(ElementType.OTHER, PropertyType.NAME, "로딩 중")
        self.common_page.wait_for_element("ios_predicate", loading_indicator, timeout=10)

        # 요소 가시성 확인
        no_results = self.common_page.create_ios_predicate(ElementType.STATIC_TEXT, PropertyType.NAME, "결과 없음")
        assert not self.common_page.is_element_visible("ios_predicate", no_results), "검색 결과가 없습니다."
