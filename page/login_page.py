import time
from page.common_page import CommonPage


class LoginPage:
    """
    LoginPage 클래스는 Login 관련 정보와 동작을 관리하는 클래스입니다.
    """

    def __init__(self, driver, os_type, rp_logger):
        self.logger = rp_logger
        self.driver = driver
        self.os_type = os_type
        self.common_page = CommonPage(driver, os_type, rp_logger)


    """
    ========= 객체 반환 함수 =========
    """

    # 메뉴 아이콘 버튼
    def menu_icon(self):
        return "menu_icon"

    # 닉네임 노출 영역
    def account_nickname_text(self):
        if self.os_type == "ios":
            return "account_nick_value_01-tab_account_nick_edit"
        else:
            return "account_nick_value_01"

    # Account 타이틀
    def account_main_title(self):
        return "account_main_title"

    # 로그아웃 버튼
    def account_sign_out_button(self):
        return "account_sign_out"

    # 설정 버튼
    def signin_setting_button(self):
        return "prex_signin_settings"

    # 뒤로 가기 버튼
    def back_icon(self):
        return "back_icon"

    """
    ========= 기능 함수 ===========
    """

    def check_signed_up (self):
        """
        닉네임 노출 여부 확인
        """
        try :
            self.common_page.click_element(self.menu_icon())
            assert self.common_page.is_visible(self.account_nickname_text()), "회원 닉네임 노출"
            nick_name = self.common_page.get_text(self.account_nickname_text())
            self.logger.info(f"회원 닉네임: {nick_name}")
            assert nick_name.startswith("Automation_"), "회원 닉네임 'Automation_'으로 시작 일치"
            return True
        except Exception as e:
            self.logger.info(f"예외 발생: {e}")
            return False

    def logout(self):
        """
        로그아웃 동작
        """
        self.common_page.click_element(self.menu_icon())
        assert self.common_page.is_visible(self.account_main_title()), "Account 화면 진입 확인"

        #닉네임이 보인 경우 로그인 된 상태 판단
        if self.common_page.is_visible(self.account_nickname_text()):
            self.common_page.swipe_to_element(self.account_sign_out_button())
            self.common_page.click_element(self.account_sign_out_button())
            self.common_page.wait_for(self.menu_icon(), timeout=3)
            assert self.common_page.is_visible(self.menu_icon()), "로그아웃 성공"

        # 닉네임 미 노출 시 이미 로그아웃으로 판단하여 뒤로 가기
        else:
            self.logger.info("이미 로그아웃 상태입니다.")
            self.common_page.click_element(self.back_icon())
            time.sleep(1)
    
    def click_menu_icon(self):
        """
        menu 아이콘 클릭
        """
        locator = self.menu_icon()
        self.common_page.click_element(locator)


    def click_setting_icon(self):
        """
        설정 버튼 클릭
        """
        locator = self.signin_setting_button()
        self.common_page.click_element(locator)
