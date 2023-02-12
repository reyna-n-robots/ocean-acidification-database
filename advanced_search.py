from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import openpyxl
import time
import unittest

import page
import elemnt

all_entries = []
all_labels = []

all_data_dict = {
    "NSGL Document #:" : [],
    "Sea Grant Program/Affiliate:" : [],
    "Title:" : [],
    "Author:" : [],
    "Publication Year :" : [],
    "Publisher:" : [],
    "Publication Type:" : [],
    "Program Report #:" : [],
    "Grant/Contract #:" : [],
    "Project #:" : []
}

class Advanced_Search(unittest.TestCase):

    def set_up(self):
        self.driver = webdriver.Firefox()
        self.driver.get("http://eos.ucs.uri.edu/EOSWebOPAC/OPAC/Search/AdvancedSearch.aspx")

    def back_one(self):
        self.driver.back()
    
    def next_page(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl00_webopacContentHolder_SearchTitleListControl_titleListNav1_arrowRight')))
        arrow = self.driver.find_element(By.ID, 'ctl00_webopacContentHolder_SearchTitleListControl_titleListNav1_arrowRight')
        arrow.click()

    def search_ocean_acidif(self):
        main_page = page.MainPage(self.driver)
        self.assertTrue(main_page.is_title_matches(), "Advanced Search - OPAC Discovery doesn't match.")

        main_page.search_text("ocean acidification")
        main_page.click_go()

        self.search_results_page = page.SearchResultsPage(self.driver)
        self.assertTrue(self.search_results_page.is_results_found(), "No results found.")
    
    def write_to_dict(self, key, value):
        if "Author:" not in key and "Project #:" not in key:
            if key in all_data_dict.keys():
                if value.isnumeric():
                    value = int(value)
                all_data_dict[key] += [value]
    
    def add_empty(self, labels):
        for k in all_data_dict.keys():
            if k not in labels:
                all_data_dict[k] += ['']

    def open_single_result(self, row_num):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'MainRepeaterDetailRow_'+row_num)))
        row_i = self.driver.find_element(By.ID, 'MainRepeaterDetailRow_' + row_num)
        link_i = row_i.find_element(By.CLASS_NAME, 'NoVisitNoUnder')
        link_i.click()
    
    def collect_single_result(self, row_num):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'ctl00_ctl00_webopacContentHolder_detailContent_BibliographicDetail_BibDetailRepeater_ctl01_DataCell')))

        entry = []
        labels = []

        long_id = 'ctl00_ctl00_webopacContentHolder_detailContent_BibliographicDetail_BibDetailRepeater_ctl'
        label = ''
        i = 0
        
        try:
            while label != 'Notes:' and label != 'Abstract:':
                i += 1
                if i < 10:
                    label = self.driver.find_element(By.ID, long_id + '0' + str(i) + '_LabelCell').text
                    labels.append(label)
                    value = self.driver.find_element(By.ID, long_id + '0' + str(i) +'_DataCell').text
                    entry.append(value) #occurring at index i-1
                else:
                    label = self.driver.find_element(By.ID, long_id + str(i) + '_LabelCell').text
                    labels.append(label)
                    value = self.driver.find_element(By.ID, long_id + str(i) +'_DataCell').text
                    entry.append(value)

                self.write_to_dict(label, value)
                
                if label == 'Author:':
                    author_row = i
                elif label == 'Publication Year :':
                    pubyear_row = i
                elif label == 'Project #:':
                    proj_num_row = i

                try:
                    label = self.driver.find_element(By.ID, long_id + '0' + str(i+1) + '_LabelCell').text
                except:
                    label = self.driver.find_element(By.ID, long_id + str(i+1) + '_LabelCell').text
        except:
            pass

        try:
            diff = pubyear_row - author_row
            for j in range(1,diff):
                entry[author_row - 1] += '; ' + entry[author_row - 1 + j]
            all_data_dict["Author:"] += [entry[author_row - 1]]
        except:
            pass

        try:
            if proj_num_row != len(labels)-1:
                for j in range(proj_num_row, len(labels)):
                    if labels[j] == '':
                        entry[proj_num_row - 1] += ', ' + entry[j]
            all_data_dict['Project #:'] += [entry[proj_num_row - 1]]
            #print(str(row_num) + ' : ' + all_data_dict['Project #:'][-1])
        except UnboundLocalError:
            #all_data_dict['Project #:'] += ['']
            #print('------ ' + str(row_num) + ' labels: ' + str(labels))
            pass
        except IndexError:
            pass

        self.add_empty(labels)
        all_entries.append(entry)
        all_labels.append(labels)

        #print(str(row_num) + ' : ' + all_data_dict['Project #:'][-1])

    def write_to_excel(self):
        dataframe = pd.DataFrame(all_data_dict)
        writer = pd.ExcelWriter('database.xlsx', mode='a', if_sheet_exists='replace', engine='openpyxl')
        dataframe.to_excel(writer, sheet_name='Sheet1', startrow=1, index=False, header=False)
        writer.close()

    def tearDown(self):
        self.driver.close()

def loop_through(start_num, end_num, page_num):
    for n in range(start_num, end_num + 1):
        search.open_single_result(str(page_num * 100 + n))
        #print(str(page_num * 100 + n))
        search.collect_single_result(n)
        search.back_one()

search = Advanced_Search()
search.set_up()
search.search_ocean_acidif()

loop_through(1,100,0)
search.next_page()
loop_through(1,100,1)
search.next_page()
loop_through(1,47,2)
try:
    search.write_to_excel()
except ValueError:
    print(len(all_data_dict['Project #:']))
    #print(all_data_dict['Project #:'])

search.tearDown()