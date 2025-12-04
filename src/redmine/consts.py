"""定数定義、環境変数."""

import os
import sys
from typing import Final

from dotenv import load_dotenv

load_dotenv("/workspace/.env.local")

try:
    API_KEY: Final[str] = os.environ["API_KEY"]
    API_URL: Final[str] = os.environ["API_URL"]
except KeyError:
    print(
        "エラー: '/workspace/.env.local' を作成して環境変数 'API_KEY' と"
        " 'API_URL' を定義してください。\n"
        "  - API_KEY: Redmine の個人設定 ＞ APIアクセスキー\n"
        "  - API_URL: プロトコル://ホスト[:ポート]"
    )
    sys.exit(1)
