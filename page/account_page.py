
import random
import string
import time
import os
from page.common_page import CommonPage
from helper.element_attribute_converter import AndroidElementType, AndroidPropertyType
from helper.regex_utility import RegexUtility
from dotenv import load_dotenv


class AccountPage:
    """
    AccountPage 클래스는 사용자 계정 관련 정보와 동작을 관리하는 클래스입니다.
    """

    def __init__(self, driver, os_type, rp_logger):
        self.driver = driver
        self.os_type = os_type
        self.common_page = CommonPage(driver, os_type, rp_logger)  # 공통 페이지 객체
        self.regex_utility = RegexUtility(driver, os_type, rp_logger)  # 정규 표현식 유틸리티 객체
        self.logger = rp_logger
        load_dotenv()  # 환경 변수를 로드

    """
    ========= 객체 반환 함수 =========
    """

    def get_account_info(self, key, is_public=False):
        # .env 의 사용자정보 불러오기
        account_info = {
            "email": os.getenv("EMAIL"),
            "phone": os.getenv("PHONE"), 
            "name": os.getenv("NAME"),
            "level": os.getenv("LEVEL")
        }
        if self.os_type == "android":
            if is_public:
                return account_info.get(key, "정보를 찾을 수 없습니다.")
            else:
                return AndroidPropertyType.TEXT, account_info.get(key, "정보를 찾을 수 없습니다.")
        else:
            return account_info.get(key, "정보를 찾을 수 없습니다.")

    # 상단 왼쪽 메뉴 아이콘
    def menu_icon(self):
            return "menu_icon"

    # 닉네임 텍스트
    def account_nickname_text(self):
            return "account_nick_value_01"

    # 닉네임 변경 버튼
    def account_nickname_edit_button(self):
        if self.os_type == "ios":
            return "tab_account_nick_edit"
        else:
            return "account_nick_value_01"

    # 닉네임 입력 텍스트 필드
    def nickname_text_field(self):
        if self.os_type == "ios":
            return "account_set_nick_text_field"
        else:
            return AndroidElementType.EDIT_TEXT

    # 닉네임 변경 완료 버튼
    def nickname_confirm_button(self):
        if self.os_type == "ios":
            return "account_set_nick_confirm"
        else:
            return AndroidElementType.BUTTON

    # 위클리 리더보드 카운트
    def weekly_leaderboard_count(self):
            return "tab_account_lb_wv"

    # 위클리 카운트 페이지 제목
    def weekly_page_title(self):
        if self.os_type == "ios":
            return "Weekly P&L leaderboard"
        else:
            return AndroidPropertyType.TEXT, "Weekly P&L leaderboard"

    # Hide info 버튼
    def hide_info_button(self):
        if self.os_type == "ios":
            return "Hide Info"
        else:
            return AndroidPropertyType.TEXT, "Hide Info"

    # 뒤로 가기 버튼
    def back_icon(self):
            return "back_icon"


    """
    ========= 기능 함수 ===========
    """


    def is_nickname(self, nickname):
        """
        현재 닉네임이 맞는지 확인
        """
        nickname_text = self.common_page.get_text(self.account_nickname_text())
        self.logger.info(f"확인된 닉네임: {nickname_text}")
        return nickname_text == nickname

    def change_nickname(self, nickname):
        """
        현재 닉네임하고 다른 랜덤으로 생성하여 닉네임 변경 및 변경 확인
        """
        self.common_page.click_element(self.account_nickname_edit_button())
        self.common_page.clean_text_field("TEXT_FIELD")
        self.common_page.set_text(nickname, self.nickname_text_field())
        self.logger.info(f"닉네임 입력: {nickname}")
        self.common_page.click_element(self.nickname_confirm_button())
        self.common_page.wait_for(self.account_nickname_text(), timeout=5)
        return self.common_page.get_text(self.account_nickname_text()) == nickname

    def generate_random_nickname(self, current_nickname):
        """
        닉네임 랜덤 생성
        """
        while True:
            random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
            new_nickname = f"Automation_{random_suffix}"
            if new_nickname != current_nickname:
                self.logger.info(f"생성된 랜덤 닉네임: {new_nickname}")
                return new_nickname

    def is_weekly_leaderboard_count(self):
        """
        위클리 리더보드 내 카운트 노출 확인
        """
        weekly_leaderboard_count = self.common_page.get_text(self.weekly_leaderboard_count())
        result = self.regex_utility.get_text_by_keyword("위클리리더보드카운트", weekly_leaderboard_count)
        self.logger.info(f"위클리 리더보드 카운트 확인: {result}")
        return result

    # Support 메뉴 클릭
    def click_support_menu(self, title):
        """
        지정한 Support 메뉴 찾아 클릭
        """
        if self.os_type == "ios":
            self.common_page.swipe_to_element(f"Setting_{title}")
            self.common_page.click_element(f"Setting_{title}")
        else:
            time.sleep(1)
            self.common_page.swipe_to_element(AndroidPropertyType.TEXT, title)
            time.sleep(1)
            self.common_page.click_element(AndroidPropertyType.TEXT, title)
            time.sleep(5)

    def get_masked_account_info(self):
        """
        마스킹 처리된 개인정보 데이터 처리 반환
        """
        email = self.get_account_info("email", is_public=True)
        phone = self.get_account_info("phone", is_public=True)
        name = self.get_account_info("name", is_public=True)

        masked_email = f"{email[:2]}"
        masked_phone_first = f"{phone[:3]}"
        masked_phone_last = f"{phone[-2:]}"
        masked_name_first = f"{name[:2]}"
        masked_name_last = f"{name[-2:]}"
        
        masked_info = {
            "email": masked_email,
            "phone_first": masked_phone_first,
            "phone_last": masked_phone_last,
            "name_first": masked_name_first,
            "name_last": masked_name_last,
        }

        if self.os_type == "android":
            android_info = {
                "email": (AndroidPropertyType.TEXT, masked_email),
                "phone_first": (AndroidPropertyType.TEXT, masked_phone_first),
                "phone_last": (AndroidPropertyType.TEXT, masked_phone_last),
                "name_first": (AndroidPropertyType.TEXT, masked_name_first),
                "name_last": (AndroidPropertyType.TEXT, masked_name_last),
            }
            return masked_info, android_info
        else:
            return masked_info, masked_info