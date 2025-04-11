from selenium import webdriver
from helpers import is_url_reachable
from data import URBAN_ROUTES_URL
from pages import UrbanRoutesPage
import json
import time
import data
from selenium.common import WebDriverException
from selenium.webdriver.common.by import By

class TestUrbanRoutes:
    @classmethod
    def test_setup_class(cls):
        # do not modify - we need additional logging enabled in order to retrieve phone confirmation code
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(5)
        if is_url_reachable(URBAN_ROUTES_URL):
            print("Connected to the Urban Routes server")
        else:
            print("Cannot connect to Urban Routes. Check the server is on and still running")

    def test_set_route(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert routes_page.get_from() == data.ADDRESS_FROM
        assert routes_page.get_to() == data.ADDRESS_TO

    def test_select_plan(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_supportive_plan()
        assert routes_page.get_current_selected_plan() == 'Supportive'

    def test_fill_phone_number(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        driver = webdriver.Chrome()
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_supportive_plan()
        assert routes_page.get_current_selected_plan() == 'Supportive'
        driver.find_element(By.ID, "Phone number").send_keys("+1 1312344356")
        driver.find_element(By.ID, "Next").click()
        code = None
        for i in range(10):
            try:
                logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                        and 'api/v1/number?number' in log.get("message")]
                for log in reversed(logs):
                    message_data = json.loads(log)["message"]
                    body = driver.execute_cdp_cmd('Network.getResponseBody',
                                                  {'requestId': message_data["params"]["requestId"]})
                    code = ''.join([x for x in body['body'] if x.isdigit()])
            except WebDriverException:
                time.sleep(1)
                continue
            if not code:
                raise Exception("No phone confirmation code found.\n"
                                "Please use retrieve_phone_code only after the code was requested in your application.")
            return code

    def test_fill_card(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        driver = webdriver.Chrome()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_supportive_plan()
        assert routes_page.get_current_selected_plan() == 'Supportive'
        driver.find_element(By.ID, "Payment method").click()
        driver.find_element(By.ID, "Add card").click()
        driver.find_element(By.ID, "Card number (not yours):").send_keys("123400004321")
        driver.find_element(By.ID, "Code").send_keys("12")
        driver.find_element(By.ID, "Link").click()

    def test_comment_for_driver(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        driver = webdriver.Chrome()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_supportive_plan()
        assert routes_page.get_current_selected_plan() == 'Supportive'
        driver.find_element(By.ID, "Message to the driver...").click()
        driver.find_element(By.ID, "Message to the driver").send_keys("Turn the seat warmers on")

    def test_order_blanket_and_handkerchiefs(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        driver = webdriver.Chrome()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_supportive_plan()
        assert routes_page.get_current_selected_plan() == 'Supportive'
        driver.find_element(By.ID, "Order requirements").click()
        driver.find_element(By.ID, "Blanket and handkerchiefs").click()

    def test_order_2_ice_creams(self):
        number_of_ice_creams = 2
        self.driver.get(data.URBAN_ROUTES_URL)
        driver = webdriver.Chrome()
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        routes_page.select_supportive_plan()
        assert routes_page.get_current_selected_plan() == 'Supportive'
        driver.find_element(By.ID, "Order requirements").click()
        for count in range(number_of_ice_creams):
            driver.find_element(By.CLASS_NAME, "counter-plus").click()
    def test_car_search_model_appears(self):
        self.driver.get(data.URBAN_ROUTES_URL)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        user_input = input("Enter the car model you want: ")
        print(f"You entered: {user_input}")

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

