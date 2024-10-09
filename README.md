# 과제용 
## 실행 전 사전 조건
- Appium 설치
- iOS 구동을 위한 Xcode, cartridge, libimobiledevice, ios-deploy 설치
- iOS Device 내 개발자모드 활성화
- 단말, xcode 내 Apple 계정 로그인
- WebDriverAgent 프로젝트 빌드 및 단말 내 설치
- Capabilities 내 udid, platformVersion, derivedDataPath 값 변경


## 실행 방법
### Appium 서버는 별도 실행 없이 코드 내 기본 `4723` 기준으로 포트 사용여부 판단, 미 사용 포트에 대해 Appium 서버 실행 동작
- Pytest를 이용하여 테스트 수행
  - `pytest -v test_sample.py` 
  - `Root` 디렉토리 내 `appium_{port}.log` 파일 생성
  - 터미널 내 Print 항목 확인 필요 시 명령어 뒤 `-s` 옵션 추가
    - `pytest -v test_sample.py -s`
