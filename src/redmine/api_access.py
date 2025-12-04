"""API 呼び出し."""

from consts import API_KEY, API_URL
from libs.lib_api import RedmineApi

api = RedmineApi(key=API_KEY, url=API_URL)

# チケットの総数.
api.pprint(len(api.get_issues()))

# プロジェクトの総数.
api.pprint(len(api.get_projects()))
