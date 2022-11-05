import time

import undetected_chromedriver
import string
import secrets
import random
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from autoreg.namefake_api import Person
from autoreg.google_sheet import GoogleSheet
# from namefake_api import Person
# from google_sheet import GoogleSheet

spreadsheetId = ""



def reg_outlook(driver: undetected_chromedriver.Chrome, person: Person, line: int):
    mail = "@outlook.com"
    google_sheet = GoogleSheet(spreadsheetId)
    print(f"Line: {line}")
    url = "https://www.microsoft.com/uk-ua/microsoft-365/outlook/email-and-calendar-software-microsoft-outlook"
    create_account_xpath = '//*[@aria-label="Створити безкоштовний обліковий запис Microsoft Outlook"]'
    time.sleep(1)
    driver.switch_to.new_window('tab')
    driver.get(url)
    wait = WebDriverWait(driver, 10)

    driver.implicitly_wait(1)
    driver.find_element(By.XPATH, create_account_xpath).click()
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-1])
    driver.implicitly_wait(1)
    driver.find_element(By.CSS_SELECTOR, "#MemberName").send_keys(person.email_u)
    time.sleep(1)
    if bool(random.getrandbits(1)):
        domain_select = Select(driver.find_element(By.CSS_SELECTOR, '#LiveDomainBoxList '))
        domain_select.select_by_index(1)
        mail = "@hotmail.com"

    driver.find_element(By.CSS_SELECTOR, "#iSignupAction").click()
    time.sleep(4)
    # driver.implicitly_wait(1)
    try:
        driver.find_element(By.CSS_SELECTOR, "#MemberNameError")
        person.email_u = person.email_u + secrets.choice(string.ascii_lowercase)
        driver.find_element(By.CSS_SELECTOR, "#MemberName").clear()
        driver.find_element(By.CSS_SELECTOR, "#MemberName").send_keys(person.email_u)
        driver.find_element(By.CSS_SELECTOR, "#iSignupAction").click()
    except:
        pass

    driver.implicitly_wait(5)
    driver.find_element(By.CSS_SELECTOR, "#PasswordInput").send_keys(person.password)
    driver.implicitly_wait(5)
    driver.find_element(By.CSS_SELECTOR, "#iSignupAction").click()
    driver.implicitly_wait(5)
    driver.find_element(By.CSS_SELECTOR, "#LastName").send_keys(person.name.split(' ')[0])
    driver.implicitly_wait(5)
    driver.find_element(By.CSS_SELECTOR, "#FirstName").send_keys(person.name.split(' ')[1])
    driver.implicitly_wait(5)
    driver.find_element(By.CSS_SELECTOR, "#iSignupAction").click()
    select_day = Select(driver.find_element(By.CSS_SELECTOR, '.datepart0'))
    select_mounth = Select(driver.find_element(By.CSS_SELECTOR, '.datepart1'))
    driver.find_element(By.CSS_SELECTOR, '#BirthYear').send_keys(str(random.randrange(1970, 2000)))
    driver.implicitly_wait(1)
    select_day.select_by_index(random.randrange(0, 30))
    time.sleep(1)
    select_mounth.select_by_index(random.randrange(0, 12))
    driver.implicitly_wait(1)
    driver.find_element(By.CSS_SELECTOR, "#iSignupAction").click()
    # google_sheet.write_data(range_=f"Лист1!B{line}:C{line}", Data=[])
    google_sheet.write_data(range_=f"Лист1!B{line}:C{line}", Data=[person.email_u + mail, person.password])
    # time.sleep(1000)


def setup_proxy(driver: undetected_chromedriver.Chrome, ip: str, port: str):
    url = "chrome-extension://padekgcemlokbadohgkifijomclgjgif/options.html#!/profile/proxy"
    ip_xpath = '//*[@ng-model="proxyEditors[scheme].host"]'
    port_xpath = '//*[@ng-model="proxyEditors[scheme].port"]'
    apply_button_xpath = '//*[@ng-click="applyOptions()"]'
    driver.implicitly_wait(1)
    driver.switch_to.new_window('tab')
    driver.get(url)
    driver.implicitly_wait(1)
    ip_element = driver.find_element(By.XPATH, ip_xpath)
    ip_element.clear()
    ip_element.send_keys(ip)
    port_element = driver.find_element(By.XPATH, port_xpath)
    port_element.clear()
    port_element.send_keys(port)
    time.sleep(3)
    driver.find_element(By.XPATH, apply_button_xpath).click()
    time.sleep(10000)


if __name__ == '__main__':

    # person = Person()
    # print(person)

    options = undetected_chromedriver.ChromeOptions()
    options.add_argument(
        fr'--load-extension=C:\Users\Stefan\PycharmProjects\accounts_manager\extension\Proxy-SwitchyOmega')
    driver = undetected_chromedriver.Chrome(version_main=106, options=options)
    setup_proxy(driver, "192.168.0.1", "9876")
    # reg_outlook(driver, person, line=312)
