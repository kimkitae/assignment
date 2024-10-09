from appium import webdriver
from appium.options.ios import XCUITestOptions

class DriverManager:
    def __init__(self, port):
        self.port = port
        self.driver = None

    def init_driver(self):
        # Appium 2.x의 XCUITest 드라이버 옵션 설정
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
        options.derivedDataPath = "/Users/kimkitae/Library/Developer/Xcode/DerivedData/WebDriverAgent-egvgxluocfqmiggkjczxcuhcygbq/"
        options.autoLaunch = True
        options.wdaLaunchTimeout = 60000.0
        options.waitForQuietness = True
        options.shouldUseCompactResponses = True
        options.networkConnectionEnabled = True
        options.showXcodeLog = False

        # Appium 서버에 연결하여 세션 시작
        self.driver = webdriver.Remote(command_executor=f"http://127.0.0.1:{self.port}", options=options)
        return self.driver

    def quit_driver(self):
        if self.driver:
            self.driver.quit()
            print("드라이버가 종료되었습니다.")
