import csv


def get_dict():
    VLG_row = csv.DictReader(open("data/VLG.csv"), delimiter=";")
    #city_dict = {}
    #city_dict['VLG'] = VLG
    #print( city_dict )
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

    print(VLG)
    return VLG

def get_kurs(city_dict, city='VLG', para='usd_rur'):
    #print( city_dict[0][para])
    maxex = 0.
    maxci = {}
    flag = False
    n=0
    out_dict = {}
    while n<5:
        for i in city_dict:
            print(city_dict[i][para])
            if float(city_dict[i][para]) > float(maxex):
                print('gogo')
                if city_dict[i]['bank_name'] in out_dict:
                    print('cont')
                    continue
                maxex =city_dict[i][para]
                print(city_dict[i]['bank_name'])
                flag = True
                print(flag)
        if flag == True:
            print('adding')
            flag2 = True
            print(maxex)
            for i in city_dict:
                if city_dict[i][para] == maxex:# and flag2:
                    print('gg')
                    out_dict[city_dict[i]['bank_name']] = city_dict[i][para] 
                    flag2 = False
            #out_dict[n] = maxci
        maxex = 0.
        flag = False
        print(n , out_dict)
        n +=1

    return out_dict


d = get_dict()

print(get_kurs(d))

