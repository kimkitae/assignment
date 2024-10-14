import re
from helper.execute_method import ExecuteMethod
import time

# 정규식 추출을 위한 클래스 정의
class RegexUtility:
    def __init__(self, driver, os_type, rp_logger):
        # 드라이버, OS 타입, 로거 초기화
        self.logger = rp_logger
        self.os_type = os_type
        self.driver = driver
        self.execute_method = ExecuteMethod(driver, os_type, rp_logger)

    def matchered_text(self, patterns, page_source=None):
        # 주어진 패턴에 맞는 텍스트를 페이지 소스에서 검색
        current_page_source = page_source if page_source else self.execute_method.get_page_source_in_json()
        
        if isinstance(current_page_source, dict):
            current_page_source = str(current_page_source)

        # 패턴과 일치하는 텍스트 검색
        match = re.search(patterns, current_page_source)
        if match:
            matched_value = match.group(0)
            self.logger.info(f"패턴과 일치하는 값: {matched_value}")
            return matched_value
        else:
            self.logger.info("패턴과 일치하는 값이 없습니다.")
            return "null"

    def matchered_text_with_index(self, patterns, index=0, page_source=None):
        # 주어진 인덱스를 기준으로 패턴과 일치하는 텍스트 검색
        current_page_source = page_source if page_source else self.execute_method.get_page_source_in_json()
        if isinstance(current_page_source, dict):
            current_page_source = str(current_page_source)

        # 패턴과 일치하는 텍스트 검색 (인덱스 활용)
        match = re.search(patterns, current_page_source)
        if match:
            matched_value = match.group(index)
            self.logger.info(f"패턴과 일치하는 값: {matched_value}")
            return matched_value
        else:
            self.logger.info("패턴과 일치하는 값이 없습니다.")
            return "null"

    def remove_digits_and_whitespace(self, text):
        # 숫자와 공백을 제거한 텍스트 반환
        return re.sub(r'\d+|\s+', '', text)

    def get_text_by_keyword(self, keyword=None, page_source=None):
        # 키워드를 기준으로 패턴과 일치하는 텍스트를 반환
        return self.get_expressions(keyword, page_source)

    def get_expressions(self, keyword=None, page_source=None):
        # 주어진 키워드를 기반으로 정규 표현식을 통해 텍스트를 검색
        max_retries = 2
        for _ in range(max_retries):
            current_page_source = page_source if page_source else self.execute_method.get_page_source_in_json()
            if isinstance(current_page_source, dict):
                current_page_source = self.dict_to_string(current_page_source)

            # 키워드에 따른 정규 표현식 패턴 정의
            patterns = {
                "리워드문구": r'Verify identity now',  # 미인증 후 앱 진입 시 노출되는 문구
                "코인up": r'(\d+) Coins are up',  # Market 내 코인 증가 수
                "코인down": r'(\d+) Coins are down',  # Market 내 코인 감소 수
                "코인리스트정보": [
                    r'^[A-Z0-9]+$',  # 코인 이름 (예: BTC)
                    r'^\d+x$',  # 레버리지 (예: 100x)
                    r'^\d+(\.\d+)?[MK]$',  # 시가총액 (예: 202.89M)
                    r'^\d{1,3}(,\d{3})*(\.\d+)?$',  # 가격 (예: 60,995.3)
                    r'^-?\d+(\.\d+)?%$'  # 변동률 (예: 1.99%)
                ],
                "이벤트날짜": r'\d{2}\.\d{2}\.\d{2} - \d{2}\.\d{2} UTC',  # airdrop 이벤트 날짜
                "이벤트상태": r'Closed|Opened',  # airdrop 이벤트 상태
                "위클리리더보드카운트": r'\d+',  # 위클리 리더보드 카운트
                "랜덤숫자플러스": r'\d+\+',  # 숫자 뒤에 +가 붙는 형식
                "USDT_ADDRESS": r'^[A-Za-z0-9_-]+$',  # USDT 주소
                "USDT_MEMO": r'^\d+$',  # USDT 메모, 숫자만으로 구성된 문자열
                "assets_data": [r'^[A-Za-z\s]+$',  # 코인 이름 (예: Bitcoin)
                                r'^\d+% APR$|^$',  # APR (예: 5% APR)
                                r'^[A-Z]+$',  # 코인 심볼 (예: BTC)
                                r'^\d+\.\d+$',  # 수량 (예: 0.00000000)
                                r'^[A-Z]+$',  # 단위 (예: BTC)
                                r'^\d+\.\d+$|^$',  # 가치 (예: 0.00)
                                ],
                "알림종류": r'Promotions|System'  # 알림 종류 (예: 프로모션, 시스템)
            }

            if keyword and isinstance(keyword, str) and keyword in patterns:
                pattern = patterns[keyword]

            # 패턴이 리스트일 경우 리스트 반환
            if isinstance(pattern, list):
                return pattern  # 리스트 반환

            # 패턴이 문자열일 경우 정규식 검색
            elif isinstance(pattern, str):
                current_page_source = page_source if page_source else self.execute_method.get_page_source_in_json()
                if isinstance(current_page_source, dict):
                    current_page_source = self.dict_to_string(current_page_source)

            match = re.search(pattern, current_page_source)
            if match:
                self.logger.info(f"{keyword}에 해당하는 패턴을 찾았습니다.")
                return match.group(0)  # 매칭된 텍스트 반환

            time.sleep(3)  # 재시도 전에 대기
            
        self.logger.info(f"{keyword}에 해당하는 패턴을 찾지 못했습니다.")
        return "null"
    
    def dict_to_string(self, d, level=0):
        # 딕셔너리를 문자열로 변환
        result = ""
        for k, v in d.items():
            result += "  " * level + str(k) + ": "
            if isinstance(v, dict):
                result += "\n" + self.dict_to_string(v, level + 1)
            else:
                result += str(v) + "\n"
        return result