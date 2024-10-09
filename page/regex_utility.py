import re
from page.execute_method import ExecuteMethod
from page.element_attribute_converter import ElementType
import time


class RegexUtility:
    def __init__(self, driver):
        self.driver = driver
        self.execute_method = ExecuteMethod(driver)

    def matchered_text(self, patterns, page_source=None):
        current_page_source = page_source if page_source else self.execute_method.get_page_source_in_json()
        
        if isinstance(current_page_source, dict):
            current_page_source = str(current_page_source)
      
        match = re.search(patterns, current_page_source)
        if match:
            matched_value = match.group(0)
            print(f"패턴과 일치하는 값: {matched_value}")
            return matched_value
        else:
            print("패턴과 일치하는 값이 없습니다.")
            return "null"

    def matchered_text_with_index(self, patterns, index=0, page_source=None):
        current_page_source = page_source if page_source else self.execute_method.get_page_source_in_json()
        if isinstance(current_page_source, dict):
            current_page_source = str(current_page_source)
    
        match = re.search(patterns, current_page_source)
        if match:
            matched_value = match.group(index)
            print(f"패턴과 일치하는 값: {matched_value}")
            return matched_value
        else:
            print("패턴과 일치하는 값이 없습니다.")
            return "null"

    def remove_digits_and_whitespace(self, text):
        return re.sub(r'\d+|\s+', '', text)

    def get_text_by_keyword(self, keyword=None, page_source=None):
        return self.get_expressions(keyword, page_source)

    def get_expressions(self, keyword=None, page_source=None):
        max_retries = 2
        for _ in range(max_retries):
            current_page_source = page_source if page_source else self.execute_method.get_page_source_in_json()
            if isinstance(current_page_source, dict):
                current_page_source = self.dict_to_string(current_page_source)
            
            patterns = {
                "리워드문구": r'Verify identity now',
                "코인수": r'(\d+) Coins are up'
            }

            if keyword and isinstance(keyword, str) and keyword in patterns:
                match = re.search(patterns[keyword], current_page_source)
                if match:
                    return match.group(0)
            
            time.sleep(3)  # 5초 대기 후 재시도
        
        print(f"{keyword}에 해당하는 패턴을 찾지 못했습니다.")
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