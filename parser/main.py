import argparse

from utils import get_banki_ru_rates 

from settings import CURR_LIST  

def main():
    parser = argparse.ArgumentParser(description='Choice of currency for parsing')
    parser.add_argument('curr', nargs='?', default='all', help='Select the required currency')    
    args = parser.parse_args()

    if args.curr == 'usd':
        get_banki_ru_rates('usd')
#        print('USD')
    elif args.curr == 'eur':
        get_banki_ru_rates('eur')
#        print('EUR')
    elif args.curr == 'all':
#        print('ALL')
        for currency in CURR_LIST:
            get_banki_ru_rates(currency)
    else:
        print('Invalid argument entered')

if __name__ == '__main__':
    main()
