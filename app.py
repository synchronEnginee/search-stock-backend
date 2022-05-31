from flask import Flask, g, request
from flask_cors import CORS
import requests
import re
from bs4 import BeautifulSoup
import json

app = Flask(__name__)
CORS(
    app,
    supports_credentials=True
)

@app.route('/stock', methods=['GET'])
def get_stock():
    vgm_url = 'https://minkabu.jp/financial_item_ranking/per?exchange=tokyo.prime&order=asc&page=6'
    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    # 一種類ごとに取得して辞書型の配列を作成
    stocks_name = [n.get_text() for n in soup.select('tbody tr td div.fwb')]
    stocks_code = [n.get_text() for n in soup.select('tbody tr td div.md_sub')]
    stocks_price = [re.sub(r'\(.*\)$', '', n.get_text()) for n in soup.select('tbody tr td div.wsnw')]
    stocks_per = [re.sub('(\s|\r\n)', '', n.get_text()) for n in soup.select('tbody tr td.tar.cur.vamd')]
    stocks_info = []
    for name, code, price, per in zip(stocks_name, stocks_code, stocks_price, stocks_per):
        stocks_info.append({"name": name, "code": code, "price": price, "per": per})

    return json.dumps(stocks_info, ensure_ascii=False, indent=2)

@app.route('/', methods=['GET'])
def get_fall_list():
    vgm_url = 'https://minkabu.jp/financial_item_ranking/fall?exchange=tokyo.prime&order=asc'
    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    # 一種類ごとに取得して辞書型の配列を作成
    stocks_name = [n.get_text() for n in soup.select('tbody tr td div.fwb')]
    stocks_code = [n.get_text() for n in soup.select('tbody tr td div.md_sub')]
    stocks_price = [re.sub(r'\(.*\)$', '', n.get_text()) for n in soup.select('tbody tr td div.wsnw')]
    stocks_fall = [re.sub('(\s|\r\n)', '', n.get_text()) for n in soup.select('tbody tr td.tar.cur.vamd')]
    stocks_target_price = [n.get_text() for n in soup.select('tbody tr td.num.vamd a > span')]
    stocks_info = []
    for name, code, price, fall, target in zip(stocks_name, stocks_code, stocks_price, stocks_fall, stocks_target_price):
        stocks_info.append({"name": name, "code": code, "price": price, "stockFall": fall, "stockTargetPrice": target})

    return json.dumps(stocks_info, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    app.run()