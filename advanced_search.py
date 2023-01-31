from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import xlsxwriter

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
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'MainRepeaterDetailRow_'+row_num)))
        row_i = self.driver.find_element(By.ID, 'MainRepeaterDetailRow_' + row_num)
        link_i = row_i.find_element(By.CLASS_NAME, 'NoVisitNoUnder')
        link_i.click()
    
    def collect_single_result(self, row_num):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl00_ctl00_webopacContentHolder_detailContent_BibliographicDetail_BibDetailRepeater_ctl01_DataCell')))

        entry = [0] * 13

        long_id = 'ctl00_ctl00_webopacContentHolder_detailContent_BibliographicDetail_BibDetailRepeater_ctl'
        
        # works manually for now but will have to change to: stop reading when you hit "notes" --> break
        # if it's just numbers and not any other characters, convert back to int or float
        for i in range(1,14):
            if i < 10:
                label = self.driver.find_element(By.ID, long_id + '0' + str(i) + '_LabelCell').text
                entry[i-1] = self.driver.find_element(By.ID, long_id + '0' + str(i) +'_DataCell').text

                if label == 'Author:':
                    author_row = i
                elif label == 'Publication Year :':
                    pubyear_row = i

            else:
                label = self.driver.find_element(By.ID, long_id + str(i) + '_LabelCell').text
                entry[i-1] = self.driver.find_element(By.ID, long_id + str(i) +'_DataCell').text
                
                if label == 'Author:':
                    author_row = i
                elif label == 'Publication Year :':
                    pubyear_row = i

        diff = pubyear_row - author_row
        for j in range(1,diff):
            entry[author_row - 1] += '; ' + entry[author_row]
            entry.pop(author_row)

        print(entry)

        dataframe = pd.DataFrame([entry])
        writer = pd.ExcelWriter('database.xlsx', engine='xlsxwriter')
        dataframe.to_excel(writer, sheet_name='Sheet1', startrow=row_num+1, index=False, header=False)
        writer.close()


    def tearDown(self):
        self.driver.close()

""" if __name__ == "__main__":
    unittest.main() """

search = Advanced_Search()
search.set_up()
search.search_ocean_acidif()
search.open_single_result('1')
search.collect_single_result(1)
#search.tearDown()