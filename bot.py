import json
from time import sleep
from urllib import parse
import requests
import pandas as pd
from os import listdir
from os.path import isfile, join

df = pd.read_excel('data.xls')


def doNaverAPI():
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


def requestInfoFromISBN(isbn):
    with open('secret-lib.txt') as f:
        ClientSecret = f.read()

    return requests.get(
        'https://www.nl.go.kr/seoji/SearchApi.do?' +
        'cert_key=' + ClientSecret +
        '&result_style=json' +
        '&page_no=1' +
        '&page_size=10'
        '&isbn=' + isbn)


def testISBNAPI():
    print(requestInfoFromISBN('9791170431114').json())


def enumResult():
    onlyfiles = [f for f in listdir('result') if isfile(join('result', f))]
    count = 0

    for fn in onlyfiles:
        with open(join('result', fn), 'r', encoding='UTF-8') as f:
            j = json.loads(f.read())

            if len(j['search']['items']) == 0:
                continue

            isbn = j['search']['items'][0]['isbn']

            info = requestInfoFromISBN(isbn)

            with open('result2/' + isbn + '.txt', 'w', encoding='UTF-8') as f:
                f.write(json.dumps(
                    {'otitle': j['otitle'],
                     'oauthor': j['oauthor'],
                     'search': j['search'],
                     'info': info.json()}, ensure_ascii=False, indent=4))

        count += 1

        print(count)


enumResult()
