import csv
import json

def read_kanji_from_csv(filename):
    kanji_list = []
    with open(filename, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            kanji = row.get('漢字')
            if kanji:
                kanji_list.append(kanji)
    return kanji_list

def create_kanji_json(kanji_list, output_filename):
    kanji_data = [{"value": kanji, "parts": []} for kanji in kanji_list]
    with open(output_filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(kanji_data, jsonfile, ensure_ascii=False, indent=4)

def main():
    input_csv = '人名漢字.csv'
    output_json = 'kanji_data.json'
    kanji_list = read_kanji_from_csv(input_csv)
    create_kanji_json(kanji_list, output_json)

if __name__ == "__main__":
    main()
