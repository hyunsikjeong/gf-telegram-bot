import json

# TODO: merge all the files into one file
equip_dict = json.load(open('dict/equip_dict.json', 'r', encoding='utf8'))
doll_dict = json.load(open('dict/doll_dict.json', 'r', encoding='utf8'))
alias_dict = json.load(open('dict/alias_dict.json', 'r', encoding='utf8'))

def find_by_alias(alias):
    if alias in alias_dict:
        return alias_dict[alias]
    return None

def get_doll_by_time(time):
    doll_list = []
    # TODO: Improve time complexity by using dictionary
    for num in doll_dict:
        dict_time = int(doll_dict[num]['time'].replace(':',''))
        if dict_time == time:
            doll_list.append(doll_dict[num])
    
    return doll_list

def get_equip_by_time(time):
    if time not in equip_dict:
        return None
    return equip_dict[time]

def get_doll_by_num(num):
    if num not in doll_dict:
        return None
    doll = doll_dict[num]
    return doll