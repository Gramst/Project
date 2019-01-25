from datetime import datetime
from utils import get_html_selenium, get_exchangers_rates, get_banks_rates, save_csv 

URL_USD = 'http://www.banki.ru/products/currency/cash/usd/moskva/#bank-rates'
FILDS_USD = ['dep_name', 'bank_name', 'usd_buy', 'usd_sell', 'update_time']
FILE_EXCH_USD = 'banki-ru-exchangers-usd_{}.csv'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))
FILE_BANKS_USD = 'banki-ru-banks-usd_{}.csv'.format(datetime.now().strftime('%Y%m%d-%H%M%S'))

def main():
    html = get_html_selenium (URL_USD)

    if html:
        save_csv(get_exchangers_rates(html, FILDS_USD, 'USD'), FILE_EXCH_USD, FILDS_USD) #currency need uppercase
        save_csv(get_banks_rates(html, FILDS_USD[1:], 'usd'), FILE_BANKS_USD, FILDS_USD[1:]) #currency need lowercase

if __name__ == '__main__':
    main()
