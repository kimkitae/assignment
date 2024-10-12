

from datetime import datetime, timezone
import re
from page.common_page import CommonPage
from page.element_attribute_converter import ElementType, PropertyType


class ChallengePage:
    def __init__(self, driver, os_type, rp_logger):
        self.driver = driver
        self.os_type = os_type
        self.common_page = CommonPage(driver, os_type, rp_logger)
        self.logger = rp_logger



    """
    ============ 변수 선언 영역 ============
    """

    def bottom_tab_challenge_button(self):
        if self.os_type == "ios":
            return ElementType.STATIC_TEXT, PropertyType.LABEL, "Challenge"
        else:
            return "market_button"

    def top_tab_launch_airdrop_button(self):
        if self.os_type == "ios":
            return ElementType.BUTTON, PropertyType.LABEL, "Launch Airdrop, Launch Airdrop"
        else:
            return "launch_airdrop_button"
    
    def event_data_element(self, index):
        if self.os_type == "ios":
            return ElementType.STATIC_TEXT, PropertyType.NAME, f"a{index}"
        else:
            return f"event_data_{index}"

    def event_status_element(self, index):
        if self.os_type == "ios":
            return ElementType.STATIC_TEXT, PropertyType.NAME, f"b{index}"
        else:
            return f"event_status_{index}"


    """
    ============ 함수 선언 영역 ============
    """

    def click_challenge_button(self):
        locator = self.bottom_tab_challenge_button()
        self.common_page.click_element(locator)
    
    def click_launch_airdrop_button(self):
        locator = self.top_tab_launch_airdrop_button()
        self.common_page.click_element(locator)

    def get_event_info(self):
        event_info = []
        max_iterations = 15
        i = 1

        while i <= max_iterations:
            data_element = self.event_data_element(i)
            status_element = self.event_status_element(i)

            is_visible = False
            is_visible = self.common_page.is_visible(data_element)

            if not is_visible:
                break

            data_text = self.common_page.get_text(data_element)
            status_text = self.common_page.get_text(status_element)
            event_info.append((data_text, status_text))

            i += 1
            if i > 1:
                self.common_page.swipe("left")
        self.logger.info(f"전체 이벤트 일정: {event_info}")
        return self.validate_event_info(event_info)

    def validate_event_info(self, event_info):
        current_time = datetime.now(timezone.utc)
        current_month_day = current_time.strftime("%m.%d")

        for data_text, status in event_info:
            assert self.common_page.get_text_by_keyword("이벤트날짜", data_text) == data_text, "이벤트 날짜 텍스트 유효성 검사"

            start_date_str, end_date_str = self.parse_date_range(data_text)

            # 현재 날짜와 비교를 위해 월/일을 datetime 객체로 변환
            start_date = datetime.strptime(start_date_str, "%m.%d")
            end_date = datetime.strptime(end_date_str, "%m.%d")
            current_date = datetime.strptime(current_month_day, "%m.%d")

            # 현재 날짜가 이벤트의 시작일과 종료일 사이에 포함되는지 확인하여 포함된다면 Opened 상태인지 확인
            if start_date <= current_date <= end_date:
                self.logger.info(f"시작 일 {start_date} - 종료 일 {end_date} / 현재 일 {current_date} - {status}")
                if status != "Opened":
                    self.logger.info(f"잘못된 이벤트 상태: {status}, Expected: Opened")
                    return False
            # 현재 날짜가 이벤트의 시작일과 종료일 사이에 포함되지 않는다면 Closed 상태인지 확인
            else:
                self.logger.info(f"시작 일 {start_date} - 종료 일 {end_date} / 현재 일 {current_date} - {status}")
                if status != "Closed":
                    self.logger.info(f"잘못된 이벤트 상태: {status}, Expected: Closed")
                    return False

        return True

    def parse_date_range(self, date_text):
        # ' UTC' 제거하고 시작과 끝 날짜 분리
        start_str, end_str = date_text.replace(' UTC', '').split(" - ")
        
        # 시작 날짜에서 연도 부분을 제거하고 월/일만 남김
        start_month_day = start_str[3:8]  # '24.09.23' -> '09.23'
        
        # 종료 날짜에서 월/일만 남김
        end_month_day = end_str[:5]  # '09.26'
        
        # 시작 날짜와 종료 날짜 문자열로 반환
        return start_month_day, end_month_day

