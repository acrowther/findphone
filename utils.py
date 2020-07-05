import base64
import sys 
import os
from google.cloud import bigquery
import datetime
import json
import requests 

def validate_message(message, param):
    var = message.get(param)
    if not var:
        raise ValueError('{} is not provided. Make sure you have \
                          property {} in the request'.format(param, param))
    return var

def parse_parameters(data):
    if data.get('data'):
        message_data = base64.b64decode(data['data']).decode('utf-8')
        message = json.loads(message_data)
    else:
        raise ValueError('Data sector is missing in the Pub/Sub message.')

    name = validate_message(message, 'name')
    return name

def sendtobq(result,dataset_id,table_id):
    print('inserting')
    client = bigquery.Client()
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)  # API request
    rows_to_insert = [result]
    errors = client.insert_rows(table, rows_to_insert)  # API request
    assert errors == []
    print('inserted')

def isvalid(url,toavoid):
  for site in toavoid:
    if site in str(url):
      return False
  return True

def findweb(name,site=None,toavoid=[]):
    headers = {
    'authority': 'api.qwant.com',
    'origin': 'https://www.qwant.com',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'dnt': '1',
    'content-type': 'application/x-www-form-urlencoded',
    'accept': '*/*',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'referer': 'https://www.qwant.com/',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',}
    
    if site==None:
      q = name
    else:
      q = f'site:{site} {name}'
    params = (
    ('count', '10'),
    ('q', q),
    ('t', 'web'),
    ('device', 'desktop'),
    ('extensionDisabled', 'true'),
    ('safesearch', '1'),
    ('locale', 'fr_FR'),
    ('uiv', '4'),
    )
    response = requests.get('https://api.qwant.com/api/search/web', headers=headers, params=params)

    print(response.content)    
    data = response.json()
    for content in data['data']['result']['items']:
        if isvalid(content['url'],toavoid):
            return {'url':content['url'],'desc':content['desc']}
    return None
