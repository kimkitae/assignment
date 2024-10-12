import json
import time
import pytest
import xml.etree.ElementTree as ET
import logging
from page.assets_page import AssetsPage
from page.challenge_page import ChallengePage
from page.etc_page import EtcPage
from helper.execute_method import ExecuteMethod
from page.market_page import MarketPage
from page.common_page import CommonPage
from page.login_page import LoginPage
from reportportal_client import RPLogger, RPLogHandler
from page.element_attribute_converter import ElementType, PropertyType, StringType

class TestScenario:
    
    @pytest.fixture(autouse=True)
    def setup(self, driver, os_type, rp_logger):
        self.driver = driver
        self.os_type = os_type
        self.common_page = CommonPage(driver, os_type, rp_logger)
        self.login_page = LoginPage(driver, os_type, rp_logger)
        self.market_page = MarketPage(driver, os_type, rp_logger)
        self.challenge_page = ChallengePage(driver, os_type, rp_logger)
        self.assets_page = AssetsPage(driver, os_type, rp_logger)
        self.etc_page = EtcPage(driver, os_type, rp_logger)
        self.execute_method = ExecuteMethod(driver, os_type, rp_logger)

        self.logger = rp_logger
    
    def test_first_test(self):

        time.sleep(15)
        coin_up_count = self.common_page.get_text_by_keyword("코인up")
        coin_down_count = self.common_page.get_text_by_keyword("코인down")
        print(coin_up_count)
        print(coin_down_count)

    def get_page_source_as_json(self):
        # 페이지 소스를 가져옵니다
        page_source = self.driver.page_source
        
        # XML 문자열을 파싱하여 ElementTree 객체로 변환합니다
        root = ET.fromstring(page_source)
        
        # ElementTree를 딕셔너리로 변환합니다
        page_dict = self.elem_to_dict(root)
        
        # 딕셔너리를 JSON 문자열로 변환합니다
        page_json = json.dumps(page_dict, ensure_ascii=False, indent=2)
        
        # JSON 출력
        print(page_json)
        
        # 로그에 기록
        self.logger.info("페이지 소스를 JSON 형태로 변환했습니다.")
        
        return page_json



    def elem_to_dict(self, elem):
        result = {}
        for child in elem:
            child_dict = self.elem_to_dict(child)
            if child.tag in result:
                if type(result[child.tag]) is list:
                    result[child.tag].append(child_dict)
                else:
                    result[child.tag] = [result[child.tag], child_dict]
            else:
                result[child.tag] = child_dict
        if elem.attrib:
            result['@attributes'] = elem.attrib
        if elem.text:
            text = elem.text.strip()
            if text:
                result['#text'] = text
        return result
