from utils import get_banki_ru_rates 

from settings import CURR_LIST  

def main():
    for currency in CURR_LIST:
    	get_banki_ru_rates(currency)

if __name__ == '__main__':
    main()
