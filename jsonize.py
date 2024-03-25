import requests
from bs4 import BeautifulSoup
import json
import re

# HTMLを取得
url = "https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/kanji/joyokanjisakuin/index.html"
response = requests.get(url)
response.encoding = "Shift_JIS"  # 文字エンコーディングをShift_JISに指定
html_content = response.text

# Beautiful Soupを使用してHTMLを解析
soup = BeautifulSoup(html_content, "html.parser")

# テーブルを取得
table = soup.find("table", {"id": "urlist"})

# テーブルのヘッダーを取得
header_cells = table.find("tr").find_all("th")
header = [cell.get_text(strip=True) for cell in header_cells]

# テーブルのデータを取得
data = []
for row in table.find_all("tr")[1:]:  # ヘッダーを除外する
    cells = row.find_all(["td", "th"])  # th要素も含める
    row_data = {}
    for i, cell in enumerate(cells):
        if cell.find("font"):  # font要素があればそのテキストを取得して配列にする
            font_texts = [re.sub(r"[\（\）\(\)]", "", font.get_text(strip=True)) for font in cell.find_all("font")]
            row_data[header[i]] = font_texts
        else:  # font要素以外の要素では<br/>で区切られたテキストを配列として取得する
            text_list = [text.strip().split("，") for text in cell.strings if text.strip()]
            row_data[header[i]] = text_list
    data.append(row_data)

# JSONに変換
json_data = json.dumps(data, ensure_ascii=False, indent=4)

# JSONをファイルに書き出す
with open("output.json", "w", encoding="utf-8") as json_file:
    json_file.write(json_data)

print("JSONデータが output.json に書き出されました。")
