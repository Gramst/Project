import requests
import json
import logging

# https://geocode-maps.yandex.ru/1.x
# https://geocode-maps.yandex.ru/1.x/?apikey=<Ваш API-ключ>&format=json&geocode=Тверская+6
# https://geocode-maps.yandex.ru/1.x/?apikey=<Ваш API-ключ>&geocode=Ивановка&ll=37.618920,55.756994&spn=3.552069,2.400552
# https://geocode-maps.yandex.ru/1.x/?apikey=<Ваш API-ключ>&geocode=37.611347,55.760241
# {'longitude': 44.5458, 'latitude': 48.512331}


api_log = logging.getLogger('Yandex api')

class YandexApi:

    def __init__(self, api_key, path):

        self.base_geocode_url = 'https://geocode-maps.yandex.ru/1.x/?apikey={0}&format=json'.format(api_key)
        self.base_search_url = ' https://search-maps.yandex.ru/v1/?apikey={0}&lang=ru_RU'.format(api_key)
        self.path = path


    def _get_raw_data_geokode(self, longitude, latitude):
        url = self.base_geocode_url + '&geocode={0},{1}'.format(longitude, latitude)
        raw_data = requests.get(url)
        return raw_data.json()


    def _dump_json(self, json_data, name_file):
        with open(self.path + '\{0}dump.json'.format(name_file), "w") as f:
            json.dump(json_data, f, indent=2)


    def _get_geo_adress_from_raw(self, raw_data):

        f_result = True
        try:
            part_row_adress = raw_data['response']['GeoObjectCollection']\
                                ['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']
        except KeyError as error:
            f_result = False
            return f_result, error
        except TypeError as error:
            f_result = False
            return f_result, error

        return f_result, part_row_adress
                        

    def get_location(self, longitude, latitude):

        raw_data = self._get_raw_data_geokode(longitude, latitude)
        self._dump_json(raw_data, f'geo_lo{longitude}la{latitude}')
        f_result, adress = self._get_geo_adress_from_raw(raw_data)
        result = adress #TODO обработать флаг результата

        return result


    def _get_raw_data_search(self, longitude, latitude, requested_atm):
        
        url = self.base_search_url + '&text={0}&ll={1},{2}&results=5&spn=0.552069,0.400552&type=biz&lang=ru_RU'\
                .format( requested_atm, longitude, latitude)
        raw_data = requests.get(url).json()
        return raw_data
        
    def _get_search_adress_from_raw(self, raw_data):
        atms = []
        for company in raw_data['features']:
            try:
                atm = {}
                atm['name'] = company['properties']['name']
                api_log.info('atm_data')
                api_log.info(atm['name'])
                atm['geo'] = company['geometry']['coordinates']
                api_log.info(atm['geo'])
                atm['time'] = company['properties']['CompanyMetaData']['Hours']['text']
                api_log.info(atm['time'])
                atm['address'] = company['properties']['CompanyMetaData']['address']
                api_log.info(atm['address'])
                atms.append(atm)
            except KeyError:
                continue
        text = ''
        n = 1
        for atm in atms:
            text +=str(n) + ')' + atm['name'] + '\n' + '***\n' + atm['address'] + '\n'  + atm['time'] + '\n\n'
            n+=1
        return True, text, atms


    def search_atm(self, longitude, latitude, requested_atm):

        raw_data = self._get_raw_data_search(longitude, latitude, requested_atm)
        self._dump_json(raw_data, f'search_lo{longitude}la{latitude}')
        f_result, text,  d_of_adress = self._get_search_adress_from_raw(raw_data)
        result = text #TODO обработать флаг результата

        return result, d_of_adress

    def get_url_static_map(self, lng, lat, t_lng, t_lat):
        #url = 'https://static-maps.yandex.ru/1.x/?ll={0},{1}&l=map&pt={2},{3},pma~{0},{1},flag'\
        #    .format(lng, lat, t_lng, t_lat)
        lng_mid = (float(lng) + float(t_lng))/2
        lat_mid = (float(lat) + float(t_lat))/2
        url = 'https://static-maps.yandex.ru/1.x/?ll={4},{5}&l=map&pt={2},{3},pma~{0},{1},ya_ru'\
            .format(lng, lat, t_lng, t_lat, lng_mid, lat_mid)

        return url
