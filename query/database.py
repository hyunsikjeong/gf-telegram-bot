import json

# TODO: merge all the files into one file
doll_dict = json.load(open('dict/doll_dict.json', 'r', encoding='utf8'))
equip_dict = json.load(open('dict/equip_dict.json', 'r', encoding='utf8'))
search_dict = json.load(open('dict/search_dict.json', 'r', encoding='utf8'))
buff_dict = json.load(open('dict/buff_dict.json', 'r', encoding='utf8'))
stat_dict = json.load(open('dict/stat_dict.json', 'r', encoding='utf8'))
skill_dict = json.load(open('dict/skill_dict.json', 'r', encoding='utf8'))
alias_dict = json.load(open('dict/alias_dict.json', 'r', encoding='utf8'))
upgrade_dict = json.load(open('dict/upgrade_dict.json', 'r', encoding='utf8'))

def find_by_alias(alias):
    if alias in alias_dict:
        return alias_dict[alias]
    return None

def get_doll_by_time(time):
    if time not in doll_dict:
        return None
    return doll_dict[time]

def get_equip_by_time(time):
    if time not in equip_dict:
        return None
    return equip_dict[time]

def get_doll_by_num(num):
    # Must exist
    doll = search_dict[num]
    doll['buff'] = buff_dict[num]
    doll['skill'] = skill_dict[num]
    doll['stats'] = stat_dict[num]
    if num in upgrade_dict:
        doll['upgrade'] = upgrade_dict[num]
    
    return doll