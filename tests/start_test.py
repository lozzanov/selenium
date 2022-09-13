#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import pymysql

def list_of_dictionaries(text, list_index):
    '''
    This function takes strings from Selenium Grid  and return it to organized list ot dictionries.
    '''
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

def insert(dict_python):
    '''
    This function takes the keys and the values of a dictionary and prepares them in a SQL Query.
    '''
    columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in dict_python.keys())
    values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in dict_python.values())
    return "INSERT IGNORE INTO %s ( %s ) VALUES ( %s );" % ('tbl_versions', columns, values)


'''
Starting the remote webdriver in selenium-grid container.
'''

driver = webdriver.Remote(command_executor='http://selenium-grid:4444/wd/hub',options=webdriver.ChromeOptions())
sleep(5)
driver.get('https://www.python.org/downloads/')
sleep(5)
elements = driver.find_elements(By.XPATH, "//div[@class='row active-release-list-widget']/ol[@class='list-row-container menu']")
text_result = elements[0].text

# Data fetched from the driver is saved in file to be used in unittest.
with open('/tests/output', 'w') as file:
    file.write(text_result)

index_list = ['Python version', 'Maintenance status', 'First released', 'End of support', 'Release schedule']
returned_list = list_of_dictionaries(text_result, index_list)

'''
The list of dictionaries has to be inserted in database container
'''
conn = pymysql.connect(host='172.30.30.2')
curs = conn.cursor()


# Creating database 'versions' in database container
curs.execute('CREATE DATABASE IF NOT EXISTS versions')
conn.close()

# Connecting again to the database 'versions'
conn = pymysql.connect(host='172.30.30.2', db="versions")
curs = conn.cursor()

# Creating table 'tbl_versions'
columns = ', '.join("`" + str(x).replace('/', '_') + "`" + " VARCHAR(255)" for x in index_list)
sql_create_table = "CREATE TABLE IF NOT EXISTS  %s ( %s ) ;" % ('tbl_versions', columns)
curs.execute(sql_create_table)
 
 
# Inserting values of the dictionary in the table  
for row in returned_list:
    sql_insert = insert(row)
    curs.execute(sql_insert)
    conn.commit() 
 

#print(returned_list)

#driver.close()

driver.quit()
