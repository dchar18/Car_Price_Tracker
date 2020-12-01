from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import re
import json
import requests
import sys

arguments = sys.argv

# - TODO --
# - add command line arguments to choose what call is being searched for
# - process data
#     - averages for the year
#     - graphs
# - do the work headless (don't open a browser window)

# r = requests.get('https://www.autotempest.com/results?make=lexus&model=gsf&zip=60004')
# data = r.json()
# print(json.dumps(data.popitem(), indent=2))

titles = []
years = []
prices = []
mileages = []
locations = []
links = []

make = ''
model = ''
zip = ''
trim = ''
# not enough arguments provided
if len(arguments) < 4:
    make = 'lexus'
    model = 'gsf'
    zip = '60004'
else:
    make = arguments[1].lower()
    model = arguments[2].lower()
    if len(arguments) == 4:
        zip = arguments[3]
    elif len(arguments) == 5:
        trim = arguments[3]
        zip = arguments[4]
    else:
        print(arguments)

driver = webdriver.Chrome('/usr/local/bin/chromedriver')
url = 'https://www.autotempest.com/results?make=' + make.lower() + '&model=' + model + '&zip=' + zip
# driver.get('https://www.autotempest.com/results?make=lexus&model=gsf&zip=60004')
driver.get(url)
sleep(5)

content = driver.page_source

# open the webpage
soup = BeautifulSoup(content, features="html.parser")
# wait for the webpage to load
sleep(5)
# pull the 'result-list-item' elements from the page
# 'result-list-item' is the common element among each posting in the page
results = soup.findAll('li', attrs={'class':'result-list-item'})

# regular  expression for finding the model year
regex = re.compile(r"[0-9]{4}")

print('Found ', len(results), ' entries...')
# iterate through the results to extract information
for item in results:
    description = item.find("span", class_="title-wrap")
    # extract the title
    title = description.find("a", class_="listing-link").text.strip()
    # extract the year
    match = re.search(regex, title)
    year = str(match.group(0))
    # add year and title to respective list
    years.append(year)
    titles.append(title.replace(year + ' ', ''))
    # extract the price, if it doesn't exists, enter 'N/A' as a placeholder
    try:
        prices.append(item.find("div", class_="price").text.strip())
    except:
        prices.append("N/A")
    # extract the mileage, if it doesn't exists, enter 'N/A' as a placeholder
    try:
        mileages.append(item.find("span", class_="info mileage").text)
    except:
        mileages.append("N/A")
    
    locations.append(item.find("span", class_="location-info-wrap").text.strip())
    links.append(item.find('a', href=True)['href'])

# display the extracted information
for k in range(0, len(results)):
    print(years[k], '\t', titles[k], '\t', prices[k], '\t', mileages[k], '\t', locations[k], '\t', links[k])
print("Num results: ", len(results))

# store the extracted information in a dataframe
df = pd.DataFrame({'Car':titles,'Year': years, 'Price':prices,'Mileage':mileages,'Location':locations,'URL':links}) 
csv_title = model + '_prices.csv'
df.to_csv(csv_title, index=False, encoding='utf-8')

driver.close()