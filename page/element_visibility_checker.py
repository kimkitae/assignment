import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import concurrent.futures

class ElementVisibilityChecker:
    def __init__(self, driver):
        self.driver = driver

    def wait_for(self, test_object, wait_time=3):
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(test_object)
            )
            return True
        except TimeoutException:
            return False

    def is_visible(self, test_object, wait_time=3):
        return self.wait_for(test_object, wait_time)

    def is_verify(self, test_object, wait_time=3):
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(test_object)
            )
            return True
        except TimeoutException:
            raise Exception(f"{test_object} 요소를 찾을 수 없습니다.")

    def is_not_visible(self, test_object, wait_time=1):
        try:
            WebDriverWait(self.driver, wait_time).until_not(
                EC.presence_of_element_located(test_object)
            )
            return True
        except TimeoutException:
            return False

    def is_visible_concurrency(self, strings_to_test):
        def check_visibility(string):
            try:
                return self.is_visible(("ios_predicate", f"label == '{string}'"))
            except Exception as e:
                print(f"{string} 확인 중 오류 발생: {str(e)}")
                return False

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(check_visibility, strings_to_test))

        for string, result in zip(strings_to_test, results):
            print(f"{string} isVisible : {result}")

        return all(results)
