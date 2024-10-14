# 과제물 
---
# 환경 구축
- **개발 환경**
  - **Appium - 2.11.5**
  - **uiautomator2 - 3.8.0**
  - **xcuitest - 7.27.1**
  - **Python - 3.9.1**
--- 

# 사전 환경 설정 방법
- **Appium 2.x 설치 및 기본 드라이버 설치**
```zsh
# Appium 2.x 설치 (npm 이용)
npm install -g appium

# Android 드라이버(UiAutomator2) 설치
appium driver install uiautomator2
# iOS 드라이버(XCUiTest) 설치
appium driver install xcuitest

# 추가 플러그인 설치
appium plugin install execute-driver
appium plugin install relaxed-caps
```
- Android - Java, SDK 설치 및 환경 변수 설정
```zsh
# Java 설치 (Homebrew 이용)
brew install openjdk

# 설치된 Java 버전 확인
java -version

# 환경 변수 설정 (bash, zsh 셸에 맞게 설정)
echo 'export JAVA_HOME=$(/usr/libexec/java_home)' >> ~/.zshrc
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> ~/.zshrc

# 설정 적용
source ~/.zshrc

# Android Studio 설치
brew install --cask android-studio

# 환경 변수 설정 (zsh 기준)
echo 'export ANDROID_HOME=$HOME/Library/Android/sdk' >> ~/.zshrc
echo 'export PATH=$ANDROID_HOME/platform-tools:$PATH' >> ~/.zshrc
echo 'export PATH=$ANDROID_HOME/emulator:$PATH' >> ~/.zshrc
echo 'export PATH=$ANDROID_HOME/tools:$PATH' >> ~/.zshrc
echo 'export PATH=$ANDROID_HOME/tools/bin:$PATH' >> ~/.zshrc
```
- **iOS 설정**

