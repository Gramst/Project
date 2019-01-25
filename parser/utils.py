import csv
#import requests
from bs4 import BeautifulSoup
import os
from selenium import webdriver

def get_html_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    generated_html = driver.page_source
    driver.close()
    return generated_html

def get_exchangers_rates(html, fields, currency):
    soup = BeautifulSoup(html, 'html.parser')
    rows_exchagers = soup.findAll('div', class_='table-flex__row item calculator-hover-icon__container')
    exchangers_table = []

    for row in rows_exchagers:
        exchangers_table.append({
            'dep_name' : row.find('a', class_='font-bold').text,
            'bank_name' : row.find('a', class_='font-size-default').text,
            fields[2] : row.find('div', attrs={'data-currencies-code' : currency})['data-currencies-rate-buy'],
            fields[3] : row.findAll('div', attrs={'data-currencies-code' : currency})[1]['data-currencies-rate-sell'],
            'update_time' : row.find('div', class_='font-size-small color-gray-gray').text[:-1]
        })

    return exchangers_table

def get_banks_rates(html, fields, currency):
    soup = BeautifulSoup(html, 'html.parser')
    rows_banks = soup.findAll('tr', class_='calculator-hover-icon__container exchange-calculator-rates ')
    banks_table = []

    for row in rows_banks:
        banks_table.append({
            'bank_name' : row.find('a', class_='font-bold').text,
            fields[1] : row.find('td', attrs={'data-currencies-code' : currency})['data-currencies-rate-buy'],
            fields[2] : row.findAll('td', attrs={'data-currencies-code' : currency})[1]['data-currencies-rate-sell'],
            'update_time' : row.find('span', class_='font-size-default').text
        })

    return banks_table

def save_csv(result_table, save_file, fields):
    csv_dir = 'csv_files'
    os.makedirs(csv_dir, exist_ok = True)
    with open(os.path.join(csv_dir, save_file), "w", encoding="utf8", newline='') as csvf:
        writer = csv.DictWriter(csvf, fields, delimiter=';')
        writer.writeheader()
        for row in result_table:
            writer.writerow(row)
