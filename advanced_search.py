from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import page
import elemnt
import unittest

class Advanced_Search(unittest.TestCase):

    def set_up(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://eos.ucs.uri.edu/EOSWebOPAC/OPAC/Search/AdvancedSearch.aspx")

    def search_ocean_acidif(self):
        main_page = page.MainPage(self.driver)
        self.assertTrue(main_page.is_title_matches(), "Advanced Search - OPAC Discovery doesn't match.")

        main_page.search_text("ocean acidification")
        main_page.click_go()

        self.search_results_page = page.SearchResultsPage(self.driver)
        self.assertTrue(self.search_results_page.is_results_found(), "No results found.")

    def open_single_result(self, row_num):
        base_page_element = elemnt.BasePageElement()
        row_i = self.driver.find_element(By.ID, 'MainRepeaterDetailRow_' + row_num)
        link_i = row_i.find_element(By.TITLE, 'Click to view complete record')
        link_i.click()

    def tearDown(self):
        self.driver.close()

""" if __name__ == "__main__":
    unittest.main() """

search = Advanced_Search()
search.set_up()
search.search_ocean_acidif()
search.open_single_result('1')
#search.tearDown()