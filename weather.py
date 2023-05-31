import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
from datetime import datetime, timedelta

# 初期日付設定
date_start = datetime(2015, 1, 1)

# データフレーム初期化
df = pd.DataFrame()

request_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
}

for _ in tqdm(range(37)): # 10日間ごとにデータを取得（2015年は36回）
    date_end = date_start + timedelta(days=9)  # 10日後
    url = f"http://www.meteomanz.com/sy8?l=1&cou=2090&ind=00000&d1={date_end.day:02d}&m1={date_end.month:02d}&y1={date_end.year}"

    # HTMLページ取得
    response = requests.get(url, headers=request_headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # テーブルデータ取得
    table = soup.find('table', {'class': 'data'})
    table_headers = [header.text for header in table.find_all('th')]
    rows = table.find_all('tr')
    data = []
    for row in rows[1:]:
        cols = row.find_all('td')
        cols = [col.text for col in cols]
        data.append(cols)

    # テーブルデータ取得
    table = soup.find('table', {'class': 'data'})
    table_headers = [header.text for header in table.find_all('th')]
    rows = table.find_all('tr')
    data = []
    for row in rows[1:]:
        cols = row.find_all('td')
        cols = [col.text.strip() for col in cols]  # 値から前後の空白を削除
        data.append(cols)

    # データフレームにデータ追加
    df_temp = pd.DataFrame(data, columns=table_headers)
    df_temp.set_index(table_headers[0], inplace=True)  # 最初の列名をインデックスとする。あなたのデータの場合、この列名を適切なものに変更してください。

    # データフレームの列を逆順にする
    df_temp = df_temp[df_temp.columns[::-1]]

    if df is None:  # 最初のループでは df は None なので、df_temp をそのまま df に代入
        df = df_temp
    else:
        df = pd.concat([df, df_temp], axis=1, join='outer')  # 同じインデックスの行をマッチング

    # 次の期間の開始日更新
    date_start = date_end + timedelta(days=1)

# CSVファイルに保存
df.to_csv('weather_data.csv')
