import requests
from bs4 import BeautifulSoup


vgm_url = 'https://minkabu.jp/financial_item_ranking/dividend_yield'
html_text = requests.get(vgm_url).text
soup = BeautifulSoup(html_text, 'html.parser')