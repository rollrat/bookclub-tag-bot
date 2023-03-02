

import json
from os import listdir
from os.path import isfile, join


onlyfiles = [f for f in listdir('result2') if isfile(join('result2', f))]
count = 0

for fn in onlyfiles:
    with open(join('result2', fn), 'r', encoding='UTF-8') as f:
        j = json.loads(f.read())

        if len(j['search']['items']) == 0 or "docs" not in j['info'] or len(j['info']['docs']) == 0:
            continue

        print(j['info']['docs'][0]['EA_ADD_CODE'][-3:], '\t',
              j['otitle'], '\t',
              j['search']['items'][0]['title'], '\t',
              j['search']['items'][0]['discount'], '\t',
              j['info']['docs'][0]['PAGE'], '\t',
              j['search']['items'][0]['isbn'], '\t',
              j['search']['items'][0]['publisher'], '\t',
              j['info']['docs'][0]['PUBLISHER']
              )
