from page.element_attribute_converter import ElementAttributeConverter, ElementType, PropertyType

class HomePage:
    def __init__(self, driver):
        self.driver = driver

    def click_login_button(self):
        locator = ElementAttributeConverter.ios_predicate_object(ElementType.BUTTON, PropertyType.NAME, "로그인")
        element = self.driver.find_element(*locator)
        element.click()
        print("로그인 버튼이 클릭되었습니다.")
