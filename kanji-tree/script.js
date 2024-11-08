// CytLayoutモジュール: グラフのレイアウトを設定する機能を提供
var CytLayout = (function () {
    // 指定されたレイアウトをCytoscapeインスタンスに適用する関数
    var _setLayout = function (cy, layoutName) {
        var layout = {
            name: layoutName,
            fit: true,           // グラフを表示領域に合わせる
            animate: true,       // レイアウト変更時のアニメーションを有効化
            animationDuration: 500  // アニメーションの持続時間（ミリ秒）
        };
        cy.layout(layout).run();  // レイアウトを適用して実行
        return layout;
    };
    // 公開APIを返す
    return {
        setLayout: _setLayout
    };
})();

// DOMの読み込みが完了したら実行
document.addEventListener("DOMContentLoaded", function () {
    // ノードの種類に応じた色を定義
    var nodeColors = {
        '象形': '#3498db',
        '指事': '#e74c3c',
        '会意': '#2ecc71',
        '形声': '#f39c12',
        '会意形声': '#9b59b6',
        'パーツ': '#000000'
    };

    // ノードとエッジのスタイルを設定する関数
    var setStyles = function (nodes, edges) {
        // ノードのスタイル設定
        nodes.forEach(function (node) {
            var nodeColor = nodeColors[node.data('type')] || '#ffffff';
            var borderColor = node.data('type') ? '#ffffff' : '#dddddd';
            node.css({
                "width": 80,                  // ノードの幅
                "height": 80,                 // ノードの高さ
                "content": node.data('label') || ' ',  // ノードのラベル
                "text-valign": "center",      // テキストの垂直位置
                "text-halign": "center",      // テキストの水平位置
                "background-color": nodeColor,  // 背景色
                "color": "#ffffff",           // テキストの色
                "font-size": "24px",          // フォントサイズ
                "font-weight": "bold",        // フォントの太さ
                "border-width": "2px",        // ボーダーの幅
                "border-color": borderColor,  // ボーダーの色
                "transition-property": "background-color, border-color",  // トランジション対象のプロパティ
                "transition-duration": "0.3s"  // トランジションの持続時間
            });
        });
        // エッジのスタイル設定
        edges.forEach(function (edge) {
            edge.css({
                "curve-style": "bezier",       // エッジの曲線スタイル
                "target-arrow-shape": "triangle",  // ターゲット側の矢印の形
                "line-color": "#95a5a6",       // ラインの色
                "target-arrow-color": "#95a5a6",  // 矢印の色
                "width": 3,                    // エッジの幅
                "opacity": 0.7                 // 不透明度
            });
        });
    };

    // JSONファイルからノードデータを取得する関数
    function fetchNodes() {
        return fetch('kanji-list.json') // JSONファイルのパスを指定
            .then(response => response.json())
            .catch(error => console.error('Error fetching nodes:', error));
    }

    // 親ノードを追加し、検証する関数
    function addAndValidateParents(nodes) {
        const nodeMap = new Map(nodes.map(node => [node.id, node]));
        const existingNodeIds = new Set(nodeMap.keys());

        nodes.forEach(node => {
            // 代替文字がある場合、親ノードを設定
            if (node.alternative && nodeMap.has(node.alternative)) {
                const parentValue = "g_" + node.alternative;
                node.parent = parentValue;
                nodeMap.get(node.alternative).parent = parentValue;
            }

            // 親ノードが存在しない場合、新しく追加
            if (node.parent && !existingNodeIds.has(node.parent)) {
                nodes.push({ id: node.parent });
                existingNodeIds.add(node.parent);
            }
        });
    }

    // エッジを動的に生成する関数
    var generateEdges = function(nodes) {
        var edges = [];
        nodes.forEach(function(node) {
            if (node.components) {
                node.components.forEach(function(targetId) {
                    edges.push({
                        data: {
                            id: node.id + '-' + targetId,
                            source: targetId,
                            target: node.id
                        }
                    });
                });
            }
        });
        return edges;
    };

    // JSONデータを取得してCytoscapeを初期化する関数
    function initializeCytoscape() {
        fetchNodes().then(nodes => {
            addAndValidateParents(nodes);

            var edges = generateEdges(nodes);

            // Cytoscapeインスタンスの作成
            var cy = cytoscape({
                container: $("#IdCytoscape"),  // Cytoscapeを表示するコンテナ要素
                elements: {
                    nodes: nodes.map(node => { return { data: node }; }),
                    edges: edges
                },
                style: [
                    {
                        selector: '[color]',
                        style: {
                            'background-color': 'data(color)',
                            'label': 'data(label)'
                        }
                    },
                    {
                        selector: '[label]',
                        style: {
                            'label': 'data(label)'
                        }
                    },
                    {
                        selector: 'node',
                        style: {
                            'background-color': '#666',
                            'label': ''
                        }
                    },
                    {
                        selector: 'edge',
                        style: {
                            'width': 3,
                            'line-color': '#ccc',
                            'target-arrow-color': '#ccc',
                            'target-arrow-shape': 'triangle',
                            'curve-style': 'bezier'
                        }
                    }
                ]
            });

            // ノードとエッジのスタイルを設定
            setStyles(cy.nodes(), cy.edges());

            // パンズーム機能の設定
            cy.panzoom({
                zoomFactor: 0.05,            // ズーム倍率
                zoomDelay: 45,               // ズーム遅延
                minZoom: 0.1,                // 最小ズーム倍率
                maxZoom: 10,                 // 最大ズーム倍率
                fitPadding: 50,              // フィット時のパディング
                panSpeed: 10,                // パンスピード
                panDistance: 10,             // パン距離
                panDragAreaSize: 75,         // パンドラッグエリアサイズ
                panMinPercentSpeed: 0.25,    // パン最小速度（パーセント）
                panInactiveArea: 8,          // パン非アクティブエリア
                panIndicatorMinOpacity: 0.5, // パンインジケータ最小不透明度
                zoomOnly: false,             // ズームのみ有効化
                fitSelector: undefined,      // フィット対象セレクタ
                animateOnFit: function () {  // フィット時のアニメーション
                    return false;
                },
                fitAnimationDuration: 1000   // フィットアニメーション時間
            });

            // 初期レイアウトの設定
            CytLayout.setLayout(cy, "fcose");

            // レイアウト変更イベントの設定
            $("#IdLayout").change(function () {
                CytLayout.setLayout(cy, $("#IdLayout").val());
            });

            // レイアウトコンテナのイベント伝播を停止
            $('#IdLayoutContainer').on('mousedown mouseup click', function(e) {
                e.stopPropagation();
            });

            // 検索ボタンのクリックイベント
            $("#IdSearchButton").on('mousedown', function(e) {
                if (e.which === 1) {  // 左クリックの場合のみ
                    e.preventDefault();  // デフォルトの動作を防止
                    focusNode(cy);
                }
            });

            // 検索入力欄のEnterキーイベント
            $("#IdSearch").keypress(function(e) {
                if (e.which == 13) {  // Enterキーが押されたとき
                    e.preventDefault();  // デフォルトの動作を防止
                    focusNode(cy);
                }
            });

            // 検索コンテナのイベント伝播を停止
            $('#IdSearchContainer').on('mousedown mouseup click dblclick', function(e) {
                e.stopPropagation();
            });

            // 検索されたノードにフォーカスする関数
            function focusNode(cy) {
                var searchTerm = $("#IdSearch").val();
                var foundNode = cy.nodes().filter(function(ele){
                    return ele.data('label') === searchTerm;
                });

                if (foundNode.length > 0) {
                    cy.animate({
                        center: {
                            eles: foundNode
                        },
                        zoom: 1,  // ズームレベル
                        duration: 1000  // アニメーション時間（ミリ秒）
                    });
                } else {
                    alert("該当する漢字が見つかりませんでした。");
                }
            }

            // レイアウト選択のイベント伝播を停止
            $('#IdLayoutContainer').on('mousedown mouseup click dblclick', function(e) {
                e.stopPropagation();
            });
        });
    }

    // Cytoscapeの初期化を実行
    initializeCytoscape();
});