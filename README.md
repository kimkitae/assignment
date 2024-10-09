# 2차 과제 준비 
---

# 실행 전 사전 조건
- Appium 2.x 설치
- iOS 구동을 위한 `Xcode`, `cartridge`, `libimobiledevice`, `ios-deploy` 설치
- iOS Device 내 개발자모드 활성화
- 단말, xcode 내 Apple 계정 로그인
- `WebDriverAgent` 프로젝트 빌드 및 단말 내 설치
- Capabilities 내 udid, platformVersion, derivedDataPath 값 변경
- 원하는 레포팅 시스템에 맞게 설정
  - Allure
  - ReportPortal
<br>

---

# 환경 구축
- python 3.9.0 버전 
- `pip install -r requirements.txt` 명령어를 통해 패키지 설치
  - 일부 누락된 패키지 존재 할 경우 수동설치
    - `pip install {package_name}`
- 필요에 의해 `Jenkins`, `ReportPortal` 도커 컨테이너 생성
  - 각 폴더 이동 하여 `docker-compose up -d` 명령어 실행

---

# 테스트 실행
### Appium 서버는 별도 실행 없이 코드 내 기본 `4723` 기준으로 포트 사용여부 판단, 미 사용 포트에 대해 Appium 서버 실행 동작
- Pytest를 이용하여 테스트 수행
  - `pytest -v test_sample.py` 
  - `Root` 디렉토리 내 `appium_{port}.log` 파일 생성
  - 터미널 내 Print 항목 확인 필요 시 명령어 뒤 `-s` 옵션 추가
    - `pytest -v test_sample.py -s`

---

# 테스트 결과 생성

## Report 생성 및 실행 방법1 - `allure`
1. `brew install allure` 를 통해 설치
2. `pytest --alluredir=./report` 명령어를 이용하여 테스트 수행
3. `allure generate ./report -o ./report/html` 로 결과 파일 생성
4. `allure open ./report/html` 로 결과 파일 열기

## Report 생성 및 실행 방법2 - `ReportPortal`
1. `pip install pytest-reportportal` 를 통해 설치
2. `report` 폴더 내 `docker-compose up -d` 명령어를 통해 컨테이너 실행
3. `http://localhost:8080` 접속 후 로그인
  - 기본 계정 : `default` / `1q2w3e`
4. 계정 정보 내 `API KEY`생성 후 복사
5. `root`폴더 내 `pytest.ini` 파일 생성, 아래의 정보 추가
```zsh
[pytest]
rp_endpoint = http://localhost:8080
rp_uuid = <API-KEY>
rp_launch = Java launch
rp_project = default_personal
```
6. `pytest -s --reportportal` 명령어를 이용해 테스트 수행
  - 매 테스트 케이스 종료 시 결과 업로드 수행

### `pytest.ini`파일 없이 CommandLine을 통해 수행 방법
```zsh
pytest -s --reportportal \
    --rp-launch="Your Launch Name" \
    --rp-project="default_personal" \
    --rp-endpoint="http://localhost:8080" \
    --rp-uuid="YOUR_API_KEY_HERE
```
---
# Jenkins 설정
- `node-1` Jenkins slave 실행
```zsh
curl -sO http://localhost:8081/jnlpJars/agent.jar
java -jar agent.jar -url http://localhost:8081/ -secret 868c682289d767d09f4b9ebaa416c75c13f6c4bf97396f281d8ef6281be96a97 -name "node-1" -workDir "/Users/kimkitae/jenkins/jenkins_home"
```
---
  

# 전체 테스트 흐름도 
- Master Jenkins
  - 각 종 Job 수행 시 해당 Job을 실행하는 노드로 전달
- 실제 장비 유선 연결되어있는 장비 내 Slave Jenkins 연결
  - 각 종 테스트 수행
  - 테스트 수행 시 git clone하여 항시 최신 코드로 테스트 수행
- 레포팅 시스템 내 테스트 결과 업로드


---

# UI 자동화 코드

## 구조
- `element_attribute_converter.py` - 오브젝트 내 속성을 이용하여 원하는 속성 추출
- `element_gesture_control.py` - 스크롤, 스와이프 관련 동작에 대한 코드 정의
- `element_interaction.py`- 오브젝트 클릭, 좌표 클릭, 텍스트 입력, 텍스트 가져오기 등 오브젝트 상호작용 관련 코드 정의
- `element_visibility_checker.py` - 오브젝트 관련 노출 여부 등 관련 코드 정의
- `execute_method.py`- W3C 명령어 커맨드 코드 정의
- `regex_utility.py`- 텍스트에 대한 정규식 관련 코드 정의
- `common_page.py`- 위 모든 클래스를 통합하여 페이지 단위 테스트 코드 정의

- `conftest.py` - 테스트 코드 실행 시 필요한 초기화 코드 정의
- `driver_manager.py` - 테스트 코드 실행 시 필요한 driver 관련 코드 정의
- `appium_server.py` - appium 서버 실행에 대한 코드 정의

## 동작
1. `conftest`에서 `fixtures`를 통해 생성된 driver를 통해 각 클래스 내 메서드 실행
2. capabilities 를 통해 정의된 값 기준으로 `driver` 초기화
3. `appium_server`클래스 내 `4723` PORT 기준으로 사용가능 여부 판단하여, 사용 불가 시 다른 PORT로 재 시도 후 사용가능 하너 PORT인 경우 APPIUM 서버 실행
4. 테스트 종료 후 `yield`를 통해 생성된 `driver` 종료