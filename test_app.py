import pytest
from test_action import TestActions


@pytest.mark.usefixtures("driver")  # Pytest fixture 사용
class TestApp:
    @classmethod
    def setup_class(cls):
        # 테스트 클래스 실행 전
        print("테스트 클래스 시작")

    @classmethod
    def teardown_class(cls):
        # 테스트 클래스 종료 후
        print("테스트 클래스 종료")

    def setup_method(self, method):
        # 각 테스트 메소드 시작 전에 실행
        print(f"테스트 케이스 {method.__name__} 시작")

    def teardown_method(self, method):
        # 각 테스트 메소드 종료 후 실행
        print(f"테스트 케이스 {method.__name__} 종료")

    def test_app_launch(self, driver):
        # 앱 활성화
        driver.activate_app("com.aqx.prex")
        print("앱이 활성화되었습니다.")

        # TestActions를 사용하여 버튼 클릭
        actions = TestActions(driver)
        actions.wait_for_seconds(5)
        actions.click_element("//XCUIElementTypeButton")
