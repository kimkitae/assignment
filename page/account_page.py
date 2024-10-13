
import random
import string
import time
import os
from page.common_page import CommonPage
from helper.element_attribute_converter import AndroidElementType, AndroidPropertyType, ElementType
from helper.regex_utility import RegexUtility
from dotenv import load_dotenv


class AccountPage:
    def __init__(self, driver, os_type, rp_logger):
        self.driver = driver
        self.os_type = os_type
        self.common_page = CommonPage(driver, os_type, rp_logger)
        self.regex_utility = RegexUtility(driver, os_type, rp_logger)
        self.logger = rp_logger
        load_dotenv()

    """
    ========== 함수 변수 ==========
    """

    def get_account_info(self, key, is_public=False):
        
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

    def menu_icon(self):
        if self.os_type == "ios":
            return "menu_icon"
        else:
            return "menu_icon"

    def account_nickname_text(self):
        if self.os_type == "ios":
            return "account_nick_value_01"
        else:
            return "account_nick_value_01"

    def account_nickname_edit_button(self):
        if self.os_type == "ios":
            return "tab_account_nick_edit"
        else:
            return "account_nick_value_01"

    def nickname_text_field(self):
        if self.os_type == "ios":
            return "account_set_nick_text_field"
        else:
            return AndroidElementType.EDIT_TEXT


    def nickname_confirm_button(self):
        if self.os_type == "ios":
            return "account_set_nick_confirm"
        else:
            return AndroidElementType.BUTTON


    """
    ------
    """


    def weekly_leaderboard_count(self):
        if self.os_type == "ios":
            return "tab_account_lb_wv"
        else:
            return "tab_account_lb_wv"

    def weekly_page_title(self):
        if self.os_type == "ios":
            return "Weekly P&L leaderboard"
        else:
            return AndroidPropertyType.TEXT, "Weekly P&L leaderboard"
        
    """
    ------
    """

    def hide_info_button(self):
        if self.os_type == "ios":
            return "Hide Info"
        else:
            return AndroidPropertyType.TEXT, "Hide Info"

    
    def back_icon(self):
        if self.os_type == "ios":
            return "back_icon"
        else:
            return "back_icon"

    """
    =========== 함수 구현 ==========
    """

    # 닉네임 확인
    def is_nickname(self, nickname):
        nickname_text = self.common_page.get_text(self.account_nickname_text())
        self.logger.info(f"확인된 닉네임: {nickname_text}")
        return nickname_text == nickname

    # 닉네임 변경
    def change_nickname(self, nickname):
        self.common_page.click_element(self.account_nickname_edit_button())
        self.common_page.clean_text_field("TEXT_FIELD")
        self.common_page.set_text(nickname, self.nickname_text_field())
        self.logger.info(f"닉네임 입력: {nickname}")
        self.common_page.click_element(self.nickname_confirm_button())
        self.common_page.wait_for(self.account_nickname_text(), timeout=5)
        return self.common_page.get_text(self.account_nickname_text()) == nickname

    # 랜덤 닉네임 생성
    def generate_random_nickname(self, current_nickname):
            while True:
                random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
                new_nickname = f"Automation_{random_suffix}"
                if new_nickname != current_nickname:
                    self.logger.info(f"생성된 랜덤 닉네임: {new_nickname}")
                    return new_nickname

    # 위클리 리더보드 카운트 확인
    def is_weekly_leaderboard_count(self):
        weekly_leaderboard_count = self.common_page.get_text(self.weekly_leaderboard_count())
        result = self.regex_utility.get_text_by_keyword("위클리리더보드카운트", weekly_leaderboard_count)
        self.logger.info(f"위클리 리더보드 카운트 확인: {result}")
        return result

    # Support 메뉴 클릭
    def click_support_menu(self, title):
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