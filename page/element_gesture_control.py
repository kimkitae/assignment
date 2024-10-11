import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from enum import Enum
from page.execute_method import ExecuteMethod
from appium.webdriver.common.appiumby import AppiumBy


class ScrollSize(Enum):
    SMALL = 25
    MEDIUM = 50
    LARGE = 75
    XLARGE = 100


class ElementGestureControl:
    MAX_RETRIES = 10

    def __init__(self, driver, os_type):
        self.driver = driver
        self.execute_method = ExecuteMethod(driver, os_type)
        self.screen_size = driver.get_window_size()
        self.screen_width = self.screen_size['width']
        self.screen_height = self.screen_size['height']
        self.base_scroll_factor = ScrollSize.MEDIUM

    def scroll_to_text(self, element_text, size=None):
        scroll_factor = size.value if size else self.base_scroll_factor.value
        return self.scroll_list_to_element_with_predicate(element_text, scroll_factor)

    def swipe_action(self, element, direction, swipe_percentage=50):
        swipe_factor = swipe_percentage / 100.0
        center_x, center_y = self.calculate_element_center(element)
        start_x, start_y, end_x, end_y = self.swipe_action_f(direction, center_x, center_y, swipe_factor)
        self.execute_method.drag_from_to(start_x, start_y, end_x, end_y, 1500)

    def swipe_from_center_to(self, swipe_percentage=50, direction='up'):
        swipe_factor = swipe_percentage / 100.0
        if direction.lower() in ['left', 'right']:
            swipe_factor *= 1.5
        
        start_x, start_y = self.screen_width // 2, self.screen_height // 2
        end_x, end_y = self.swipe_action_f(direction, start_x, start_y, swipe_factor)
        self.execute_method.drag_from_to(start_x, start_y, end_x, end_y, 1000)

    def swipe_by_percentage(self, start_x_percent, start_y_percent, end_x_percent, end_y_percent):
        start_x = int(self.screen_width * (start_x_percent / 100.0))
        start_y = int(self.screen_height * (start_y_percent / 100.0))
        end_x = int(self.screen_width * (end_x_percent / 100.0))
        end_y = int(self.screen_height * (end_y_percent / 100.0))

        self.execute_method.drag_from_to(start_x, start_y, end_x, end_y, 1000)

    def swipe_to_element(self, locator, duration_time=1000):
        start_x = self.screen_width // 2
        end_x = self.screen_width // 2
        start_y = int(self.screen_height * 2 / 3)
        end_y = int(self.screen_height / 3)
        print(f"start_x - {start_x}, end_x - {end_x}, start_y - {start_y}, end_y- {end_y}")
        print(f"swipe_to_element - {locator}")

        return self.swipe_to_find_element_f(locator, start_x, start_y, end_x, end_y, duration_time)

    def swipe_to_find_element_f(self, locator, start_x, start_y, end_x, end_y, duration_time):

        try:
            for _ in range(self.MAX_RETRIES):
                try:
                    element = WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located(locator))

                    if element.is_displayed():
                        location = element.location
                        size = element.size

                        if (location['y'] + size['height']) > self.screen_height * 0.8:
                            self.swipe('down')

                        return True
                except TimeoutException:
                    self.execute_method.drag_from_to(start_x, start_y, end_x, end_y, duration_time)
                    time.sleep(0.5)
            return False
        except Exception as e:
            print(f'Object찾기 실패: {e}')
            return False

    def scroll_list_to_element_with_predicate(self, element_text, scroll_size):
        predicate_string = f"type == 'XCUIElementTypeStaticText' AND visible == true AND label == '{element_text}'"
        
        for _ in range(self.MAX_RETRIES):
            try:
                self.driver.find_element(AppiumBy.IOS_PREDICATE, predicate_string)
                # self.driver.find_element_by_ios_predicate(predicate_string)
                return True
            except NoSuchElementException:
                self.scroll_entire_list(scroll_size)
        
        print(f"{self.MAX_RETRIES}회 이상 Element를 찾지 못했습니다.")
        return False

    def scroll_entire_list(self, scroll_size):
        start_x = self.screen_width // 2
        start_y = int(self.screen_height * 0.8)
        end_y = int(self.screen_height * 0.2)

        self.execute_method.drag_from_to(start_x, start_y, start_x, end_y, 1500)
        time.sleep(1)

    def swipe(self, direction):
        self.swipe_from_center_to(50, direction)

    def drag_to_drop(self, from_element, to_element):
        from_center_x, from_center_y = self.calculate_element_center(from_element)
        to_center_x, to_center_y = self.calculate_element_center(to_element)

        self.execute_method.drag_from_to(from_center_x, from_center_y, to_center_x, to_center_y, 2500)

    def calculate_element_center(self, element):
        location = element.location
        size = element.size
        return location['x'] + size['width'] // 2, location['y'] + size['height'] // 2

    def swipe_action_f(self, direction, start_x, start_y, swipe_factor):
        end_x, end_y = start_x, start_y
        if direction.lower() == 'down':
            end_y = int(start_y - (start_y * swipe_factor))
        elif direction.lower() == 'up':
            end_y = int(start_y + (self.screen_height - start_y) * swipe_factor)
        elif direction.lower() == 'left':
            end_x = int(start_x - (start_x * swipe_factor))
        elif direction.lower() == 'right':
            end_x = int(start_x + (self.screen_width - start_x) * swipe_factor)
        else:
            raise ValueError("Invalid swipe direction")
        return end_x, end_y

    def scroll_to_elements(self, element, max_scrolls=10):
        elements = []
        for _ in range(max_scrolls):
            try:
                current_elements = element
                elements.extend(current_elements)
                if len(elements) >= 20:
                    break
                self.scroll_entire_list(ScrollSize.MEDIUM.value)
                time.sleep(1)
            except NoSuchElementException:
                break
        return elements[:20]
