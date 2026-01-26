# kanji-data

日本語・漢字に関する各種データを整理し、再利用しやすい形で保管することを目的としたデータ集である。
主に、漢字検定1級の学習への利用を想定している。

## データ一覧

### JIS漢字.csv

日本産業規格（JIS）の JIS X 0213 に基づく、漢字10050字を収録した CSV データ。

- 漢字
- JIS 面区点コード
- ユニコード
- JIS 第何水準か

JIS水準と面区点コードのおおまかな対応は以下のとおりである。

- JIS 第1水準：1面 16～46区、47区の一部
- JIS 第2水準：1面 48～83区、84区の一部
- JIS 第3水準：1面 14～15区、47区の一部、84区の一部、85～94区
- JIS 第4水準：2面

### 常用漢字表.json

文化庁が発表した常用漢字表[^1][^2]をもとに構成した、常用漢字2136字種およびその異体字を収録した JSON データ。

- 漢字
- 音読み・訓読み
- 用例
- 備考（異なる表記、慣用読み、対義語・類義語表記など）

> [!CAUTION]
> まだ十分に構造化できていない。

### 漢検漢字辞典漢字.csv

『漢検漢字辞典』[^3]および漢字ペディア[^4]の情報を整理した CSV データ。

- 漢字（テキストまたは画像）
- 親字・旧字・その他の別
- 漢検級
- 漢検漢字辞典での掲載ページ
- 漢字ペディアへのリンク
- 字種・字体の識別番号
- 補足情報、注記、編集記録

各漢検級における対象漢字数[^5]は以下のとおりである。

- 10級：80字
- 9級：240字
- 8級：440字
- 7級：642字
- 6級：835字
- 5級：1026字
- 4級：1339字
- 3級：1623字
- 準2級：1951字
- 2級：2136字
- 準1級：約3000字
- 1級：約6000字

本データでは、各漢字を以下の漢検級に分類している。

- 10級：80字
- 9級：160字
- 8級：200字
- 7級：202字
- 6級：193字
- 5級：191字
- 4級：313字
- 3級：284字
- 準2級：328字
- 2級：185字
- 準1級：857字
- 1/準1級：644字
- 1級：2676字
- 配当外：473字

### 部首.csv

漢字の部首を整理した CSV データ。
本データでは、『漢検漢字辞典』[^3]に基づく部首分類を採用している。

- 部首
- 名称
- 画数
- ユニコード
- 漢検漢字辞典での掲載順

> [!NOTE]
> 康熙字典の部首も214種類であるが、漢検漢字辞典では「⼡（U+2F21）」と「⼢（U+2F22）」を統合し、さらに「⺍（U+2E8D）」を追加しているため、内訳は一致しない。

### 子の名に使える漢字.csv

子の名に使用可能な漢字[^6]2999字（2769字種・2999字体）を整理した CSV データ。

- 漢字
- 常用漢字の通用字体か、常用漢字外の字か、常用漢字の異体字か

> [!NOTE]
> 戸籍法施行規則（昭和二十二年司法省令第九十四号）別表第二（第六十条、第六十八条の二関係）[^7]

## 今後の追加予定

- 各字種・字体に対して、全データ間で共通となる一意の識別番号を付与する。

## ダウンロードリンク

以下は、本リポジトリ内に存在するファイルへのリンクである。
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
[^6]: https://www.moj.go.jp/MINJI/minji86.html
[^7]: https://elaws.e-gov.go.jp/document?lawid=322M40000010094
[^5]: https://www.kanken.or.jp/kanken/grades/overview/
[^4]: https://www.kanjipedia.jp/