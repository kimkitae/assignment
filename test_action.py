from selenium.common.exceptions import NoSuchElementException
from time import sleep

class TestActions:
    def __init__(self, driver):
        self.driver = driver

    def click_element(self, xpath):
        # 특정 XPath로 버튼 클릭
        try:
            button = self.driver.find_element("xpath", xpath)
            button.click()
            print("버튼이 성공적으로 클릭되었습니다.")
        except NoSuchElementException:
            print("버튼을 찾지 못했습니다.")

    def wait_for_seconds(self, seconds):
        # 대기 함수
        sleep(seconds)
        print(f"{seconds}초 동안 대기합니다.")
