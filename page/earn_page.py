import time
from helper.execute_method import ExecuteMethod
from page.common_page import CommonPage
from helper.element_attribute_converter import AndroidPropertyType, ElementType, StringType
from helper.regex_utility import RegexUtility


class EarnPage:
    """
    EarnPage 클래스는 Earn 관련 정보와 동작을 관리하는 클래스입니다.
    """

    def __init__(self, driver, os_type, rp_logger):
        self.driver = driver
        self.os_type = os_type
        self.common_page = CommonPage(driver, os_type, rp_logger)
        self.regex_utility = RegexUtility(driver, os_type, rp_logger)
        self.execute_method = ExecuteMethod(driver, os_type, rp_logger)
        self.logger = rp_logger


    """
    ========= 객체 반환 함수 =========
    """

    # Earn 버튼
    def bottom_tab_earn_button(self):
        if self.os_type == "ios":
            return "Earn"
        else:
            return AndroidPropertyType.TEXT, "Earn"

    # Earn Way 버튼
    def earn_way_to_no_button(self):
        if self.os_type == "ios":
            return ElementType.BUTTON, StringType.BEGINS, "earn_way_to_no"
        else:
            return "non_usdt_deposit_no0"

    # Deposit 내 주소 복사 버튼
    def deposit_copy_address_button(self):
        return "deposit_copy_address"

    # Deposit 메모 값
    def deposit_memo_value(self):
        return "deposit_memo_value"

    # Deposit 주소 값
    def deposit_address(self):
        return "deposit_address"

    # Deposit 내 드랍박스 버튼
    def dropdown_network(self):
        if self.os_type == "ios":
            return "chevron-down"
        else:
            return "depositnetwortno1"

    # Dropbox 내 network 항목
    def btm_select_network_no(self, index):
        if self.os_type == "ios":
            return f"btms_select_network_no_{index + 1}"
        else:
            return f"btms_select_network_no{index}"

    """
    ========= 기능 함수 ===========
    """

    def is_address(self):
        """
        Deposit 내 주소 영역 노출 확인
        """
        if self.common_page.is_visible(self.deposit_address()):
            return self.common_page.get_text(self.deposit_address())
        else:
            return False

    def is_memo_value(self):
        """
        Deposit 내 메모 영역 노출 확인
        """
        if self.common_page.is_visible(self.deposit_memo_value()):
            return self.common_page.get_text(self.deposit_memo_value())
        else:
            return False

    def change_network_button(self, index):
        """
        지정한 번호의 Network 변경 0부터 시작
        """
        self.common_page.click_element(self.dropdown_network())
        self.common_page.click_element(self.btm_select_network_no(index))
        self.logger.info(f"네트워트 변경 : {self.btm_select_network_no(index)}")

    def set_default_first_network(self):
        """
        기본 으로 0번째 Network로 선택
        """
        time.sleep(2)
        self.common_page.click_element(self.dropdown_network())
        time.sleep(1)
        self.common_page.click_element(self.btm_select_network_no(0))
        self.logger.info(f"가장 첫번째 네트워크 선택 {self.btm_select_network_no(0)}")

    def validate_toast_message(self):
        """
        주소 복사 버튼 선택 시 Toast 팝업 노출 여부 확인
        Android는 Copied 와 클립보드 복사 문구 노출되어 둘중 하나 노출 시 통과
        """
        if self.os_type == "ios":
            return self.common_page.is_visible("deposit_address_copied_no1")
        else:
            page_source = self.execute_method.get_page_source_in_json()
            toast_message_1 = self.regex_utility.matchered_text(r'Copied to clipboard.*', page_source)
            toast_message_2 = self.regex_utility.matchered_text(r'클립보드에 복사되었어요.', page_source)
            self.logger.info(f"toast_message_1: {toast_message_1}, toast_message_2: {toast_message_2}")
            return toast_message_1 != "null" or toast_message_2 != "null"