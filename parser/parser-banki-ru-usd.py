from utils import get_html_seleniumm, get_exchangers_rates, get_banks_rates, save_csv 

URL_USD = 'http://www.banki.ru/products/currency/cash/usd/moskva/#bank-rates'
FILDS_USD = ['dep_name', 'bank_name', 'usd_buy', 'usd_sell', 'update_time']
FILE_EXCH_USD = 'banki-ru-exchangers-usd.csv'
FILE_BANKS_USD = 'banki-ru-banks-usd.csv'

def main():
    html = get_html_seleniumm (URL_USD)

    if html:
        save_csv(get_exchangers_rates(html, FILDS_USD, 'USD'), FILE_EXCH_USD, FILDS_USD) #carrency need uppercase
        save_csv(get_banks_rates(html, FILDS_USD[1:], 'usd'), FILE_BANKS_USD, FILDS_USD[1:]) #carrency need lowercase

if __name__ == '__main__':
    main()
