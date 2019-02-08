import csv
import os

from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver

from settings import BANKS_TR, CSV_DIR, EXCH_DIV, FIELDS

def get_html_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url)
    generated_html = driver.page_source
    driver.close()
    return generated_html

def get_usd_eur_rates(html, sity_ru):
    soup = BeautifulSoup(html, 'html.parser')
    rows_exchagers = soup.findAll('div', class_=EXCH_DIV)
    currency_table = []

    for row in rows_exchagers:
        currency_table.append({
            'dep_name' : row.find('a', class_='font-bold').text,
            'bank_name' : row.find('a', class_='font-size-default').text,
            'usd_rur' : row.find('div', attrs={'data-currencies-code' : 'USD'})['data-currencies-rate-buy'],
            'rur_usd' : row.findAll('div', attrs={'data-currencies-code' : 'USD'})[1]['data-currencies-rate-sell'],
            'eur_rur' : row.find('div', attrs={'data-currencies-code' : 'EUR'})['data-currencies-rate-buy'],
            'rur_eur' : row.findAll('div', attrs={'data-currencies-code' : 'EUR'})[1]['data-currencies-rate-sell'],
            'update_time' : row.find('div', class_='font-size-small color-gray-gray').text[:-1]
        })

    rows_banks = soup.findAll('tr', class_=BANKS_TR)

    for row in rows_banks:
        currency_table.append({
            'dep_name' : '{} - {}'.format(row.find('a', class_='font-bold').text, sity_ru),            
            'bank_name' : row.find('a', class_='font-bold').text,
            'usd_rur' : row.find('td', attrs={'data-currencies-code' : 'usd'})['data-currencies-rate-buy'],
            'rur_usd' : row.findAll('td', attrs={'data-currencies-code' : 'usd'})[1]['data-currencies-rate-sell'],
            'eur_rur' : row.find('td', attrs={'data-currencies-code' : 'eur'})['data-currencies-rate-buy'],
            'rur_eur' : row.findAll('td', attrs={'data-currencies-code' : 'eur'})[1]['data-currencies-rate-sell'],
            'update_time' : row.find('span', class_='font-size-default').text
        })

    return currency_table

def save_csv(result_table, save_file, fields, csv_dir):
    os.makedirs(csv_dir, exist_ok = True)
    with open(os.path.join(csv_dir, save_file), "w", encoding="utf8", newline='') as csvf:
        writer = csv.DictWriter(csvf, fields, delimiter=';')
        writer.writeheader()
        for row in result_table:
            writer.writerow(row)

def get_banki_ru_rates(sity, sity_ru):
    url = 'https://www.banki.ru/products/currency/cash/{}/#bank-rates'.format(sity)
    file_rates = 'banki-ru-rates-{}_{}.csv'.format(sity, datetime.now().strftime('%Y%m%d-%H%M%S'))

    html = get_html_selenium (url)

    if html:
        save_csv(get_usd_eur_rates(html, sity_ru), file_rates, FIELDS, CSV_DIR)
