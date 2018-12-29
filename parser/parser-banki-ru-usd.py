import csv
import requests
from bs4 import BeautifulSoup

URL = 'http://www.banki.ru/products/currency/cash/usd/moskva/'

def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False

def get_exchange_rates(html):
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.findAll('div', class_='table-flex__row item calculator-hover-icon__container')
    exchange_table = []

    for row in rows:
        exchange_table.append({
            'dep_name' : row.find('a', class_='font-bold').text,
            'bank_name' : row.find('a', class_='font-size-default').text,
            'usd_buy' : row.find('div', attrs={'data-currencies-code' : 'USD'})['data-currencies-rate-buy'],
            'usd_sell' : row.findAll('div', attrs={'data-currencies-code' : 'USD'})[1]['data-currencies-rate-sell'],
            'update_time' : row.find('div', class_='font-size-small color-gray-gray').text[:-1]
        })

    return exchange_table

def save_csv(exchange_table):
    with open("banki-ru-usd.csv", "w", encoding="utf8", newline='') as csvf:
        fields = ['dep_name', 'bank_name', 'usd_buy', 'usd_sell', 'update_time']
        writer = csv.DictWriter(csvf, fields, delimiter=';')
        writer.writeheader()
        for row in exchange_table:
            writer.writerow(row)


def main():
    html = get_html(URL)

    if html:
        save_csv(get_exchange_rates(html))

if __name__ == '__main__':
    main()
