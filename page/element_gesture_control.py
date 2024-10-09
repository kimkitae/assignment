import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from enum import Enum
from conftest import driver
from page.execute_method import ExecuteMethod


class ScrollSize(Enum):
    SMALL = 25
    MEDIUM = 50
    LARGE = 75
    XLARGE = 100


class ElementGestureControl:
    last_scrolled_element = None
    base_scroll_factor = ScrollSize.MEDIUM
    MAX_RETRIES = 10

    @staticmethod
    def scroll_to_text(element_text, size=None):
        scroll_factor = size.value if size else ElementGestureControl.base_scroll_factor.value
        return ElementGestureControl.scroll_list_to_element_with_predicate(element_text, scroll_factor)

    @staticmethod
    def swipe_action(element, direction, swipe_percentage=50):
        swipe_factor = swipe_percentage / 100.0
        center_x, center_y = ElementGestureControl.calculate_element_center(element)
        start_x, start_y, end_x, end_y = ElementGestureControl.swipe_action_f(direction, center_x, center_y, swipe_factor)
        ExecuteMethod.drag_from_to(start_x, start_y, end_x, end_y, 1500)

    @staticmethod
    def swipe_from_center_to(swipe_percentage=50, direction='up'):
        swipe_factor = swipe_percentage / 100.0
        if direction.lower() in ['left', 'right']:
            swipe_factor *= 1.5

        screen_size = driver.get_window_size()
        screen_width, screen_height = screen_size['width'], screen_size['height']
        start_x, start_y = screen_width // 2, screen_height // 2

        end_x, end_y = ElementGestureControl.swipe_action_f(direction, start_x, start_y, swipe_factor)
        ExecuteMethod.drag_from_to(start_x, start_y, end_x, end_y, 1000)

    @staticmethod
    def swipe_by_percentage(start_x_percent, start_y_percent, end_x_percent, end_y_percent):
        screen_size = driver.get_window_size()
        screen_width, screen_height = screen_size['width'], screen_size['height']

        start_x = int(screen_width * (start_x_percent / 100.0))
        start_y = int(screen_height * (start_y_percent / 100.0))
        end_x = int(screen_width * (end_x_percent / 100.0))
        end_y = int(screen_height * (end_y_percent / 100.0))

        ExecuteMethod.drag_from_to(start_x, start_y, end_x, end_y, 1000)

    @staticmethod
    def swipe_to_element(element, duration_time=1000):
        screen_size = driver.get_window_size()
        width, height = screen_size['width'], screen_size['height']
        start_x = width // 2
        end_x = width // 2
        start_y = int(height * 2 / 3)
        end_y = int(height / 3)

        return ElementGestureControl.swipe_to_find_element_f(element, start_x, start_y, end_x, end_y, duration_time)

    @staticmethod
    def swipe_to_find_element_f(element, start_x, start_y, end_x, end_y, duration_time):
        try:
            for _ in range(ElementGestureControl.MAX_RETRIES):
                try:
                    WebDriverWait(driver, 1).until(EC.visibility_of(element))
                    return True
                except TimeoutException:
                    ExecuteMethod.drag_from_to(start_x, start_y, end_x, end_y, duration_time)
                    time.sleep(0.5)
            return False
        except Exception as e:
            print(f'Object찾기 실패: {e}')
            return False

    @staticmethod
    def scroll_list_to_element_with_predicate(element_text, scroll_size):
        predicate_string = f"type == 'XCUIElementTypeStaticText' AND visible == true AND label == '{element_text}'"
        
        for _ in range(ElementGestureControl.MAX_RETRIES):
            try:
                element = driver.find_element_by_ios_predicate(predicate_string)
                return True
            except NoSuchElementException:
                ElementGestureControl.scroll_entire_list(scroll_size)
        
        print(f"{ElementGestureControl.MAX_RETRIES}회 이상 Element를 찾지 못했습니다.")
        return False

    @staticmethod
    def scroll_entire_list(scroll_size):
        screen_size = driver.get_window_size()
        start_x = screen_size['width'] // 2
        start_y = int(screen_size['height'] * 0.8)
        end_y = int(screen_size['height'] * 0.2)

        ExecuteMethod.drag_from_to(start_x, start_y, start_x, end_y, 1500)
        time.sleep(1)

    @staticmethod
    def swipe(direction):
        ElementGestureControl.swipe_from_center_to(50, direction)

    @staticmethod
    def drag_to_drop(from_element, to_element):
        from_center_x, from_center_y = ElementGestureControl.calculate_element_center(from_element)
        to_center_x, to_center_y = ElementGestureControl.calculate_element_center(to_element)

        ExecuteMethod.drag_from_to(from_center_x, from_center_y, to_center_x, to_center_y, 2500)

    @staticmethod
    def calculate_element_center(element):
        location = element.location
        size = element.size
        return location['x'] + size['width'] // 2, location['y'] + size['height'] // 2

    @staticmethod
    def swipe_action_f(direction, start_x, start_y, swipe_factor):
        screen_size = driver.get_window_size()
        screen_width, screen_height = screen_size['width'], screen_size['height']

        end_x, end_y = start_x, start_y
        if direction.lower() == 'down':
            end_y = int(start_y - (start_y * swipe_factor))
        elif direction.lower() == 'up':
            end_y = int(start_y + (screen_height - start_y) * swipe_factor)
        elif direction.lower() == 'left':
            end_x = int(start_x - (start_x * swipe_factor))
        elif direction.lower() == 'right':
            end_x = int(start_x + (screen_width - start_x) * swipe_factor)
        else:
            raise ValueError("Invalid swipe direction")

        return start_x, start_y, end_x, end_y