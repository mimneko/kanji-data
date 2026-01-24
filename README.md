# kanji-data

日本語・漢字に関する各種データを整理し、再利用しやすい形で保管することを目的としたデータ集

## 収録ファイル一覧

### 常用漢字表.json

文化庁発表の常用漢字表[^1][^2]をもとに構成した JSON データ。未だ綺麗に構造化できていない
- 漢字 2136 字種、異体字
- 音読み・訓読み
- 用例
- 備考（異表記、慣用読み、対義・類義表記など）

### JIS漢字.csv

日本産業企画（JIS）の JIS X 0213 漢字一覧の 1, 2 面の CSV データ
- 漢字 
- JISコード体系に基づく漢字情報

### 漢検漢字辞典漢字.csv

漢検漢字辞典[^3]のデータを整理した CSV データ
- 漢検基準に基づく漢字情報

- 10級: 80字
- 9級: 160字 + 10級まで = 240字
- 8級: 200字 + 9級まで = 440字
- 7級: 202字 + 8級まで = 642字
- 6級: 193字 + 7級まで = 835字
- 5級: 191字 + 6級まで = 1026字
- 4級: 313字 + 5級まで = 1339字
- 3級: 284字 + 4級まで = 1623字
- 準2級: 328字 + 3級まで = 1951字
- 2級: 185字 + 準2級まで = 2136字

### 子の名に使える漢字.csv

子の名に使える漢字[^4]に関する CSV データ
- 戸籍・命名において使用可能な漢字
- 常用漢字 + 人名用漢字(常用漢字の異体字を含む) = 2999字(2769字種2999字体)

> 参考：戸籍法施行規則（昭和二十二年司法省令第九十四号）別表第二（第六十条、第六十八条の二関係）[^5]

### 部首.csv

漢字の部首情報を整理した CSV データ
- 部首名
- 対応する漢字

## ダウンロードリンク

以下は、このリポジトリ内に存在する  
<div id="download-meta">
  <a id="repo-zip" href="#" target="_blank" rel="noopener">
    リポジトリを ZIP でダウンロード
  </a>
</div>

<div id="download-status">取得中です。</div>
<ul id="download-list"></ul>

<script>
(() => {
  // ===== 設定 =====
  const OWNER = "mimneko";   // GitHub ユーザ名
  const REPO  = "kanji-data";   // リポジトリ名
  const REF   = "main";        // ブランチ or タグ
  const START_PATH = "";       // "data" などに限定可

  const apiUrl = (path) => {
    const p = path ? "/" + path : "";
    return `https://api.github.com/repos/${OWNER}/${REPO}/contents${p}?ref=${REF}`;
  };

  const rawUrl = (path) =>
    `https://raw.githubusercontent.com/${OWNER}/${REPO}/${REF}/${path}`;

  document.getElementById("repo-zip").href =
    `https://github.com/${OWNER}/${REPO}/archive/refs/heads/${REF}.zip`;

  const listEl = document.getElementById("download-list");
  const statusEl = document.getElementById("download-status");

  const isTarget = (name) =>
    name.endsWith(".csv") || name.endsWith(".json");

  async function fetchJSON(url) {
    const r = await fetch(url);
    if (!r.ok) throw new Error(r.statusText);
    return r.json();
  }

  async function walk(path, acc) {
    const items = await fetchJSON(apiUrl(path));
    if (!Array.isArray(items)) return;

    for (const item of items) {
      if (item.type === "file" && isTarget(item.name)) {
        acc.push(item.path);
      }
      if (item.type === "dir") {
        await walk(item.path, acc);
      }
    }
  }

  (async () => {
    try {
      const files = [];
      await walk(START_PATH, files);

      files.sort().forEach(p => {
        const li = document.createElement("li");
        const a  = document.createElement("a");
        a.href = rawUrl(p);
        a.textContent = p;
        a.setAttribute("download", "");
        li.appendChild(a);
        listEl.appendChild(li);
      });

      statusEl.textContent = `件数: ${files.length}`;
    } catch (e) {
      statusEl.textContent = "取得に失敗しました。";
    }
  })();
})();
</script>

---

[^1]: https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/kanji/joyokanjisakuin/index.html
[^2]: https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/pdf/joyokanjihyo_20101130.pdf
[^3]: 公益財団法人 日本漢字能力検定協会．『漢検漢字辞典』第二版．2014，1984p．
[^4]: https://www.moj.go.jp/MINJI/minji86.html
[^5]: https://elaws.e-gov.go.jp/document?lawid=322M40000010094