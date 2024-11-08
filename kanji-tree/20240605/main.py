from kanji_tree_utils import KanjiNode, save_kanji_tree, load_kanji_tree, print_tree

# 漢字のパーツ辞書の定義
parts_dict = {
    "日": KanjiNode("日"),
    "月": KanjiNode("月"),
    "皿": KanjiNode("皿"),
    "くさかんむり": KanjiNode("くさかんむり"),
    "木": KanjiNode("木")
}

# 木構造の定義
# 先に必要なパーツを定義
parts_dict["明"] = KanjiNode("明", [
    parts_dict["日"],
    parts_dict["月"]
])

# その後、他の漢字を定義
parts_dict.update({
    "林": KanjiNode("林", [
        parts_dict["木"],
        parts_dict["木"]
    ]),
    "萌": KanjiNode("萌", [
        parts_dict["明"],
        parts_dict["くさかんむり"]
    ]),
    "盟": KanjiNode("盟", [
        parts_dict["明"],
        parts_dict["皿"]
    ])
})

# 漢字の木構造をリストとしてまとめる
kanji_tree = [
    parts_dict["萌"],
    parts_dict["明"],
    parts_dict["盟"],
    parts_dict["林"]
]

# 漢字の木構造をJSONファイルに保存
save_kanji_tree(kanji_tree, "kanji_trees.json")

# JSONファイルから漢字の木構造を読み込み
new_kanji_tree = load_kanji_tree("kanji_trees.json")

# 読み込んだデータの確認
for tree in new_kanji_tree:
    print_tree(tree)
    print()
