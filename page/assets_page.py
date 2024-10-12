

import re
import time
from page.common_page import CommonPage
from page.element_attribute_converter import ElementType, PropertyType, StringType


class AssetsPage:
    def __init__(self, driver, os_type, rp_logger):
        self.driver = driver
        self.os_type = os_type
        self.common_page = CommonPage(driver, os_type, rp_logger)
        self.logger = rp_logger

    
    """
    ========== Element 변수 ==========
    """
    def bottom_tab_assets_button(self):
        if self.os_type == "ios":
            return ElementType.STATIC_TEXT, PropertyType.LABEL, "Assets"
        else:
            return "market_button"
        
    def portfolio_balance_title(self):
        if self.os_type == "ios":
            return "assets_title_no1"
        else:
            return "Portfolio Balance"

    def portfolio_balance_value(self):
        if self.os_type == "ios":
            return "assets_title_no1_value_no2"
        else:
            return "0.00"
        
    def deposit_button(self):
        if self.os_type == "ios":
            return "tab_deposit"
        else:
            return "deposit_button"
        
    def assets_list(self):
        if self.os_type == "ios":
            return ElementType.BUTTON, StringType.BEGINS, "prex_receive_full_"
        else:
            return "carousel_no5_image"
        
    def withdraw_button(self):
        if self.os_type == "ios":
            return "tab_withdraw"
        else:
            return "withdraw_button"
        
    def open_positions_button(self):
        if self.os_type == "ios":
            return "tab_yp_open"
        else:
            return "positions_open_button"
        
    def pending_positions_button(self):
        if self.os_type == "ios":
            return "tab_yp_pending"
        else:
            return "positions_pending_button"

    def positions_open_description(self):
        if self.os_type == "ios":
            return "positions_open_description"
        else:
            return "All effective orders and contracts you possess show here."
        
    def positions_pending_description(self):
        if self.os_type == "ios":
            return "positions_pending_description"
        else:
            return "When you place a trigger order, orders that are still awaiting execution show here."
        
    
    def your_assets_title(self):
        if self.os_type == "ios":
            return "assets_title_no3"
        else:
            return "Your Assets"
        
    def your_assets_value(self):
        if self.os_type == "ios":
            return "assets_ya_value_no1"
        else:
            return "0.00"
    
    def bottom_usdt_bouns_value(self):
        if self.os_type == "ios":
            return ElementType.BUTTON, StringType.BEGINS,  "assets_ya_name_usdt_bonus"
        else:
            return "learn_more_button"


    def portfolio_detail_titles(self):
        if self.os_type == "ios":
            return ["Unrealized P&L", "Net funding fee", "Funds invested", "Funds reserved", "Available funds"]
        else:
            return "0.00"
    
    def portfolio_detail_values(self):
        if self.os_type == "ios":
            return ["assets_pb_value_no1", "assets_pb_value_no2", "assets_pb_value_no3", "assets_pb_value_no4", "assets_pb_value_no5"]
        else:
            return "0.00"

    def withdraw_no_list_content(self):
        if self.os_type == "ios":
            return "No available assets"
        else:
            return "No available assets"

    """
    ========== 함수 변수 ==========
    """
     
    def click_assets_button(self):
        locator = self.bottom_tab_assets_button()
        self.common_page.click_element(locator)

    def is_portfolio_detail_lists(self):
        titles = self.portfolio_detail_titles()
        values = self.portfolio_detail_values()
        for _ in range(len(titles)):
            if self.common_page.is_visible(titles[_]) and self.common_page.is_visible(values[_]):
                continue
            else:
                return False
        return True

    def click_open_positions_button(self):
        self.common_page.click_element(self.open_positions_button())
        return self.common_page.get_text(self.positions_open_description())
    
    def click_pending_positions_button(self):
        self.common_page.click_element(self.pending_positions_button())
        return self.common_page.get_text(self.positions_pending_description())

    def is_valid_deposit_crypto_list(self):
        assets_data = self.gather_information_assets_lists()
        assert len(assets_data) >= 5, "데이터가 5개 이상 노출 확인"

        for asset in assets_data[:5]:
            fields = [field.strip() for field in asset.split(",")]

            # 필드 개수 보정: 부족하거나 초과하는 필드를 맞춤
            if len(fields) < 6:
                self.logger.info(f"필드 수가 {len(fields)}개로 부족합니다. 기본값으로 채웁니다. 원래 필드: {fields}")
                fields += ['0.00'] * (6 - len(fields))
            elif len(fields) > 6:
                self.logger.info(f"필드 수가 {len(fields)}개로 초과합니다. 초과 필드를 제거합니다. 원래 필드: {fields}")
                fields = fields[:6]

            # 유효성 검사 수행
            is_valid = self.validata_assets_data(", ".join(fields))
            self.logger.info(f"assets 정보: {asset}, 일치 여부: {is_valid}")
            if not is_valid:
                return False
        return True


    def gather_information_assets_lists(self):
        assets_data = {}
        max_swipes = 5
        for _ in range(max_swipes):
            locator = self.assets_list()
            current_assets = self.get_current_assets_data(locator)
            for assets in current_assets:
                assets_name = assets.split(",")[0].strip()
                if assets_name not in assets_data:  # 중복된 항목을 추가하지 않음
                    assets_data[assets_name] = assets

                if len(assets_data) >= 5:  # 5개 수집되면 중단
                    break

            if len(assets_data) >= 5:
                break

            self.common_page.swipe("down")
            time.sleep(1)

        return list(assets_data.values())



    def get_current_assets_data(self, locator):
        elements = self.common_page.find_elements(locator)
        return [element.get_attribute('label') for element in elements]

    def validata_assets_data(self, assets_data):
        # 정규식 패턴 가져오기
        patterns = self.common_page.get_text_by_keyword("assets_data")

        # 데이터를 콤마로 분리한 후 각 항목의 공백을 제거
        fields = [field.strip() for field in re.split(r',\s*(?!\d)', assets_data)]  # 콤마로 분리하되 숫자의 콤마는 유지

        # 필드 개수 보정: 부족한 필드를 기본값으로 채우기
        if len(fields) < len(patterns):
            fields += ['0.00'] * (len(patterns) - len(fields))
        
        # 패턴과 데이터 필드 수가 일치하는지 확인
        if len(fields) != len(patterns):
            self.logger.info(f"패턴 수와, 실제 데이터 필드 수가 일치 하지 않습니다. Patterns: {len(patterns)}, Fields: {len(fields)}")
            return False

        # 각 필드가 정규식 패턴에 맞는지 검사
        for pattern, field in zip(patterns, fields):
            if not re.match(pattern, field):
                self.logger.info(f"'{field}' 와 '{pattern}' 이 일치하지 않습니다.")
                return False

        return True

