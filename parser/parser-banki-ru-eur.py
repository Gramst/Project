from utils import get_html_seleniumm, get_exchangers_rates, get_banks_rates, save_csv 

URL_EUR = 'http://www.banki.ru/products/currency/cash/eur/moskva/#bank-rates'
FILDS_EUR = ['dep_name', 'bank_name', 'eur_buy', 'eur_sell', 'update_time']
FILE_EXCH_EUR = 'banki-ru-exchangers-eur.csv'
FILE_BANKS_EUR = 'banki-ru-banks-eur.csv'

def main():
    html = get_html_seleniumm (URL_EUR)

    if html:
        save_csv(get_exchangers_rates(html, FILDS_EUR, 'EUR'), FILE_EXCH_EUR, FILDS_EUR) #carrency need uppercase
        save_csv(get_banks_rates(html, FILDS_EUR[1:], 'eur'), FILE_BANKS_EUR, FILDS_EUR[1:]) #carrency need lowercase

if __name__ == '__main__':
    main()
