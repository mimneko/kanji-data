import json
import tkinter as tk
from tkinter import ttk, messagebox

class KanjiListGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("漢字リスト管理ツール")
        self.master.geometry("1280x720")

        self.kanji_list = []
        self.load_kanji_list()

        self.kanji_types = ["形声", "指事", "象形", "会意", "会意形声", "パーツ"]

        self.create_widgets()

    def load_kanji_list(self):
        try:
            with open("kanji-list.json", "r", encoding="utf-8") as f:
                self.kanji_list = json.load(f)
        except FileNotFoundError:
            messagebox.showwarning("ファイルが見つかりません", "kanji-list.jsonが見つかりません。空のリストで開始します。")

    def save_kanji_list(self):
        with open("kanji-list.json", "w", encoding="utf-8") as f:
            json.dump(self.kanji_list, f, ensure_ascii=False, indent=4)

    def create_widgets(self):
        # Main frame
        main_frame = ttk.PanedWindow(self.master, orient=tk.HORIZONTAL)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Left frame for Treeview
        left_frame = ttk.Frame(main_frame)
        main_frame.add(left_frame, weight=4)

        # Treeview
        self.tree = ttk.Treeview(left_frame, columns=("ID", "Label", "Type", "Components", "Alternative"))
        self.tree.heading("ID", text="ID")
        self.tree.heading("Label", text="漢字")
        self.tree.heading("Type", text="成り立ち")
        self.tree.heading("Components", text="構成要素")
        self.tree.heading("Alternative", text="異体字")
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("ID", width=50)
        self.tree.column("Label", width=50)
        self.tree.column("Type", width=100)
        self.tree.column("Components", width=200)
        self.tree.column("Alternative", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Right frame for Edit panel
        right_frame = ttk.Frame(main_frame)
        main_frame.add(right_frame, weight=2)

        # Edit panel
        edit_frame = ttk.LabelFrame(right_frame, text="漢字編集")
        edit_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(edit_frame, text="ID:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.id_entry = ttk.Entry(edit_frame)
        self.id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(edit_frame, text="漢字:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.label_entry = ttk.Entry(edit_frame)
        self.label_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(edit_frame, text="成り立ち:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.type_combobox = ttk.Combobox(edit_frame, values=self.kanji_types)
        self.type_combobox.grid(row=2, column=1, padx=5, pady=5)
        self.type_combobox.set("形声")

        ttk.Label(edit_frame, text="構成要素:").grid(row=3, column=0, sticky="ne", padx=5, pady=5)
        self.components_frame = ttk.Frame(edit_frame)
        self.components_frame.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.components_entries = []

        ttk.Label(edit_frame, text="異体字:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.alternative_entry = ttk.Entry(edit_frame)
        self.alternative_entry.grid(row=4, column=1, padx=5, pady=5)

        # Reference display
        ttk.Label(edit_frame, text="参考:").grid(row=5, column=0, sticky="ne", padx=5, pady=5)
        self.reference_text = tk.Text(edit_frame, height=3, width=30, wrap=tk.WORD)
        self.reference_text.grid(row=5, column=1, padx=5, pady=5)
        self.reference_text.config(state=tk.DISABLED)

        # Add button to add new component entry
        ttk.Button(edit_frame, text="構成要素を追加", command=self.add_component_entry).grid(row=6, column=0, columnspan=2, pady=5)

        # Buttons
        button_frame = ttk.Frame(edit_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="追加", command=self.add_kanji).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="更新", command=self.update_kanji).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="削除", command=self.delete_kanji).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="保存", command=self.save_changes).pack(side=tk.LEFT, padx=5)

        self.populate_tree()

        # Bind events for real-time reference updates
        self.id_entry.bind("<KeyRelease>", self.update_reference)
        self.label_entry.bind("<KeyRelease>", self.update_reference)

    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        for kanji in self.kanji_list:
            components = ", ".join(kanji.get("components", []))
            alternative = kanji.get("alternative", "")
            self.tree.insert("", tk.END, values=(kanji["id"], kanji["label"], kanji["type"], components, alternative))

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            kanji = next(k for k in self.kanji_list if k["id"] == item["values"][0])
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, kanji["id"])
            self.label_entry.delete(0, tk.END)
            self.label_entry.insert(0, kanji["label"])
            self.type_combobox.set(kanji["type"])
            
            # Clear existing components entries
            for entry in self.components_entries:
                entry.destroy()
            self.components_entries.clear()

            # Add new components entries
            components = kanji.get("components", [])
            for component in components:
                self.add_component_entry(component)

            self.alternative_entry.delete(0, tk.END)
            self.alternative_entry.insert(0, kanji.get("alternative", ""))

            self.update_reference()

    def add_component_entry(self, value=""):
        entry = ttk.Entry(self.components_frame, width=10)
        entry.insert(0, value)
        entry.pack(side=tk.LEFT, padx=2, pady=2)
        self.components_entries.append(entry)
        entry.bind("<KeyRelease>", self.update_reference)

    def update_reference(self, event=None):
        self.reference_text.config(state=tk.NORMAL)
        self.reference_text.delete(1.0, tk.END)
        
        components = [entry.get() for entry in self.components_entries if entry.get()]
        alternative = self.alternative_entry.get()
        
        reference_kanjis = []
        for kanji in self.kanji_list:
            if kanji["id"] in components or kanji["id"] == alternative:
                reference_kanjis.append(f"{kanji['id']}: {kanji['label']}")
        
        self.reference_text.insert(tk.END, ", ".join(reference_kanjis))
        self.reference_text.config(state=tk.DISABLED)

    def add_kanji(self):
        id_value = self.id_entry.get().strip()
        label_value = self.label_entry.get().strip()

        if not id_value or not label_value:
            messagebox.showwarning("入力エラー", "IDと漢字は必須です。")
            return

        if any(kanji["id"] == id_value for kanji in self.kanji_list):
            messagebox.showwarning("重複エラー", "同じIDの漢字が既に存在します。")
            return

        new_kanji = {
            "id": id_value,
            "label": label_value,
            "type": self.type_combobox.get()
        }
        components = [entry.get() for entry in self.components_entries if entry.get()]
        if components:
            new_kanji["components"] = components
        alternative = self.alternative_entry.get()
        if alternative:
            new_kanji["alternative"] = alternative
        
        self.kanji_list.append(new_kanji)
        self.populate_tree()
        self.tree.selection_set(self.tree.get_children()[-1])
        self.on_tree_select(None)

    def update_kanji(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("選択なし", "更新する漢字を選択してください。")
            return

        id_value = self.id_entry.get().strip()
        label_value = self.label_entry.get().strip()

        if not id_value or not label_value:
            messagebox.showwarning("入力エラー", "IDと漢字は必須です。")
            return

        item = self.tree.item(selected[0])
        index = next(i for i, k in enumerate(self.kanji_list) if k["id"] == item["values"][0])

        updated_kanji = {
            "id": id_value,
            "label": label_value,
            "type": self.type_combobox.get(),
        }

        components = [entry.get() for entry in self.components_entries if entry.get()]
        if components:
            updated_kanji["components"] = components

        alternative = self.alternative_entry.get()
        if alternative:
            updated_kanji["alternative"] = alternative

        self.kanji_list[index] = updated_kanji
        self.populate_tree()

    def delete_kanji(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("選択なし", "削除する漢字を選択してください。")
            return

        if messagebox.askyesno("削除の確認", "選択した漢字を削除してもよろしいですか？"):
            item = self.tree.item(selected[0])
            self.kanji_list = [k for k in self.kanji_list if k["id"] != item["values"][0]]
            self.populate_tree()

    def save_changes(self):
        self.save_kanji_list()
        messagebox.showinfo("保存完了", "変更がkanji-list.jsonに保存されました。")

if __name__ == "__main__":
    root = tk.Tk()
    app = KanjiListGUI(root)
    root.mainloop()