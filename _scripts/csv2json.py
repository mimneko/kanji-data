import os
import csv
import json

def convert_all_csv_in_directory():
    """
    プロジェクトの_data/csv/ディレクトリ内のすべてのCSVファイルを
    _data/json/ディレクトリにJSONとして変換します。
    '識別番号'列が存在する場合、その値を整数に変換します。
    """
    try:
        # スクリプトの絶対パスからプロジェクトのルートディレクトリを特定します
        # 例: /path/to/project/_scripts/convert_csv.py -> /path/to/project
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        project_root = os.path.dirname(script_dir)

        # 入力と出力のディレクトリパスを構築します
        csv_dir = os.path.join(project_root, '_data', 'csv')
        json_dir = os.path.join(project_root, '_data', 'json')

        # 出力ディレクトリが存在しない場合は作成します
        os.makedirs(json_dir, exist_ok=True)

        # CSVディレクトリが存在するか確認します
        if not os.path.isdir(csv_dir):
            print(f"エラー: 入力ディレクトリが見つかりません: {csv_dir}")
            return

        # CSVディレクトリ内の.csvで終わるファイル名のリストを取得します
        csv_files = [f for f in os.listdir(csv_dir) if f.lower().endswith('.csv')]

        if not csv_files:
            print(f"情報: {csv_dir} 内に変換対象のCSVファイルが見つかりません。")
            return

        print("CSVからJSONへの変換を開始します...")

        # 各CSVファイルをループ処理します
        for csv_filename in csv_files:
            csv_filepath = os.path.join(csv_dir, csv_filename)

            # 出力するJSONファイルの名前を決定します (例: words.csv -> words.json)
            json_filename = os.path.splitext(csv_filename)[0] + '.json'
            json_filepath = os.path.join(json_dir, json_filename)

            print(f"  変換中: {csv_filename} -> {json_filename}")

            data = []
            try:
                # CSVファイルをBOM付きUTF-8として読み込みます
                with open(csv_filepath, mode='r', encoding='utf-8-sig', newline='') as csv_file:
                    # 各行を辞書として読み込みます
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        # '識別番号'列が存在する場合、その値を整数に変換します
                        if '識別番号' in row and row['識別番号']:
                            try:
                                row['識別番号'] = int(row['識別番号'])
                            except (ValueError, TypeError):
                                # 変換に失敗した場合は警告を表示し、値は文字列のままにします
                                print(f"    警告: ファイル '{csv_filename}' の行で '識別番号' ({row['識別番号']}) を整数に変換できませんでした。")
                                pass
                        data.append(row)

                # JSONファイルにインデント付きで書き込みます
                with open(json_filepath, mode='w', encoding='utf-8') as json_file:
                    # indent=4: 4スペースでインデント
                    # ensure_ascii=False: 日本語などの非ASCII文字をそのまま出力
                    json.dump(data, json_file, indent=4, ensure_ascii=False)

            except Exception as e:
                print(f"    エラー: {csv_filename} の処理中にエラーが発生しました。詳細: {e}")
                # エラーが発生しても次のファイルの処理を続行します
                continue

        print("\n変換処理が完了しました。")

    except Exception as e:
        print(f"スクリプトの実行中に予期せぬエラーが発生しました: {e}")


if __name__ == "__main__":
    # スクリプトが直接実行された場合に関数を呼び出します
    convert_all_csv_in_directory()
