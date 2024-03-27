from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from bs4 import BeautifulSoup
from security import safe_requests
from time import sleep

import os

class ApartmentData:

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.response = safe_requests.get("https://appbrewery.github.io/Zillow-Clone/")
        self.soup = BeautifulSoup(self.response.text, "html.parser")

    def open_form(self):
        self.driver.get(
            "https://docs.google.com/forms/d/e/1FAIpQLScCjlt90DnhF_qlPe-fBmw7ArafcuhpdnkT8cCCbiUDrrBSXg/viewform?usp=sf_link")

    def get_listing_links(self):
        link_elements = self.soup.find_all(name="a", class_="StyledPropertyCardDataArea-anchor")
        listing_links = [a['href'] for a in link_elements]

        return listing_links

    def get_listing_addresses(self):
        address_elements = self.soup.find_all(name="address")
        address_list = [address.text.rstrip().lstrip().strip('\n') for address in address_elements]

        return address_list

    def get_price_listings(self):
        price_elements = self.soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine")
        price_list = [price.text.strip('/mo').strip('+ 1bd') for price in price_elements]

        return price_list

    def enter_data(self):
        address_list = self.get_listing_addresses()
        prices = self.get_price_listings()
        links = self.get_listing_links()
        num_apartments = len(address_list)
        self.open_form()

        for i in range(num_apartments):
            sleep(1)
            inputs = self.driver.find_elements(By.CSS_SELECTOR, value=".RdH0ib .zHQkBf, .RdH0ib .tL9Q4c")
            address_input = inputs[0]
            price_input = inputs[1]
            link_input = inputs[2]

            address_input.click()
            address_input.send_keys(address_list[i])
            price_input.click()
            price_input.send_keys(prices[i])
            link_input.click()
            link_input.send_keys(links[i])

            submit = self.driver.find_element(By.CSS_SELECTOR, value=".Y5sE8d")
            submit.click()
            self.driver.implicitly_wait(4)
            next = self.driver.find_element(By.LINK_TEXT, value="Submit another response")
            next.click()
            self.driver.implicitly_wait(4)

        messagebox.showinfo(title="Finished", message="Data gathering process complete.")
        self.driver.quit()

