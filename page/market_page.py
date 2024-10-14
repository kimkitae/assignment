import re
import time
from helper.regex_utility import RegexUtility
from page.common_page import CommonPage
from helper.element_attribute_converter import ElementType, PropertyType, StringType, AndroidElementType
from helper.execute_method import ExecuteMethod
from appium.webdriver.common.appiumby import AppiumBy


class MarketPage:
    """
    MarketPage 클래스는 Market 관련 정보와 동작을 관리하는 클래스입니다.
    """

    def __init__(self, driver, os_type, rp_logger):
        self.logger = rp_logger
        self.driver = driver
        self.os_type = os_type
        self.common_page = CommonPage(driver, os_type, rp_logger)
        self.execute_method = ExecuteMethod(driver, os_type, rp_logger)
        self.regex_utility = RegexUtility(driver, os_type, rp_logger)

    """
    ========= 객체 반환 함수 =========
    """

    # Market 버튼
    def bottom_tab_market_button(self):
        if self.os_type == "ios":
            return ElementType.STATIC_TEXT, PropertyType.LABEL, "Market"
        else:
            return "tab_market"

    # 가장 하단 view all selections 버튼
    def bottom_button_view_all_selections(self):
        return "tab_view_all_selections"

    # See all buton
    def see_all_button(self, title: str):
        # 진입 할 See all Button의 타이틀 명 입력
        title_name = title.replace(" ", "_").lower()
        if title_name == "new_listings":
            return "carousel_no2_see_all"
        elif title_name == "top_movers":
            return "carousel_no3_see_all"
        elif title_name == "high_volume":
            return "carousel_no5_see_all"
        elif title_name == "high_funding_rates":
            return "carousel_no6_see_all"
        else:
            self.logger.info(f"해당 카테고리는 존재하지 않습니다. : {title}")
            raise ValueError(f"해당 카테고리는 존재하지 않습니다. : {title}")

    # Coin 데이터 리스트
    def coin_list(self):
        if self.os_type == "ios":
            return ElementType.BUTTON, StringType.BEGINS, "carousel_no5_image"
        else:
            return "carousel_no5_image"

    # 검색 버튼
    def search_icon(self):
        return "search_icon"

    # 검색 입력 필드
    def search_input(self):
        if self.os_type == "ios":
            return "text_field"
        else:
            return AndroidElementType.EDIT_TEXT

    # 검색 결과 내 코인 이름 영역
    def search_result_coin_name(self):
        return "searched_product_ticker_"

    # 알림 버튼
    def notification_button(self):
        return "notification_icon"

    """
    ========= 기능 함수 ===========
    """
     
    def click_market_button(self):
        """
        Market 버튼 클릭
        """
        locator = self.bottom_tab_market_button()
        self.common_page.click_element(locator)

    def swipe_to_view_all_selections(self):
        """
        view all selections 버튼 보일때까지 스와이프
        """
        locator = self.bottom_button_view_all_selections()
        self.common_page.swipe_to_element(locator)

    def click_view_all_selections(self):
        """
        view all selections 스와이프 및 클릭
        """
        self.swipe_to_view_all_selections()
        locator = self.bottom_button_view_all_selections()
        self.common_page.click_element(locator)

    def swipe_to_title(self, title: str):
        """
        해당 타이틀 찾을때까지 스와이프
        """
        locator = self.see_all_button(title)
        self.common_page.swipe_to_element(locator)

    def click_see_all_button(self, title: str):
        """
        해당 타이틀의 see all button 클릭
        """

        self.swipe_to_title(title)
        locator = self.see_all_button(title)
        self.common_page.click_element(locator)

    def is_search_result_coin(self, search_keyword: str):
        """
        검색어 에 대한 결과 내 해당 코인 노출 확인
        """
        locator = self.search_result_coin_name() + search_keyword
        self.logger.info(f"검색 결과 코인 이름 : {self.common_page.get_text(locator)}")
        return self.common_page.is_visible(locator)


    def get_text_coin_up_and_down(self):
        """
        Market 내 Coins are up, Coins are down 노출 및 데이터 유효성 확인
        """
        time.sleep(2)
        if self.os_type == "ios":
            # 각 up, down 정규식 패턴에 포함되는 데이터 노출 확인
            coin_up_count = self.common_page.get_text_by_keyword("코인up")
            coin_down_count = self.common_page.get_text_by_keyword("코인down")
            self.logger.info(f"UP: {coin_up_count}, DOWN: {coin_down_count}")
        else :
            # 카운트와 문자가 분리되어있어, 문자의 부모요소에서 카운트 부분을 추출하여 0 Coins are up 과 같이 단어로 조립하여 검증
            coins_up_number_element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Coins are up").fromParent(new UiSelector().className("android.widget.TextView"))')
            coins_up_number = coins_up_number_element.get_attribute('text')
            coin_up_count = f"{coins_up_number} Coins are up"

            coins_down_number_element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Coins are down").fromParent(new UiSelector().className("android.widget.TextView"))')            
            coins_down_number = coins_down_number_element.get_attribute('text')
            coin_down_count = f"{coins_down_number} Coins are down"

            self.logger.info(f"UP: {coin_up_count}, DOWN: {coin_down_count}")
        
        up_count = int(coin_up_count.split()[0])
        down_count = int(coin_down_count.split()[0])

        return up_count, down_count 

    def is_valid_coin_list(self):
        """

        """
        time.sleep(3)

        coin_data = self.gather_information_coin_lists()
        
        assert len(coin_data) >= 20, "데이터가 20개 이상 노출 확인"
        self.logger.info(f"{len(coin_data)} 개의 데이터가 노출되었습니다.")
        
        unique_coins = set()
        for coin in coin_data[:20]:
            if self.os_type == "ios":
                fields = [field.strip() for field in re.split(r',\s*(?!\d)', coin)]
                coin_name = fields[0]
            else:
                coin_name = coin['name']

            if coin_name in unique_coins:
                self.logger.info(f"{coin_name}은 중복되었습니다.")
                return False
            unique_coins.add(coin_name)
            
            is_valid = self.validate_coin_data(coin)
            self.logger.info(f"coin 정보: {coin}, 일치 여부: {is_valid}")
            if not is_valid:
                return False
        return True

    def gather_information_coin_lists(self):
        coins_data = []
        unique_coins = set()
        for _ in range(5):
            current_coins = self.get_current_coin_data(self.coin_list())
            for asset in current_coins:
                if self.os_type == "ios":
                    coin_name = asset.split(",")[0].strip()
                else:
                    coin_name = asset['name']

                if coin_name not in unique_coins:
                    coins_data.append(asset)
                    unique_coins.add(coin_name)
                    if len(coins_data) >= 20:
                        return coins_data[:20]
            
            self.common_page.swipe("down")
            time.sleep(1)  # 스와이프 후 화면 로딩 대기

        return coins_data[:20]  # 20개 미만일 경우 수집된 모든 자산 반환

    def get_current_coin_data(self, locator):
        if self.os_type == "ios":
            elements = self.common_page.find_elements(locator)
            return [element.get_attribute('label') for element in elements]
        else:
            coins = []
            ticker_elements = self.common_page.find_elements("uiautomator", 'new UiSelector().descriptionStartsWith("carousel_no5_ticker_")')
            leverage_elements = self.common_page.find_elements("uiautomator", 'new UiSelector().descriptionStartsWith("carousel_no5_leverage_")')
            price_elements = self.common_page.find_elements("uiautomator", 'new UiSelector().descriptionStartsWith("carousel_no5_price_")')
            fluctuation_elements = self.common_page.find_elements("uiautomator", 'new UiSelector().descriptionStartsWith("carousel_no5_fluctuation_")')



            self.logger.info(f"현재 화면에 {len(ticker_elements)}개의 코인이 있습니다.")

            for index, element in enumerate(ticker_elements):
                # 코인명 (BTC, ETH 등)
                coin_name:str = element.get_attribute('text')
                
                # 레버리지 값 가져오기 (부모 요소에서 하위 요소 추출)
                leverage_view = leverage_elements[index]
                leverage_text = leverage_view.find_element(AppiumBy.CLASS_NAME, "android.widget.TextView").get_attribute('text')

                # 가격 정보 가져오기
                price_view = price_elements[index]
                price_text = price_view.find_element(AppiumBy.CLASS_NAME, "android.widget.TextView").get_attribute('text')

                # 변동률 정보 가져오기
                fluctuation_view = fluctuation_elements[index]
                fluctuation_text = fluctuation_view.find_element(AppiumBy.CLASS_NAME, "android.widget.TextView").get_attribute('text')

                 # 부모 요소에서 추가 정보 가져오기 (필요시)
                volume_element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{coin_name}").fromParent(new UiSelector().className("android.widget.TextView").instance(2))')
                volume_text = volume_element.get_attribute('text')

                # 중복 제거를 위한 set 생성
                unique_coins = set()

                # 코인 정보를 문자열로 변환하여 set에 추가
                asset_info = f"{coin_name},{leverage_text},{volume_text},{price_text},{fluctuation_text}"
                if asset_info not in unique_coins:
                    unique_coins.add(asset_info)
                    coins.append({
                        'name': coin_name,
                        'leverage': leverage_text,
                        'volume': volume_text,
                        'price': price_text,
                        'fluctuation': fluctuation_text
                    })

            return coins

    def validate_coin_data(self, asset):
        """
        코인 데이터에 대한 유효성 검증
        """

        patterns = {
            "coin_data": [
                r'^[A-Z0-9]+$',  # 코인 이름 (BTC)
                r'^\d+x$',  # 레버리지 (100x)
                r'^\d+(\.\d+)?[MK]$',  # 시가총액 (202.89M)
                r'^\d{1,3}(,\d{3})*(\.\d+)?$',  # 가격 (60,995.3)
                r'^-?\d+(\.\d+)?%$'  # 변동률 (1.99%)
            ]}

        if self.os_type == "ios":
            # , 단위로 자르나 , 뒤에 숫자 있는 경우 건너띈다 (44,555 같은 경우)
            fields = [field.strip() for field in re.split(r',\s*(?!\d)', asset)]
        else:
            fields = [
                asset['name'],
                asset['leverage'],
                asset['volume'],
                asset['price'],
                asset['fluctuation']
            ]

        # 필드수와 패턴의 수 일치 여부 확인
        if len(fields) != len(patterns["coin_data"]):
            self.logger.info(f"패턴 수와, 실제 데이터 필드 수가 일치하지 않습니다. Patterns: {len(patterns['coin_data'])}, Fields: {len(fields)}")
            return False

        # 필드 별 데이터와 정규식 패턴 일치 여부 확인
        for pattern, field in zip(patterns["coin_data"], fields):
            if not re.match(pattern, field):
                self.logger.info(f"'{field}'와 '{pattern}'이 일치하지 않습니다.")
                return False

        return True