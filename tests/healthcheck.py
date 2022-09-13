import requests
 
 
x = requests.get('http://selenium-grid:4444/status')
 
 
print(x.status_code)

