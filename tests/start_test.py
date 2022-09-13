#!/usr/bin/python3


from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep



def list_of_dictionaries(text, list_index):
    return_list = []
    split_list = []
    for i in text.split('\n'):
        split_list.append(i.split(' ')) #[['3.10', 'bugfix', '2021-10-04', '2026-10', 'PEP', '619'], 
    for i in split_list:
        i[-2:] = [' '.join(i[-2:])]     #[['3.10', 'bugfix', '2021-10-04', '2026-10', 'PEP 619'], [
    for i in split_list:
        dictionary = dict(zip(list_index, i))
        return_list.append(dictionary)  #[{'Python version': '3.9', 'Maintenance status': 'security', 'First released': '2020-10-05', 'End of support': '2025-10', 'Release schedule': 'PEP 596'}, {'
    return return_list


driver = webdriver.Remote(command_executor='http://selenium-grid:4444/wd/hub',options=webdriver.ChromeOptions())

sleep(5)

driver.get('https://www.python.org/downloads/')

sleep(5)

elements = driver.find_elements(By.XPATH, "//div[@class='row active-release-list-widget']/ol[@class='list-row-container menu']")

text_result = elements[0].text

with open('/tests/output', 'w') as file:
    file.write(text_result)


index_list = ['Python version', 'Maintenance status', 'First released', 'End of support', 'Release schedule']

returned_list = list_of_dictionaries(text_result, index_list)


print(returned_list)

driver.close()

driver.quit()
