from flask import Flask, g, request
import requests
import re
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route('/stock', methods=['GET'])
def get_stock():
    vgm_url = 'https://minkabu.jp/financial_item_ranking/dividend_yield'
    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    stock_names = [n.get_text() for n in soup.select('tbody tr td div.fwb')]
    stock_price = [re.sub(r'\(.*\)$', '', n.get_text()) for n in soup.select('tbody tr td div.wsnw')]
    print(stock_names)
    print(stock_price)

    return json.dumps(stock_price)

if __name__ == "__main__":
    app.run()