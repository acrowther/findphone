import base64
import sys 
import os
import datetime
import json
import requests
import scrapy
import urllib.parse
from utils import *

def findphone(name):
  print(f'searching {name}')
  qname=urllib.parse.quote_plus(name)
  response=requests.get(f'https://www.google.com/search?hl=fr&ie=UTF-8&oe=UTF-8&q={qname}+t%C3%A9l%C3%A9phone')
  if response.ok:
    print('response ok')
    sel=scrapy.Selector(response)
    phone=sel.xpath('//div[contains(text(),"+")]/text()').re_first('\+\d\d \d \d\d \d\d \d\d \d\d')
    if phone is None:
      print('phone not found')
      return None
    else:
      print('phone found')
      return {'name':name,'phone':phone}
  else:
    print(f'response ko for {name}')
    return None

def process(data, context):
    name=parse_parameters(data)
    result=findphone(name)
    if result!=None:
      sendtobq(result,'us','phone')