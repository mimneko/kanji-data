## 常用漢字表_音訓・用例付き
文化庁[^1]でまとめられている常用漢字表[^2]のファイル

常用漢字全2136字

## 常用漢字一覧_部首・漢検級情報
常用漢字表の簡易版。識別番号は文化庁の「常用漢字表の字体・字形に関する指針（報告）について」[^6]による。

部首名は漢検漢字辞典[^3]により、部首は見返しの部首配列順の見出しの形に近いものを選んだ。また、部首IDは漢字ペディアで用いられているものである。また、下記漢検級も記載。

## 子の名に使える漢字[^4]
常用漢字 + 人名用漢字(常用漢字の異体字を含む) = 2999字(2769字種2999字体)

識別番号は独自に付けたもので、意味はない。

戸籍法施行規則（昭和二十二年司法省令第九十四号）別表第二（第六十条、第六十八条の二関係）[^5]による。

## 漢検配当漢字一覧
### 漢検配当漢字一覧_リスト形式(10級-2級)
配当級は「日本漢字能力検定 級別漢字表（１０級～２級）」（２０２０年２月発表、公益財団法人 日本漢字能力検定協会発行）による。

識別番号は人名漢字とリンクしており、同様に独自に付けたもので、意味はない。

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

### 漢検配当漢字一覧_等級別(10級-1級抜けあり)
配当級は漢検漢字辞典[^3]による。
漢字検定の配当漢字には、文字コードの充てられていない文字も存在するため、それらは記述していない。また、手作業でのチェックのため抜けがあることも注意されたし。

## 新旧字体対照表
AsahiNet[^7]による。

文献によって新字体・旧字体の定義が異なり、これより少ないとしているもの、多いとしているものの両方が見られる。本リポジトリでは、最終的に「旧字体のようなもの」を網羅することを目指す。

---

## CSV / JSON ダウンロード一覧

以下は、このリポジトリ内に存在する  
`.csv` および `.json` ファイルの自動生成リンクです。

- 個別ダウンロード用リンク
- 一括取得は GitHub の ZIP を利用

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

[^1]: https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/kanji/joyokanjisakuin/index.html
[^2]: https://www.bunka.go.jp/kokugo_nihongo/sisaku/joho/joho/kijun/naikaku/pdf/joyokanjihyo_20101130.pdf
[^3]: 公益財団法人 日本漢字能力検定協会．『漢検漢字辞典』第二版．2014，1984p．
[^4]: https://www.moj.go.jp/MINJI/minji86.html
[^5]: https://elaws.e-gov.go.jp/document?lawid=322M40000010094
[^6]: https://www.bunka.go.jp/koho_hodo_oshirase/hodohappyo/pdf/2016022902.pdf
[^7]: https://www.asahi-net.or.jp/~ax2s-kmtn/ref/old_chara.html

