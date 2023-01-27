from elemnt import BasePageElement
#from locators import MainPageLocators
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class BasePage(object):
    """initialize base page that will be called from all pages"""
    def __init__(self, driver):
        self.driver = driver

class MainPage(BasePage):
    """Home page action methods come here"""

    def is_title_matches(self):
        return "Advanced Search - OPAC Discovery" in self.driver.title
    
    def search_text(self, input_text):
        searchbox = self.driver.find_element(By.CLASS_NAME, 'AdvancedSearchInputBox')
        searchbox.send_keys(input_text)

    def click_go(self):
        searchbox = self.driver.find_element(By.CLASS_NAME, 'AdvancedSearchInputBox')
        searchbox.send_keys(Keys.RETURN)

class SearchResultsPage(BasePage):

    def is_results_found(self):
        return "No results found." not in self.driver.page_source