from appium import webdriver
from appium.options.ios import XCUITestOptions
from appium.options.android import UiAutomator2Options

class DriverManager:
    def __init__(self, port, os_type):
        self.port = port
        self.os_type = os_type
        self.driver = None

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
        options.udid = "00008101-000125D40202001E"
        options.bundleId = "com.aqx.prex"
        options.platform_version = "18.0"
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
        options.derivedDataPath = "/Users/kimkitae/Library/Developer/Xcode/DerivedData/WebDriverAgent-egvgxluocfqmiggkjczxcuhcygbq"
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
        options.appPackage = "com.aqx.prex"
        options.appActivity = "com.aqx.prex.MainActivity"
        # ... (안드로이드 관련 옵션들 추가)
        return options

    def quit_driver(self):
        if self.driver:
            self.driver.quit()
            print("드라이버가 종료되었습니다.")