```zsh
# Xcode 설치 및 설정
xcode-select --install
sudo xcode-select -s /Applications/Xcode.app/Contents/Developer

# 필수 도구 설치
brew install libimobiledevice
brew install carthage
brew install ios-deploy
```
- iOS, Android Device 개발자모드 활성화
- **iOS의 경우 Device, xcode 내 Apple 계정 로그인**
- `WebDriverAgent` 프로젝트 빌드 및 단말 설치 (`Integration`. `Ruuner`, `Lib`)
```zsh
# 기본적으로 아래의 경로에 존재
/Users/<유저>/.appium/node_modules/appium-xcuitest-driver/node_modules/appium-webdriveragent/
```
 - [WebDriverAgent 설치](https://m.blog.naver.com/wooy0ng/223473944904) 내용 참조

- 필요 시 `Allure` 또는 `ReportPortal` 설치 [테스트 리포팅 방법](#테스트-리포팅-방법) 참조<br><br>

- Git clone 
  - `https://github.com/kimkitae/assignment.git` 

- `.env`파일을 아래의 정보와 같이 프로젝트 Root에 생성 
  - Capabilities 내 `udid`, `platformVersion`, `derivedDataPath` 값
  - 테스트 계정 정보
 
```.env
"""
    iOS Device Information
"""
IOS_UDID=<단말 UDID>
IOS_PLATFORM_VERSION=<단말 OS 버전>
APP_BUNDLE=<실행 앱 Bundle ID>
WEBDRIVERAGENT_PATH=<WebDriverAgent 빌드된 경로>

"""
    Android Device Information
"""
ANDROID_UDID=<단말 UDID>
ANDROID_PLATFORM_VERSION=<단말 OS>
APP_PACKAGE=<실행 앱 Package>


"""
    User Information
"""
EMAIL=<테스트 계정 이메일>
PHONE = <테스트 계정 전화번호 ("+8201000000000")>
NAME = <테스트 계정 이름 ("gildong hong")>
LEVEL = <테스트 계정의 레벨 정보 ("Level 2")>
```
- Python 패키지 설치
```
pip install -r requirements.txt

#일부 패키지 누락되었을 경우 아래의 패키지 수동 설치 pip `install {package_name}`
pip install reportportal-client
pip install python-dotenv
pip install pytest-reportportal
pip install pytest
pip install Appium-Python-Clien`
pip install allure-pytest
```
---

# 테스트 실행 방법
- 테스트 실행은 항상 프로젝트 `Root`에서 수행한다. (Fixture 사용을 위함)

```
# 기본 테스트 실행
pytest test_case -s 
```
- `pytest` Command 로 시작
- 테스트 수행 할 `폴더` or `.py 파일` 입력
  - 폴더의 경우 `test`라는 `prefix` 이름의 `.py` 파일들을 테스트 파일로 인식
  - 파일의 경우 `test`라는 `prefix` 이름의 `def `함수들을 테스트 케이스로 인식
- 수행 할 OS 정보 (미 입력 시 기본 iOS 수행)
- 콘솔을 통한 `logger` - `INFO` 정보 확인 필요 시 `--log-cli-level=INFO` 추가 <선택옵션>
```zsh
#iOS 수행
pytest test_case -s --os=ios

#Android 수행
pytest test_case -s --os=android

#logger 내용 콘솔 출력
pytest test_case --log-cli-level=INFO
```
- Report 시스템 사용 시 해당 패키지에 따라 아래 커맨드 사용 <선택옵션>
```
# ReportPortal 사용
pytest test_case --os=<ios or android> --reportPortal

# Allure
pytest test_case --os=<ios or android> --alluredir=./report
```

---

# 테스트 리포팅 방법
**2개의 방법으로 리포팅이 가능하며, 모두 웹 서비스 형태로 구동되어 웹으로 확인 가능**<br>
**logger에 의해 모든 리포트 시스템에서 Fail 항목 내 상세 Log 확인 가능**


## Allure
- `brew install allure` 설치
- 테스트 수행 시 아래의 Command 순으로 입력

```zsh
# 테스트 수행 시 테스트 결과 파일 저장위치 지정
pytest <테스트 폴더/파일> <os선택> --alluredir=<리포트 생성을 위한 파일 저장 위치>

# 생성된 결과 파일을 이용하여 HTML 파일로 Generate
allure generate <위 지정한 폴더> -o <결과 HTML 만들어질 폴더 경로>

# 생성된 HTML 실행
allure open <결과 HTML 만들어진 경로>
```
- **Sample 리포트 확안하기 (프로젝트 root 위치에서 아래 커맨드 수행)**
  - `allure open ./report/allure/android/html`
  - `allure open ./report/allure/ios/html`


## ReportPortal
- `Docker for Desktop`설치
- `report` 폴더 내 `docker-compose.yml` 파일로 컨테이너 생성
  - `docker-compose up -d` 실행
- 컨테이너 생성 후 `http://localhost:8080` 접속
 - 기본 계정 : `defalut`/ `1q2w3e`
- 프로젝트 `Root`내 `pytest.ini`파일을 아래 내용으로 생성 
```
[pytest]
rp_endpoint = http://localhost:8080
rp_api_key = <ReportPortal 로그인 후 계정 내 API KEY 생성> 
rp_launch = <테스트 수행되어 저장될 이름>
rp_project = default_personal

```
- 테스트 수행 시 아래의 Command로 수행
```
pytest <테스트 폴더/파일> <os선택> --reportportal
```

- `pytest.ini`파일 없이 CommandLine을 통해 수행 방법
```zsh
pytest -s --reportportal \
    --rp-launch="Your Launch Name" \
    --rp-project="default_personal" \
    --rp-endpoint="http://localhost:8080" \
    --rp-api-key="YOUR_API_KEY_HERE
```
- [Test Sample 리포트 보기](https://report.kimkitae.com/ui/#daearcdo_personal/launches/all/1)
  - 로그인 정보 : `default`/ `1q2w3e`
---

# UI 자동화 코드 구조

전체 프로젝트 구조

본 프로젝트는 UI 테스트 자동화를 위한 다양한 기능들을 개별 파일로 분리하여 관리합니다. 각 파일은 특정한 역할과 책임을 가지며, 이를 통해 전체 코드의 가독성 및 유지보수성을 높였습니다. 아래는 주요 파일들의 구조와 역할을 설명합니다.

### 폴더 구조
- helper
  - 공용 기능 함수 정의
- chromedriver
  - Android WebView Context 사용을 위한 ChromeDriver (ARM) 존재
- page
  - 각 화면/기능 단위로 함수 정의 

### 주요 파일 설명
- helper : 공통 기능 함수 정의 
  - `element_attribute_converter.py`: 오브젝트 내 속성을 이용해 원하는 속성 추출
  - `element_gesture_control.py`: 스크롤, 스와이프 등 동작 정의
  - `element_interaction.py`: 오브젝트 클릭, 텍스트 입력 등 상호작용 관련 코드
  - `element_visibility_checker.py`: 오브젝트의 노출 여부 확인 관련 코드
  - `execute_method.py`: W3C 명령어 커맨드 코드 정의
  - `regex_utility.py`: 정규식 관련 유틸리티 코드
- chromedriver : Android WebView Context 사용을 위한 `ChromeDriver` (ARM) 존재 
- jenkins : `Jenkins` 컨테이너 생성을 위한 `docker-compose.yml` 파일
- report : Report 결과 데이터 및 `reportportal` 컨테이너 생성을 위한 `docker-compose.yml`파일 존재
  - `allure`폴더 내 `allure generate ./report/allure -o ./report/allure/html` 로 확인 가능
- page : 각 화면/기능 별 기능함수 정의
  - `common_page`: helper 파일들을 정의, 사용편의를 위해 기능함수 재정의
- test_case : 테스트 케이스 정의
- `appium_server`: `AppiumService`를 이용하여 테스트 수행 시 자동 Appium 실행
  - 기본 `4723`Port로 실행 시도, 해당 Port 사용 중인 경우 다른 `Port`를 이용하여 실행
- `conftest.py`: `driver`, 서버 실행, addoption 및 `fixture` 선언
- `driver_manager.py`: `driver`생성을 위한 Capabilities, appium server 설정

---
# 트러블슈팅

Q.`AppiumServer`실행 시 자동 서버 실행이 되지 않아요.
  - A. 수동으로 `appium -p <port>`로 실행하여 `driver.manager.py`에 appium 서버 port 정보 수기변경 해주세요.<br>

Q.`Execute Method` 기능이 정상적으로 동작하지 않아요.
  - A. `xcuitest` 드라이버를 업데이트 해주세요. 또한 사용하는 단말 또한 최소 `iOS 16` 이상 버전을 사용해주세요. W3C 기능은 최신 `UIAutomator2`, `XCUITest` 드라이버에서 동작합니다.

Q. Console를 통해 테스트 진행 상황, 테스트 결과를 볼 수 없나요?
  - A. `logger` 출력을 활성화하여 확인 가능합니다. 테스트 수행 커맨드 내 `--log-cli-level=INFO`를 입력해주세요.

Q. `ReportPortal` 컨네이너 생성 후 기존 데이터들이 남아 있어요.
  - A. 바로 테스트 수행없이도 기존 결과를 보여드리기 위해 `./report` 폴더를 바인딩 마운트하여 사용하고 있어 내 폴더의 데이터들을 삭제 해주시면 됩니다.

Q. Android Webview Context 전환이 실패 해요.
  - A. 테스트 하시는 단말의 버전과 호환되는 Chromedriver를 다운로드하여 프로젝트 내 chromedriver 폴더에 넣어주세요.

---