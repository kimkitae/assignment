import socket
import time
import requests
import subprocess
from appium.webdriver.appium_service import AppiumService

class AppiumServer:
    def __init__(self):
        self.port = self.find_available_port()
        self.service = AppiumService()
        self.log_file = f'appium_{self.port}.log'  # 로그 파일 이름 설정


    def find_available_port(self, start_port=4723):
        # 사용 가능한 포트를 찾음
        port = start_port
        while not self.is_port_available(port):
            port += 1
        return port

    def is_port_available(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            return sock.connect_ex(('localhost', port)) != 0

    def start(self):
        print("Appium 서버 시작 시도...")
        try:
            appium_path = "/opt/homebrew/bin/appium"
            self.service.start(
                args=[
                    '--address', '127.0.0.1',
                    f'--port={self.port}',
                    f'--log={self.log_file}',
                    '--log-level', 'debug',
                    '--use-plugins', 'execute-driver',
                    '--relaxed-security'
                ],
                main_script=appium_path
            )
            print(f"Appium 서버 시작 명령 실행됨. 포트: {self.port}")

            time.sleep(10)
            # 서버가 시작될 때까지 최대 10초 대기
            for i in range(10):
                if self.service.is_running:
                    print(f"Appium 서버가 포트 {self.port}에서 성공적으로 시작되었습니다.")
                    return
                print(f"Appium 서버 시작 대기 중... ({i+1}/10)")
                time.sleep(1)
            print(f"Appium 서버를 포트 {self.port}에서 시작하는 데 실패했습니다.")
            print(f"로그 파일을 확인하세요: {self.log_file}")
        except Exception as e:
            print(f"Appium 서버 시작 중 오류 발생: {str(e)}")

    def stop(self):
        # Appium 서버 중지
        if self.service.is_running:
            self.service.stop()
            print(f"Appium 서버가 포트 {self.port}에서 중지되었습니다.")
