from settings import SITIES_RU
from utils import get_banki_ru_rates 


def main():
    for count in SITIES_RU:
        get_banki_ru_rates(count['name_translit'], count['city_name'])

if __name__ == '__main__':
    main()
