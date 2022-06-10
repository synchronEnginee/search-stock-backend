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

# サニタイズする
@app.route('/<page_num>', methods=['GET'])
def get_fall_list(page_num):
    vgm_url = 'https://minkabu.jp/financial_item_ranking/fall?exchange=tokyo.prime&order=asc&page=' + str(page_num)
    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    # 一種類ごとに取得して辞書型の配列を作成
    stocks_name = [n.get_text() for n in soup.select('tbody tr td div.fwb')]
    stocks_code = [n.get_text() for n in soup.select('tbody tr td div.md_sub')]
    # (*)をトリム
    stocks_price = [re.sub(r'\(.*\)$', '', n.get_text()) for n in soup.select('tbody tr td div.wsnw')]
    # タブとスペースと改行除去
    stocks_fall = [re.sub('(\s|\r\n)', '', n.get_text()) for n in soup.select('tbody tr td.tar.cur.vamd')]
    stocks_target_price = [n.get_text() for n in soup.select('tbody tr td.num.vamd a > span')]
    stocks_info = []
    for name, code, price, fall, target in zip(stocks_name, stocks_code, stocks_price, stocks_fall, stocks_target_price[0::2]):
        stocks_info.append({"name": name, "code": code, "price": price, "stockFall": fall, "stockTargetPrice": target})

    return json.dumps(stocks_info, ensure_ascii=False, indent=2)

@app.route('/compare/<stock_code>', methods=['GET'])
def get_compare_list(stock_code):
    vgm_url = 'https://minkabu.jp/stock/' + str(stock_code) + '/chart'
    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    name = soup.select_one('p.md_stockBoard_stockName').text
    stock_info = [n.get_text() for n in soup.select('td.num')]
    per = float(re.sub('[^0-9\.]', '', stock_info[7]))
    pbr = float(re.sub('[^0-9\.]', '', stock_info[8]))
    dividendYield = float(re.sub('[^0-9\.]', '', stock_info[9]))
    dividendPayoutRatio = float(re.sub('[^0-9\.]', '', stock_info[10]))

    return json.dumps({"name": name, "per": per, "pbr": pbr, "dividendYield": dividendYield, "dividendPayoutRatio": dividendPayoutRatio},
     ensure_ascii=False, indent=2)

if __name__ == "__main__":
    app.run()