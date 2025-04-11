from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

class UrbanRoutesPage:
    #Locators
    FROM_FIELD = (By.ID, 'from')
    TO_FIELD = (By.ID, 'to')
    CUSTOM_OPTION_LOCATOR = (By.XPATH, '//div[@text()="Custom"]')
    CLICK_CALL_TAXI_BUTTON = (By.XPATH, '//button[contains(text(), "Call a taxi")]')
    PHONE_NUMBER_INPUT_LOCATOR = (By.ID, 'phone')
    SUBMIT_PHONE_NUMBER_LOCATOR = (By.XPATH, '//button[@type="submit"]')
    PAYMENT_TYPE_LOCATOR = (By.XPATH, '//div[@class="pp-text"]')
    ADD_CARD_LOCATOR = (By.XPATH, '//div[@class="modal"//div[@class="pp-row disabled"]')
    CARD_NUMBER_LOCATOR = (By.ID, 'input[id="number"]')
    CARD_CODE_LOCATOR = (By.ID, 'input[id="code"]')
    COMMENT_FROM_DRIVER_LOCATOR = (By.ID, 'comment')
    SUPPORTIVE_ICON_LOCATOR = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1[/div[5]')
    BLANKET_AND_HANDKERCHIEFS_LOCATOR = (By.XPATH, '//span[@class="slider round"]')
    ADD_ICE_CREAM_LOCATOR = (By.XPATH, '//div[@class="r-group"//div[@class=counter-plus"]')
    ORDER_NUMBER_LOCATOR = (By.XPATH, '//div[@class="order-number"]')
    select_supportive_plan = (By.NAME, 'Supportive')
    get_current_selected_plan = (By.CLASS_NAME, 'tcard-title')

    def __init__(self,driver):
        self.driver = driver

    def set_from(self, from_address):
        from_field = WebDriverWait(self.driver, 3).until(
            expected_conditions.visibility_of_element_located(self.FROM_FIELD))
        from_field.send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.TO_FIELD).send_keys(to_address)
    def get_from(self):
        return self.driver.find_element(*self.FROM_FIELD).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.TO_FIELD).get_property('value')

    def click_call_taxi_button(self):
        WebDriverWait(self.driver, 3).until(expected_conditions.visibility_of_element_located(self.CLICK_CALL_TAXI_BUTTON),
        self.driver.find_element(*self.CLICK_CALL_TAXI_BUTTON))

    def set_route(self, from_address, to_address):
        self.set_from(from_address)
        self.set_to(to_address)
        self.click_call_taxi_button()


