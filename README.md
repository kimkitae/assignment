# 2차 과제 준비 
## 실행 전 사전 조건
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


# 테스트 실행
### Appium 서버는 별도 실행 없이 코드 내 기본 `4723` 기준으로 포트 사용여부 판단, 미 사용 포트에 대해 Appium 서버 실행 동작
- Pytest를 이용하여 테스트 수행
  - `pytest -v test_sample.py` 
  - `Root` 디렉토리 내 `appium_{port}.log` 파일 생성
  - 터미널 내 Print 항목 확인 필요 시 명령어 뒤 `-s` 옵션 추가
    - `pytest -v test_sample.py -s`

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
```
[pytest]
rp_endpoint = http://localhost:8080
rp_uuid = <API-KEY>
rp_launch = Java launch
rp_project = default_personal
```
6. `pytest -s --reportportal` 명령어를 이용해 테스트 수행
  - 매 테스트 케이스 종료 시 결과 업로드 수행

### `pytest.ini`파일 없이 CommandLine을 통해 수행 방법
```
pytest -s --reportportal \
    --rp-launch="Your Launch Name" \
    --rp-project="default_personal" \
    --rp-endpoint="http://localhost:8080" \
    --rp-uuid="YOUR_API_KEY_HERE
```