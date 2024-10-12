import re
from helper.execute_method import ExecuteMethod
import time
import xml.etree.ElementTree as ET

class RegexUtility:
    def __init__(self, driver, os_type, rp_logger):
        self.logger = rp_logger
        self.os_type = os_type
        self.driver = driver
        self.execute_method = ExecuteMethod(driver, os_type, rp_logger)

    def matchered_text(self, patterns, page_source=None):
        current_page_source = page_source if page_source else self.execute_method.get_page_source_in_json()
        
        if isinstance(current_page_source, dict):
            current_page_source = str(current_page_source)
      
        match = re.search(patterns, current_page_source)
        if match:
            matched_value = match.group(0)
            self.logger.info(f"패턴과 일치하는 값: {matched_value}")
            return matched_value
        else:
            self.logger.info("패턴과 일치하는 값이 없습니다.")
            return "null"

    def matchered_text_with_index(self, patterns, index=0, page_source=None):
        current_page_source = page_source if page_source else self.execute_method.get_page_source_in_json()
        if isinstance(current_page_source, dict):
            current_page_source = str(current_page_source)
    
        match = re.search(patterns, current_page_source)
        if match:
            matched_value = match.group(index)
            self.logger.info(f"패턴과 일치하는 값: {matched_value}")
            return matched_value
        else:
            self.logger.info("패턴과 일치하는 값이 없습니다.")
            return "null"

    def remove_digits_and_whitespace(self, text):
        return re.sub(r'\d+|\s+', '', text)

    def get_text_by_keyword(self, keyword=None, page_source=None):
        return self.get_expressions(keyword, page_source)

    def get_expressions(self, keyword=None, page_source=None):
        max_retries = 2
        print(self.execute_method.get_page_source_in_json())
        for _ in range(max_retries):
            current_page_source = page_source if page_source else self.execute_method.get_page_source_in_json()
            print(type(current_page_source)) 
            if isinstance(current_page_source, dict):
                current_page_source = self.dict_to_string(current_page_source)

            patterns = {
                "리워드문구": r'Verify identity now', # 미인증 후 앱 진입 시 노출되는 문구
                "코인up": r'(\d+) Coins are up', # Market 내 표시되는 코인 수
                "코인down": r'(\d+) Coins are down', # Market 내 표시되는 코인 수
                "코인리스트정보": [
                    r'^[A-Z0-9]+$',                        # 코인 이름 (BTC)
                    r'^\d+x$',                             # 레버리지 (100x)
                    r'^\d+(\.\d+)?[MK]$',                  # 시가총액 (202.89M)
                    r'^\d{1,3}(,\d{3})*(\.\d+)?$',         # 가격 (60,995.3)
                    r'^-?\d+(\.\d+)?%$'                    # 변동률 (1.99%)
                ],
                "이벤트날짜" : r'\d{2}\.\d{2}\.\d{2} - \d{2}\.\d{2} UTC', # airdrop 내 이벤트 날짜 문구
                "이벤트상태" : r'Closed|Opened', # airdrop 내 이벤트 상태 문구
                "위클리리더보드카운트" : r'\d+', # 위클리 리더보드 카운트
                "랜덤숫자플러스" : r'\d+\+', # 랜덤 숫자 뒤에 + 기호가 오는 표현을 위한 정규식
                "USDT_ADDRESS": r'^[A-Za-z0-9_-]+$',  # USDT 주소
                "USDT_MEMO": r'^\d+$',  # 랜덤한 길이의 숫자로만 구성된 문자열
                "assets_data": [r'^[A-Za-z\s]+$',                       # 코인 이름 (예: Bitcoin, Tether USD)
                    r'^\d+% APR$|^$',                       # APR (예: 5% APR) 또는 존재하지 않을 수 있음 (빈 문자열 허용)
                    r'^[A-Z]+$',                            # 코인 심볼 (예: BTC)
                    r'^\d+\.\d+$',                          # 수량 (예: 0.00000000)
                    r'^[A-Z]+$',                            # 단위 (예: BTC)
                    r'^\d+\.\d+$|^$',                       # 가치 (예: 0.00) 또는 존재하지 않을 수 있음 (빈 문자열 허용)
                ],
                "알림종류" : r'Promotions|System'
            }

            if keyword and isinstance(keyword, str) and keyword in patterns:
                pattern = patterns[keyword]

            # 패턴이 리스트일 경우
            if isinstance(pattern, list):
                return pattern  # 리스트 반환

            # 패턴이 문자열일 경우
            elif isinstance(pattern, str):
                current_page_source = page_source if page_source else self.execute_method.get_page_source_in_json()
                if isinstance(current_page_source, dict):
                    current_page_source = self.dict_to_string(current_page_source)

            match = re.search(pattern, current_page_source)
            if match:
                return match.group(0)  # 매칭된 결과 반환

            time.sleep(3)  # 5초 대기 후 재시도
            
        self.logger.info(f"{keyword}에 해당하는 패턴을 찾지 못했습니다.")
        return "null"
    
    def dict_to_string(self, d, level=0):
        result = ""
        for k, v in d.items():
            result += "  " * level + str(k) + ": "
            if isinstance(v, dict):
                result += "\n" + self.dict_to_string(v, level + 1)
            else:
                result += str(v) + "\n"
        return result
    
    def xml_to_json(self, element):
        result = {}
        for child in element:
            child_data = self.xml_to_json(child)
            if child.tag in result:
                if type(result[child.tag]) is list:
                    result[child.tag].append(child_data)
                else:
                    result[child.tag] = [result[child.tag], child_data]
            else:
                result[child.tag] = child_data
        if element.text and element.text.strip():
            result['#text'] = element.text.strip()
        if element.attrib:
            result['@attributes'] = element.attrib
        return result

