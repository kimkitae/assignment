
import re
import time
from page.common_page import CommonPage
from page.element_attribute_converter import ElementType, PropertyType, StringType
from page.execute_method import ExecuteMethod
from appium.webdriver.common.appiumby import AppiumBy

class MarketPage:
    def __init__(self, driver, os_type):
        self.driver = driver
        self.os_type = os_type
        self.common_page = CommonPage(driver, os_type)
        self.execute_method = ExecuteMethod(driver, os_type)

    """
    ========== Element 변수 ==========
    """
    def bottom_tab_market_button(self):
        if self.os_type == "ios":
            return ElementType.STATIC_TEXT, PropertyType.LABEL, "Market"
        else:
            return "market_button"
        
    def bottom_button_view_all_selections(self):
         if self.os_type == "ios":
            return "tab_view_all_selections"
         else:
            return "tab_view_all_selections"

    def see_all_button(self, title: str):
        title_name = title.replace(" ", "_").lower()
        if self.os_type == "ios":
            if title_name == "new_listings":
                return "carousel_no2_see_all"
            elif title_name == "top_movers":
                return "carousel_no3_see_all"
            elif title_name == "high_volume":
                return "carousel_no5_see_all"
            elif title_name == "high_funding_rates":
                return "carousel_no6_see_all"
            else:
                raise ValueError(f"해당 카테고리는 존재하지 않습니다. : {title}")
    
    def coin_list(self):
        if self.os_type == "ios":
            return ElementType.BUTTON, StringType.BEGINS, "carousel_no5_image"
        else:
            return "carousel_no5_image"

    """
    ========== 함수 변수 ==========
    """
     
    def click_market_button(self):
        locator = self.bottom_tab_market_button()
        self.common_page.click_element(locator)

    def swipe_to_view_all_selections(self):
        locator = self.bottom_button_view_all_selections()
        self.common_page.swipe_to_element(locator)

    def click_view_all_selections(self):
        self.swipe_to_view_all_selections()
        locator = self.bottom_button_view_all_selections()
        self.common_page.click_element(locator)

    def swipe_to_title(self, title: str):
        locator = self.see_all_button(title)
        self.common_page.swipe_to_element(locator)

    def click_see_all_button(self, title: str):
        self.swipe_to_title(title)
        locator = self.see_all_button(title)
        self.common_page.click_element(locator)

    def is_valid_coin_information(self):
        coins_data = self.gather_information_coin_lists()
        assert len(coins_data) > 0, "코인 데이터 1개이상 노출 확인"

        for coin_data in coins_data:
            is_valid = self.validata_coin_data(coin_data)
            print(f"코인 정보: {coin_data}, 일치 여부: {is_valid}")
            if not is_valid:
                return False
        return True


    def gather_information_coin_lists(self):
        coins_data = {}
        max_swipes = 5
        for _ in range(max_swipes):
            locator = self.coin_list()
            current_coins = self.get_current_coins_data(locator)
            for coin in current_coins:
                coin_name = coin.split(",")[0].strip()
                coins_data[coin_name] = coin

            if len(coins_data) >= 20:
                break

            self.common_page.swipe("down")
            time.sleep(1)

        return list(coins_data.values())

    def get_current_coins_data(self, locator):
        elements = self.common_page.find_elements(locator)
        return [element.get_attribute('label') for element in elements]

    def validata_coin_data(self, coin_data):
        # 정규식 패턴 가져오기
        patterns = self.common_page.get_text_by_keyword("코인리스트정보") 
        
        # 데이터를 콤마로 분리한 후 각 항목의 공백을 제거
        fields = [field.strip() for field in re.split(r',\s*(?!\d)', coin_data)]  # 콤마로 분리하되 숫자의 콤마는 유지

        # # 패턴과 데이터 필드 수가 일치하는지 확인
        if len(fields) != len(patterns):
            print(f"패턴 수와, 실제 데이터 필드 수가 일치 하지 않습니다. Patterns: {len(patterns)}, Fields: {len(fields)}")
            return False
        
        # 각 필드가 정규식 패턴에 맞는지 검사
        for pattern, field in zip(patterns, fields):
            if not re.match(pattern, field):
                print(f"'{field}' 와 '{pattern}' 이 일치하지 않습니다.")
                return False
        return True



