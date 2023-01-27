from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# subsidiary objects
from advanced_search import Advanced_Search


def open_result(row_num):
    row_i = driver.find_element(By.ID, 'MainRepeaterDetailRow_' + row_num)
    link_i = row_i.find_element(By.TITLE, 'Click to view complete record')
    link_i.click()
    return None

# execute search
ocean_acidif_search()
assert searchbox.find_element(By.VALUE, 'ocean acidification')
#open_result('1')