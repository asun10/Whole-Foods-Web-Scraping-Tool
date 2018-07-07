#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 16:10:07 2018

@author: asun
"""


import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Setup the Google Sheets API
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/asun/Documents/Python/WholeFoods.json', scope)
client = gspread.authorize(credentials)

import urllib2
from bs4 import BeautifulSoup
from urllib2 import urlopen

# Beautiful Soup scraping for Whole Foods website
page = urllib2.urlopen('https://www.wholefoodsmarket.com/sales-flyer/lincolnpark')
soup = BeautifulSoup(page)

brand = [el.get_text() for el in soup.find_all('div', attrs={"class": 'views-field views-field-field-flyer-brand-name'})]
product_name = [el.get_text() for el in soup.find_all('div', attrs={"class": 'views-field views-field-field-flyer-product-name'})]
price = [el.get_text() for el in soup.find_all('div', attrs={"class": 'sale_line'})]
regular_price = [div.string for div in soup.findAll("div", "reg_line")]
valid_range = [el.get_text() for el in soup.find_all('div', attrs={"class": 'views-field views-field-field-flyer-end-date'})]

brand_list = []
product_name_list = []
price_list = []
regular_price_list= []
valid_range_list = []

sale_list = [brand_list, product_name_list, price_list, regular_price_list, valid_range_list]

#connect to worksheets
wks = client.open("GroceryList").worksheet("WholeFoodsSale")

print 'Connected to Your GroceryList Googlesheet'

i = 0

while i < len(brand):
    brand_list = brand[i]
    product_name_list = product_name[i]
    price_list = price[i]
    regular_price_list = regular_price[i]
    valid_range_list = valid_range[i]
    sale_list = [brand_list, product_name_list, price_list, regular_price_list, valid_range_list]
    index = i+2
    wks.insert_row(sale_list, index)
    i = i+1

print 'Done'
