import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ExecuteMethod:
    def __init__(self, driver, os_type):
        self.driver = driver
        self.os_type = os_type

    def activate_app(self):
        if self.os_type == "ios":
            self.driver.execute_script("mobile: activateApp", {"bundleId": "com.aqx.prex"})
        elif self.os_type == "android":
            self.driver.execute_script("mobile: activateApp", {"packageId": "com.aqx.prex"})

    def launch_app(self):
        if self.os_type == "ios":
            self.driver.execute_script("mobile: launchApp", {"bundleId": "com.aqx.prex"})
        elif self.os_type == "android":
            self.driver.execute_script("mobile: launchApp", {"packageId": "com.aqx.prex"})

    def terminate_app(self):
        if self.os_type == "ios":
            self.driver.execute_script("mobile: terminateApp", {"bundleId": "com.aqx.prex"})
        elif self.os_type == "android":
            self.driver.execute_script("mobile: terminateApp", {"packageId": "com.aqx.prex"})

    def swipe(self,direction):
        self.driver.execute_script("mobile: swipe", {"direction": direction, "velocity": 250})

    def swipe_on_element(self, element, direction):
        self.driver.execute_script("mobile: swipe", {"element": element.id, "direction": direction, "velocity": 250})

    def drag_from_to(self, start_x, start_y, end_x, end_y, duration_time):
        duration = duration_time / 1000.0
        self.driver.execute_script("mobile: dragFromToForDuration", {
            "duration": duration,
            "fromX": start_x,
            "fromY": start_y,
            "toX": end_x,
            "toY": end_y
        })

    def deep_link(self, url):
        if self.os_type == "ios":
            self.driver.execute_script("mobile: deepLink", {"url": url, "bundleId": "com.aqx.prex"})
        elif self.os_type == "android":
            self.driver.execute_script("mobile: deepLink", {"url": url, "packageId": "com.aqx.prex"})

    def get_device_info(self):
        return self.driver.execute_script("mobile: deviceInfo")

    def get_contexts(self, wait_for_webview_ms=5000):
        return self.driver.execute_script("mobile: getContexts", {"waitForWebviewMs": wait_for_webview_ms})

    def get_page_source_in_json(self):
        return self.driver.execute_script("mobile: source", {"format": "json", "recursive": True})

    def hide_keyboard(self):
        self.driver.execute_script("mobile: hideKeyboard", {"keys": ["done", "완료"]})

    def is_keyboard_shown(self):
        return self.driver.execute_script("mobile: isKeyboardShown")

    def set_simulated_location(self, latitude, longitude):
        self.driver.execute_script("mobile: setSimulatedLocation", {"latitude": latitude, "longitude": longitude})

    def reset_simulated_location(self):
        self.driver.execute_script("mobile: resetSimulatedLocation")

    def scroll_to_element(self, element_id):
        self.driver.execute_script("mobile: scrollToElement", {"elementId": element_id})

    def start_perf_record(self):
        self.driver.execute_script("mobile: startPerfRecord")

    def stop_perf_record(self):
        self.driver.execute_script("mobile: stopPerfRecord")

    def scroll(self, direction, predicate_string):
        self.driver.execute_script("mobile: scroll", {
            "direction": direction,
            "predicateString": predicate_string,
            "toVisible": True
        })

    def start_xctest_screen_recording(self):
        if self.os_type == "ios":
            return self.driver.execute_script("mobile: startXCTestScreenRecording", {"fps": 24})
        else:
            raise ValueError(f"스크린 녹화는 아이폰에서만 가능합니다.")

    def get_xctest_screen_recording_info(self):
        if self.os_type == "ios":
            return self.driver.execute_script("mobile: getXCTestScreenRecordingInfo")
        else:
            raise ValueError(f"스크린 녹화는 아이폰에서만 가능합니다.")

    def stop_xctest_screen_recording(self):
        if self.os_type == "ios":
            self.driver.execute_script("mobile: stopXCTestScreenRecording")
        else:
            raise ValueError(f"스크린 녹화는 아이폰에서만 가능합니다.")

    def system_alert(self, action="accept", button_name=None):
        if self.os_type == "ios":
            if action == "getButtons":
                buttons = self.driver.execute_script("mobile: alert", {"action": "getButtons"})
                flat_buttons = [item for sublist in buttons for item in sublist]
                return button_name in flat_buttons
            else:
                self.driver.execute_script("mobile: alert", {"action": action, "buttonLabel": button_name})
                return True
        else:
            raise ValueError(f"시스템 알림은 아이폰에서만 가능합니다.")
