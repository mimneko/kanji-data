import csv
import json

# ファイルパスを指定
csv_file_path = '漢検漢字.csv'
json_file_path = 'output.json'

# データを格納するリストを初期化
data = []

# ファイルを開いて読み込み
with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
    reader = csv.reader(file)
    # ヘッダーを読み飛ばす
    next(reader)
    for row in reader:
        # 各行の最初の要素を取得
        kanji = row[1]
        # 残りの要素をpartsとして取得
        parts = row[2:]
        # 空の要素を削除
        parts = [element for element in parts if element]
        # 辞書として追加
        data.append({"kanji": kanji, "parts": parts})

# JSONファイルに書き込み
with open(json_file_path, mode='w', encoding='utf-8') as json_file:
    json.dump(data, json_file, ensure_ascii=False, indent=2)

# 結果を表示（確認用）
print(json.dumps(data, ensure_ascii=False, indent=2))
