import requests
import re
from bs4 import BeautifulSoup


vgm_url = 'https://minkabu.jp/financial_item_ranking/dividend_yield'
html_text = requests.get(vgm_url).text
soup = BeautifulSoup(html_text, 'html.parser')

stock_names = [n.get_text() for n in soup.select('tbody tr td div.fwb')]
stock_price = [re.sub(r'\(.*\)$', '', n.get_text()) for n in soup.select('tbody tr td div.wsnw')]
print(stock_names)
print(stock_price)