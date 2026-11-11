/* ============================================================
   施工事例のデータ

   ■ このファイルは自動で作られています。直接編集しないでください。
     次回の自動反映のときに、ここでの手直しは消えてしまいます。

   ■ 内容を直すところ：施工事例台帳（スプレッドシート）

   ■ 作り直しているもの：tools/施工事例台帳_生成.py
     （.github/workflows/news-from-sheet.yml が定期的に実行します）
     /works/ のカードも、続けて tools/施工事例一覧作成.py が作り直します。
   ============================================================ */

const CASE_ITEMS = [
  // ---- 1件目（台帳 2行目） ----
  {
    category: "キッチン改修（練習用の見本）",
    type:     "水回り",
    before: "lp_image_assets_png/cases/web/kitchen_before.jpg",
    after:  "lp_image_assets_png/cases/web/kitchen_after.jpg",
    spec:   { location: "キッチン", period: "5日間", cost: "約120万円〜（目安）", building: "戸建て" },
    detail: {
      problem: "古くなった水まわりを使いやすくしたい",
      work:    "収納力を高めた最新システムキッチンへ交換",
      change:  "作業スペースと収納が増え、毎日の料理が快適になりました。",
      comment: "限られたスペースでも使いやすくなるようプランを工夫しました。"
    },
    link: ""
  },
  // ---- 2件目（台帳 3行目） ----
  {
    category: "玄関ドア交換（練習用の見本）",
    type:     "内装・建具",
    before: "lp_image_assets_png/cases/web/entrance_door_before.jpg",
    after:  "lp_image_assets_png/cases/web/entrance_door_after.jpg",
    spec:   { location: "玄関", period: "1日間", cost: "約55万円〜（目安）", building: "戸建て" },
    detail: {
      problem: "カギがかかりにくく防犯面が心配",
      work:    "3重ロックのカギ付きで断熱性のある玄関ドアへ交換",
      change:  "開け閉めが軽くなり、玄関まわりの印象も明るくなりました。",
      comment: "玄関は家の顔とのご要望におこたえしました。"
    },
    link: ""
  }
];
