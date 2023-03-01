import json
from time import sleep
from urllib import parse
import requests
import pandas as pd


df = pd.read_excel('data.xls')

with open('secret-id.txt') as f:
    ClientId = f.read()

with open('secret-key.txt') as f:
    ClientSecret = f.read()

count = 0

for row in df.iterrows():
    title = row[1][0]
    author = row[1][1]

    try:
        encodedTitle = parse.quote(title)
    except:
        print(title)

    res = requests.get(
        'https://openapi.naver.com/v1/search/book.json?query=' +
        encodedTitle + '&display=10&start=1',
        headers={'X-Naver-Client-Id': ClientId,
                 'X-Naver-Client-Secret': ClientSecret}
    )

    with open('result/' + str(count) + '.txt', 'w', encoding='UTF-8') as f:
        f.write(json.dumps(
            {'otitle': title,
             'oauthor': author,
             'search': res.json()}, ensure_ascii=False, indent=4))

    count += 1

    print(count)

    sleep(0.05)
