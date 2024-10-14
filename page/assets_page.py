import re
import time
from page.common_page import CommonPage
from helper.element_attribute_converter import AndroidPropertyType, ElementType, PropertyType, StringType
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException

class AssetsPage:
    """
    AssetsPage 클래스는 Assets 화면 내 동작을 관리하는 클래스입니다.
    """

    def __init__(self, driver, os_type, rp_logger):
        self.driver = driver
        self.os_type = os_type
        self.common_page = CommonPage(driver, os_type, rp_logger)
        self.logger = rp_logger

    
    """
    ========= 객체 반환 함수 =========
    """

    # Assets 버튼
    def bottom_tab_assets_button(self):
        if self.os_type == "ios":
            return ElementType.STATIC_TEXT, PropertyType.LABEL, "Assets"
        else:
            return AndroidPropertyType.TEXT, "Assets"

    # Portfolio 제목
    def portfolio_balance_title(self):
            return "assets_title_no1"

    # Portfolio 값
    def portfolio_balance_value(self):
            return "assets_title_no1_value_no2"

    # Deposit Button
    def deposit_button(self):
        if self.os_type == "ios":
            return "tab_deposit"
        else:
            return AndroidPropertyType.TEXT, "Deposit crypto"

    # Deposit 내 코인 리스트
    def assets_list(self):
        if self.os_type == "ios":
            return ElementType.BUTTON, StringType.BEGINS, "prex_receive_full_"
        else:
            return "carousel_no5_image"

    # withdraw 버튼
    def withdraw_button(self):
            return "tab_withdraw"

    # Open position 버튼
    def open_positions_button(self):
        if self.os_type == "ios":
            return "tab_yp_open"
        else:
            return "tab_order_form_positions_open"

    # Pending position 버튼
    def pending_positions_button(self):
        if self.os_type == "ios":
            return "tab_yp_pending"
        else:
            return AndroidPropertyType.TEXT, "Pending"

    # Open Position 설명문
    def positions_open_description(self):
            return "positions_open_description"

    # Pending Position 설명문
    def positions_pending_description(self):
            return "positions_pending_description"

    # your assets 제목
    def your_assets_title(self):
            return "assets_title_no3"

    # your asstes 보유양
    def your_assets_value(self):
            return "assets_ya_value_no1"

    # assets 최 하단 USDT Bouns
    def bottom_usdt_bouns_value(self):
        if self.os_type == "ios":
            return ElementType.BUTTON, StringType.BEGINS,  "assets_ya_name_usdt_bonus"
        else:
            return AndroidPropertyType.TEXT, "0.00", 2

    # portfolio 상세 타이틀
    def portfolio_detail_titles(self):
            return ["Unrealized P&L", "Net funding fee", "Funds invested", "Funds reserved", "Available funds"]

    #  portfolio 상세 값
    def portfolio_detail_values(self):
            return ["assets_pb_value_no1", "assets_pb_value_no2", "assets_pb_value_no3", "assets_pb_value_no4", "assets_pb_value_no5"]

    # withdraw 내 빈 리스트 이름
    def withdraw_no_list_content(self):
        if self.os_type == "ios":
            return "No available assets"
        else:
            return AndroidPropertyType.TEXT, "No available assets"

    """
    ========= 기능 함수 ===========
    """
     
    def click_assets_button(self):
        """
        assets 진입
        """
        locator = self.bottom_tab_assets_button()
        self.common_page.click_element(locator)

    def is_portfolio_detail_lists(self):
        """
        portfolio 상세 리스트 노출 확인
        """
        titles = self.portfolio_detail_titles()
        values = self.portfolio_detail_values()

        for _ in range(len(titles)):
            title = titles[_]
            value = values[_]

            if self.os_type == "ios":
                # iOS에서는 문자열로 그대로 사용
                title_locator = title
                value_locator = value
            else:  # Android
                # Android에서는 AndroidPropertyType을 사용해 튜플로 전달
                title_locator = (AndroidPropertyType.TEXT, title)
                value_locator = value

            # is_visible 호출
            if self.common_page.is_visible(title_locator) and self.common_page.is_visible(value_locator):
                self.logger.info(f"{title} / {value} 노출 확인")
                continue
            else:
                return False

        return True


    def click_open_positions_button(self):
        """
        Open position 버튼 선택 후 설명문 반환
        """
        self.common_page.click_element(self.open_positions_button())
        return self.common_page.get_text(self.positions_open_description())
    
    def click_pending_positions_button(self):
        """
        Pending position 버튼 선택 후 설명문 반환
        """
        self.common_page.click_element(self.pending_positions_button())
        return self.common_page.get_text(self.positions_pending_description())


    def is_valid_deposit_crypto_list(self):
        """
        assets 내 Deposit crypto List들의 데이터 유효성 확인
        """
        
        # 충분한 시간을 주기 위해 3초 대기
        time.sleep(3)

        # 리스트 데이터 가져오기
        assets_data = self.gather_information_assets_lists()


        assert len(assets_data) >= 5, "데이터가 5개 이상 노출 확인"
        self.logger.info(f"{len(assets_data)} 개의 데이터가 노출되었습니다.")

        # 리스트 내 5개 데이터에 대해 iOS는 각 데이터 분할 필요
        for asset in assets_data[:5]:
            if self.os_type == "ios":
                fields = [field.strip() for field in asset.split(",")]

                 # 두 번째 필드가 없거나, 두 번째 필드가 APR 형식이 아닌 경우 빈 문자열 추가
                if len(fields) < 2 or not re.match(r'^\d+% APR$', fields[1]):
                    self.logger.info(f"APR 필드가 없거나 유효하지 않으므로 빈 문자열로 채웁니다. 원래 필드: {fields}")
                    fields.insert(1, '')  # 두 번째 위치에 빈 문자열 추가

                # 필드 개수 보정: 부족한 필드를 맞춤
                if len(fields) < 6:
                    self.logger.info(f"필드 수가 {len(fields)}개로 부족합니다. 기본값으로 채웁니다. 원래 필드: {fields}")
                    fields += ['0.00'] * (6 - len(fields))

                asset = ', '.join(fields)

            is_valid = self.validate_assets_data(asset)
            self.logger.info(f"assets 정보: {asset}, 일치 여부: {is_valid}")
            if not is_valid:
                return False
        return True


    def gather_information_assets_lists(self):
        """
        List 요소에서 5개의 데이터 반환
        """
        assets_data = []
        current_assets = self.get_current_assets_data(self.assets_list())
        # assets_data 에 추가
        for assets in current_assets:
            assets_data.append(assets)

            if len(assets_data) >= 5:  # 5개 이상 자산을 수집하면 중단
                break

        return assets_data[:5]  # 5개의 자산만 반환

    
    def get_current_assets_data(self, locator):
        """
        현재 리스트의 코인 데이터 정보 추출
        """

        if self.os_type == "ios":
            # element의 label 속성 반환
            elements = self.common_page.find_elements(locator)
            return [element.get_attribute('label') for element in elements]

        else:
            assets = []

            # 'select_asset_name_'으로 시작하는 모든 자산 요소를 찾습니다.
            asset_elements = self.common_page.find_elements("uiautomator", 'new UiSelector().descriptionStartsWith("select_asset_name_")')
            self.logger.info(f"현재 화면에 {len(asset_elements)}개의 자산이 있습니다.")

            # 'select_asset_value_no1_'으로 시작하는 자산 가치 요소를 찾습니다.
            value_elements = self.common_page.find_elements("uiautomator", 'new UiSelector().descriptionStartsWith("select_asset_value_no1_")')
            self.logger.info(f"현재 화면에 {len(value_elements)}개의 자산 가치 요소가 있습니다.")

            for index, element in enumerate(asset_elements):
                # 자산 이름 정보 가져오기
                asset_name = element.get_attribute('text')  # 예시: "select_asset_name_bitcoin"

                # 자산 가치 정보 가져오기 (value 요소가 있는 경우에만 처리)
                if index < len(value_elements):
                    value_element = value_elements[index]
                    value = value_element.get_attribute('text')  # 예시: "select_asset_value_no1_bitcoin"
                    symbol = value_element.get_attribute('content-desc')  # 예시: "select_asset_value_no1_bitcoin"
                else:
                    value = None  # 자산 가치가 없을 경우 None 처리
                    symbol = None

                # 'earn_est_value_no5' 뷰에서 해당 자산의 APR값 가져오기
                try:
                    parent_view = self.common_page.find_element("uiautomator", f'new UiSelector().description("earn_est_value_no5").instance({index})')
                    apr_element = parent_view.find_element(AppiumBy.CLASS_NAME, "android.widget.TextView")
                    apr = apr_element.get_attribute("text") if apr_element else ''
                except NoSuchElementException as e:
                    apr = ''


                # Symble명을 이용하여 coe 값 가져오기 (유동적인 자산 값 처리)
                coin_code: str = symbol.split('_')[-1]  # 마지막 '_' 뒤의 값 추출 (예: 'eth')
                code = coin_code.upper()

                # 자산 정보를 로그로 출력
                self.logger.info(f"자산 정보: {asset_name}, {value}, {apr}, {code}")

                # 수집한 자산 정보를 딕셔너리에 저장
                assets.append({
                    'name': asset_name,
                    'apr': apr,
                    'code_1': code,
                    'value': value,
                    'code_2': code
                })

            return assets


    def validate_assets_data(self, asset):
        """
        각 코인 정보들이 패턴에 맞는지 검증
        """
        if self.os_type == "ios":
            patterns = {
                "assets_data": [r'^[A-Za-z\s]+$',           # 코인 이름 (예: Bitcoin, Tether USD)
                    r'^\d+% APR$|^$',                       # APR (예: 5% APR) 또는 존재하지 않을 수 있음 (빈 문자열 허용)
                    r'^[A-Z]+$',                            # 코인 심볼 (예: BTC)
                    r'^\d+\.\d+$',                          # 수량 (예: 0.00000000)
                    r'^[A-Z]+$',                            # 단위 (예: BTC)
                    r'^\d+\.\d+$|^$',                       # 가치 (예: 0.00) 또는 존재하지 않을 수 있음 (빈 문자열 허용)
                ]}
            fields = [field.strip() for field in re.split(r',\s*(?!\d)', asset)]  # 콤마로 분리하되 숫자의 콤마는 유지

             # 필드 개수 보정: 부족한 필드를 기본값으로 채우기
            if len(fields) < len(patterns):
                fields += ['0.00'] * (len(patterns) - len(fields))

        else:
            patterns = {
                "assets_data": [
                    r'^[A-Za-z\s]+$',               # 코인 이름 (예: Bitcoin, Tether USD)
                    r'^\d+% APR$|^$',               # APR (예: 5% APR) 또는 존재하지 않을 수 있음 (빈 문자열 허용)
                    r'^[A-Z]+$',                    # 코인 심볼 (예: BTC)
                    r'^\d+(\.\d+)?$|^$',            # 가치 (예: 0.00, 0, 10.5 등) 또는 존재하지 않을 수 있음 (빈 문자열 허용)
                    r'^[A-Z]+$',                    # 단위 (예: BTC)
                ]}
            fields = [
                asset['name'],
                asset['apr'],
                asset['code_1'],
                asset['value'],
                asset['code_2']
            ]

        # 패턴 수와 필드 수가 일치하지 않을 경우 False 반환
        if len(fields) != len(patterns["assets_data"]):
            self.logger.info(f"패턴 수와, 실제 데이터 필드 수가 일치하지 않습니다. Patterns: {len(patterns['assets_data'])}, Fields: {len(fields)}")
            return False


        # 각 필드가 정규식 패턴에 맞는지 검사
        for pattern, field in zip(patterns["assets_data"], fields):
            if not re.match(pattern, field):
                self.logger.info(f"'{field}'와 '{pattern}'이 일치하지 않습니다.")
                return False

        return True


