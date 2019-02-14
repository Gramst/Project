import csv

def get_dict():
    VLG_row = csv.DictReader(open("data/VLG.csv"), delimiter=";")
    VLG = {}
    n = 0
    for i in VLG_row:
        VLG[n] = {}
        VLG[n]['bank_name'] = i['bank_name']
        VLG[n]['usd_rur'] = i['usd_rur']
        VLG[n]['eur_rur'] = i['eur_rur']
        VLG[n]['rur_eur'] = i['rur_eur']
        VLG[n]['rur_usd'] = i['rur_usd']
        n += 1

    return VLG

def get_kurs(city_dict, city='VLG', para='usd_rur'):
    maxex = 0.
    maxci = {}
    flag = False
    n=0
    out_dict = {}
    while n<5:
        for i in city_dict:
            if float(city_dict[i][para]) > float(maxex):
                if city_dict[i]['bank_name'] in out_dict:
                    continue
                maxex =city_dict[i][para]
                flag = True
        if flag == True:
            flag2 = True
            for i in city_dict:
                if city_dict[i][para] == maxex:# and flag2:
                    out_dict[city_dict[i]['bank_name']] = city_dict[i][para] 
                    flag2 = False
            #out_dict[n] = maxci
        maxex = 0.
        flag = False
        n +=1

    return out_dict


d = get_dict()


