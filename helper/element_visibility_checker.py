from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import concurrent.futures


# 오브젝트의 노출, 미노출 관련 클래스 정의
class ElementVisibilityChecker:
    def __init__(self, driver, rp_logger):
        # 드라이버 및 로거 초기화
        self.logger = rp_logger
        self.driver = driver

    def wait_for(self, test_object, wait_time=3):
        # 주어진 객체가 나타날 때까지 대기
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(test_object)
            )
            return True  # 객체가 성공적으로 나타나면 True 반환
        except TimeoutException:
            return False  # 타임아웃이 발생하면 False 반환

    def is_visible(self, test_object, wait_time=3):
        # 주어진 객체가 화면에 나타났는지 확인
        return self.wait_for(test_object, wait_time)

    def is_verify(self, test_object, wait_time=3):
        # 주어진 객체가 화면에 나타났는지 검증, 실패 시 예외 발생
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(test_object)
            )
            return True  # 객체가 존재하면 True 반환
        except TimeoutException:
            self.logger.info(f"{test_object} 요소를 찾을 수 없습니다.")
            raise Exception(f"{test_object} 요소를 찾을 수 없습니다.")

    def is_not_visible(self, test_object, wait_time=1):
        # 주어진 객체가 화면에 더 이상 보이지 않는지 확인
        try:
            WebDriverWait(self.driver, wait_time).until_not(
                EC.presence_of_element_located(test_object)
            )
            return True  # 객체가 화면에 없으면 True 반환
        except TimeoutException:
            return False  # 타임아웃 시 False 반환

    def is_visible_concurrency(self, strings_to_test):
        # 여러 문자열을 병렬로 테스트하여 각 요소가 화면에 나타났는지 확인
        def check_visibility(string):
            try:
                return self.is_visible(("ios_predicate", f"label == '{string}'"))
            except Exception as e:
                self.logger.info(f"{string} 확인 중 오류 발생: {str(e)}")
                return False

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(check_visibility, strings_to_test))

        for string, result in zip(strings_to_test, results):
            # 각 문자열의 가시성 결과를 로그에 기록

            self.logger.info(f"{string} isVisible : {result}")

        # 모든 요소가 화면에 나타났는지 여부 반환
        return all(results)
