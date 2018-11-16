import os
import json

for file in os.listdir():
    if file.endswith('.json'):
        print(file)
        data = json.load(open(file, 'r', encoding='utf8'))

        if file == 'doll_dict.json':
            for num in data:
                for idx in range(len(data[num]['alias'])):
                    data[num]['alias'][idx] = data[num]['alias'][idx].lower()
                data[num]['alias'] = sorted(data[num]['alias'])
        json.dump(
            data,
            open(file, 'w', encoding='utf8'),
            ensure_ascii=False,
            indent=4,
            sort_keys=True)
