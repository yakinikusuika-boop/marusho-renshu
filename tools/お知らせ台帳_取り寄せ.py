# -*- coding: utf-8 -*-
"""
お知らせ台帳（Googleスプレッドシートの公開CSV）を1ファイルに取り寄せるスクリプト。

  使い方（URLは環境変数から受け取る。引数には書かない）:
      NEWS_SHEET_CSV_URL="https://docs.google.com/.../pub?output=csv" \
        python tools/お知らせ台帳_取り寄せ.py --out work/ledger_raw.csv

  なぜ curl ではなくこれを使うのか
    curl は URL に改行やタブが混ざっていると取得できない。
    GitHub の Secret は貼り付けのときに末尾の改行が入りやすく、実際にそれで失敗した
    （2026-11-11）。Python の urllib は URL から改行・タブを自動で取り除くため、
    同じ値でも成功する。ここでは加えて自分でも前後の空白と改行・タブを落としている。

  安全のための決めごと
    ・取得できなかった／中身が空だったときは終了コード 1。出力ファイルは作らない。
      → 呼び出し側（ワークフロー）はここで止まるので、news.js は書き換わらない。
    ・エラー文には URL を一切出さない。台帳のURLはログに残さない。

  標準ライブラリだけで動く。
"""

import argparse
import os
import re
import sys
import time
import urllib.error
import urllib.request

ENV_NAME = "NEWS_SHEET_CSV_URL"
USER_AGENT = "marusho-news-builder"
TIMEOUT_SECONDS = 60
ATTEMPTS = 3
RETRY_WAIT_SECONDS = 5


def die(message):
    """URLを出さずに失敗を知らせて終わる。"""
    sys.stderr.write("::error::%s\n" % message)
    sys.exit(1)


def clean_url(raw):
    """前後の空白と、途中に混ざった改行・タブを取り除く。"""
    return re.sub(r"[\r\n\t]", "", (raw or "").strip())


def fetch(url):
    """台帳のCSVを取ってくる。失敗したら数秒おいて繰り返す。"""
    last_error = ""
    for attempt in range(1, ATTEMPTS + 1):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
                return response.read()
        except urllib.error.HTTPError as error:
            # 404・401 などは繰り返しても直らないので、その場で諦める
            last_error = "HTTP %s %s" % (error.code, error.reason)
            if error.code < 500:
                break
        except Exception as error:  # 通信の失敗・時間切れなど
            last_error = type(error).__name__
        if attempt < ATTEMPTS:
            sys.stderr.write(
                "::warning::台帳の取り寄せに失敗しました（%s）。%d秒おいて%d回目を試します。\n"
                % (last_error, RETRY_WAIT_SECONDS, attempt + 1)
            )
            time.sleep(RETRY_WAIT_SECONDS)
    die("台帳を取り寄せられませんでした（%s）。news.js は書き換えていません。" % last_error)


def main():
    parser = argparse.ArgumentParser(
        description="お知らせ台帳の公開CSVを取り寄せてファイルに保存する"
    )
    parser.add_argument("--out", required=True, help="保存先（例: work/ledger_raw.csv）")
    args = parser.parse_args()

    url = clean_url(os.environ.get(ENV_NAME))
    if not url:
        die(
            "%s が未設定です。リポジトリの Secrets に台帳のCSV URLを登録してください。"
            % ENV_NAME
        )
    if not re.match(r"^https://", url, re.I):
        die(
            "%s が https:// で始まっていません。台帳のCSV URLを登録し直してください。"
            % ENV_NAME
        )

    raw = fetch(url)
    if not raw.strip():
        die("台帳が空でした。news.js は書き換えていません。")

    folder = os.path.dirname(os.path.abspath(args.out))
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(args.out, "wb") as handle:
        handle.write(raw)

    print("台帳を取り寄せました（%d バイト）" % len(raw))


if __name__ == "__main__":
    main()
