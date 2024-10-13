from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.options.android import UiAutomator2Options
from dotenv import load_dotenv
import os

class DriverManager:
    def __init__(self, port, os_type):
        self.port = port
        self.os_type = os_type
        self.driver = None
        load_dotenv()

    def init_driver(self):
        if self.os_type == "ios":
            options = self._get_ios_options()
        elif self.os_type == "android":
            options = self._get_android_options()
        else:
            raise ValueError(f"Unsupported OS type: {self.os_type}")

        self.driver = webdriver.Remote(command_executor=f"http://127.0.0.1:{self.port}", options=options)
        return self.driver

    def _get_ios_options(self):
        options = XCUITestOptions()
        options.platformName = "iOS"
        options.deviceName = "iPhone"
        options.udid = os.getenv("IOS_UDID")
        options.bundleId = os.getenv("APP_PACKAGE")
        options.platform_version = os.getenv("IOS_PLATFORM_VERSION")
        options.automationName = "XCUITest"
        options.noReset = True
        options.fullReset = False
        options.usePrebuiltWDA = True
        options.nativeWebTap = True
        options.reduceMotion = True
        options.reduceTransparency = True
        options.wdaConnectionTimeout = 60000.0
        options.webviewConnectTimeout = 90000.0
        options.launchWithIDB = True
        options.startIWDP = True
        options.maxTypingFrequency = 50.0
        options.useJSONSource = True
        options.useNativeCachingStrategy = True
        options.skipUnlock = False
        options.forceAppLaunch = True
        options.locationServicesEnabled = True
        options.resetLocationService = True
        options.includeDeviceCapsToSessionInfo = True
        options.maxAPILatency = 60000.0
        options.derivedDataPath = os.getenv("WEBDRIVERAGENT_PATH")
        options.autoLaunch = True
        options.wdaLaunchTimeout = 60000.0
        options.waitForQuietness = True
        options.shouldUseCompactResponses = True
        options.networkConnectionEnabled = True
        options.showXcodeLog = False

        return options

    def _get_android_options(self):
        options = UiAutomator2Options()
        options.platformName = "Android"
        options.deviceName = "Android Device"
        options.appPackage = os.getenv("APP_PACKAGE")
        options.appActivity = f"{os.getenv('APP_PACKAGE')}.MainActivity"
        options.autoGrantPermissions = True
        options.udid = os.getenv("ANDROID_UDID")
        options.platformVersion = os.getenv("ANDROID_PLATFORM_VERSION")
        options.automationName = "UiAutomator2"
        options.noReset = True
        options.fullReset = False
        options.recreateChromeDriverSessions = True
        options.chromedriver_executable = "./chromedriver/chromedriver"

        return options

    def quit_driver(self):
        if self.driver:
            self.driver.quit()
            print("드라이버가 종료되었습니다.")
