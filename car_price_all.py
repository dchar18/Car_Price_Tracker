from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import re
import json
import requests
import sys
import datetime

cars = [
    ('lexus', 'gsf', '60004'),
    ('lexus', 'rcf', '60004'),
    ('lexus', 'lc500', '60004'),
    ('lexus', 'gs350', '60004', 'F Sport'),
    ('lexus', 'is350', '60004', 'F Sport'),
    ('mazda', 'mazdaspeed3', '60004'),
    ('tesla', 'model3', '60004'),
    # ('toyota', 'rav4', '60004'),
    ('lexus', 'ls500', '60004', 'F Sport')
]
date = datetime.datetime.now().strftime('%x')

for car in cars:
    titles = []
    years = []
    prices = []
    mileages = []
    locations = []
    links = []

    make = car[0]
    model = car[1].replace(' ', '')
    zip = car[2]

    # tuple has (make, model, zip)
    if len(car) == 3:
        print(make, ' ', model)
        url = 'https://www.autotempest.com/results?make=' + \
            make.lower() + '&model=' + model.lower() + '&zip=' + zip
    # tuple has (make, model, zip, trim)
    else:
        trim = car[3].replace(' ', '+')
        print(make, ' ', model, ' ', trim)
        url = 'https://www.autotempest.com/results?make=' + \
            make.lower() + '&model=' + model.lower() + '&trim_kw=' + trim + '&zip=' + zip

    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    print("Searching: " + url)
    driver.get(url)
    sleep(5)

    content = driver.page_source

    # open the webpage
    soup = BeautifulSoup(content, features="html.parser")
    # wait for the webpage to load
    sleep(5)
    # pull the 'result-list-item' elements from the page
    # 'result-list-item' is the common element among each posting in the page
    results = soup.findAll('li', attrs={'class': 'result-list-item'})

    # regular expression for finding the model year
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

        locations.append(
            item.find("span", class_="location-info-wrap").text.strip())
        links.append(item.find('a', href=True)['href'])

    dates = [date]*len(results)

    # display the extracted information
    # for k in range(0, len(results)):
    # print(dates[k], '\t', years[k], '\t', titles[k], '\t', prices[k], '\t', mileages[k], '\t', locations[k], '\t', links[k])
    print("Num results: ", len(results))

    # store the extracted information in a dataframe
    df = pd.DataFrame({'Date': dates, 'Car': titles, 'Year': years, 'Price': prices,
                       'Mileage': mileages, 'Location': locations, 'URL': links})
    csv_title = model + '_prices.csv'
    df.to_csv(csv_title, mode='a', encoding='utf-8', index=False)

    driver.close()
