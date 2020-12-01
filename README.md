# Car Price Tracker
Tracking car prices can be rather tedious so this Python script automates that process

## Description
This script uses autotempest.com to gather the prices for a specified make and model in the United States in hopes of tracking prices over the a long-term period to reveal patterns in prices. Autotempest.com compiles listings from Cars.com, eBay.com, Carvana and many other webistes into one website. From there, this script extracts the car name (make and model), the year, odometer, price, location, and a link to the posting and saves the data in a .csv file.

In the near future, this script will analyze the data to show measures such as what's the average price for the car based on the year it was manufactured and the average price based on the odometer readings. Most importantly, I intend to graph each listing's data to show how much the prices are changing over the next year or so. 

## Setup
To install all required dependencies, enter the following command in the command-line:```pip install -r requirements.txt```
To run the file, there are two options:
1. ```python3 car_price.py```
  This will extract data for the default car (Lexus GSF in 60004)
1. ```python3 car_price.py <make> <model> <zip>```
  This will extract data for the specified car where every field beginning with < and ending with > is to be replaced with the respective field
