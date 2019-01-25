from utils import get_banki_ru_rates 

import settings

def main():
    for currency in settings.CURR_LIST:
    	get_banki_ru_rates(currency)

if __name__ == '__main__':
    main()
