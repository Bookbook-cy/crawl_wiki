import requests
import json
import time
import pandas as pd
from bs4 import BeautifulSoup
response = requests.get('https://www.mhlw.go.jp/seisakunitsuite/seisakuhyouka/')
response.encoding = response.apparent_encoding

soup = BeautifulSoup(response.text, 'html.parser')
print(soup.title.string)