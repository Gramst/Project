from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os
from selenium import webdriver

import settings

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
    rows_exchagers = soup.findAll('div', class_=settings.EXCH_DIV)
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
    rows_banks = soup.findAll('tr', class_=settings.BANKS_TR)
    banks_table = []

    for row in rows_banks:
        banks_table.append({
            'bank_name' : row.find('a', class_='font-bold').text,
            fields[1] : row.find('td', attrs={'data-currencies-code' : currency})['data-currencies-rate-buy'],
            fields[2] : row.findAll('td', attrs={'data-currencies-code' : currency})[1]['data-currencies-rate-sell'],
            'update_time' : row.find('span', class_='font-size-default').text
        })

    return banks_table

def save_csv(result_table, save_file, fields, csv_dir):
    os.makedirs(csv_dir, exist_ok = True)
    with open(os.path.join(csv_dir, save_file), "w", encoding="utf8", newline='') as csvf:
        writer = csv.DictWriter(csvf, fields, delimiter=';')
        writer.writeheader()
        for row in result_table:
            writer.writerow(row)

def get_banki_ru_rates(currency):
    url = 'http://www.banki.ru/products/currency/cash/{}/moskva/#bank-rates'.format(currency)
    fields = ['dep_name', 'bank_name', '{}_buy'.format(currency), '{}_sell'.format(currency), 'update_time']
    file_exchangers = 'banki-ru-exchangers-{}_{}.csv'.format(currency, datetime.now().strftime('%Y%m%d-%H%M%S'))
    file_banks = 'banki-ru-banks-{}_{}.csv'.format(currency, datetime.now().strftime('%Y%m%d-%H%M%S'))

    html = get_html_selenium (url)

    if html:
        #for exchangers currency need uppercase
        save_csv(get_exchangers_rates(html, fields, currency.upper()), file_exchangers, fields, settings.CSV_DIR)
        save_csv(get_banks_rates(html, fields[1:], currency), file_banks, fields[1:], settings.CSV_DIR)