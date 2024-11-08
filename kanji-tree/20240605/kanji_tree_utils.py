import json

class KanjiNode:
    def __init__(self, value, parts=None):
        self.value = value
        self.parts = parts if parts is not None else []

def kanji_to_dict(node):
    if not node:
        return None
    return {
        "value": node.value,
        "parts": [kanji_to_dict(part) for part in node.parts]
    }

def dict_to_kanji(data):
    if not data:
        return None
    return KanjiNode(
        value=data["value"],
        parts=[dict_to_kanji(part) for part in data["parts"]]
    )

def save_kanji_tree(kanji_tree, filename):
    with open(filename, "w", encoding='utf-8') as f:
        json.dump([kanji_to_dict(tree) for tree in kanji_tree], f, indent=4, ensure_ascii=False)

def load_kanji_tree(filename):
    with open(filename, "r", encoding='utf-8') as f:
        data = json.load(f)
    return [dict_to_kanji(tree) for tree in data]

def print_tree(node, indent=0):
    if node:
        print(" " * indent + node.value)
        for part in node.parts:
            print_tree(part, indent + 4)
