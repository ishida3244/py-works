"""作業時間クラス.
https://www.redmine.org/projects/redmine/wiki/Rest_TimeEntries
"""

import datetime
from typing import Final

from pydantic.dataclasses import dataclass

from .lib_api import RedmineApi


@dataclass
class TimeEntryProject:
    """作業時間のプロジェクト."""

    id: int
    name: str


@dataclass
class TimeEntryIssue:
    """作業時間のチケット."""

    id: int


@dataclass
class TimeEntryUser:
    """作業時間のユーザー."""

    id: int
    name: str


@dataclass
class Activity:
    """作業時間の作業分類."""

    id: int
    name: str


@dataclass
class Status:
    """作業時間のステータス."""

    id: int
    name: str
    is_closed: bool


@dataclass
class Priority:
    """作業時間の優先度."""

    id: int
    name: str


@dataclass
class TimeEntry:
    """GET /time_entries.json API の応答に含まれる個々の作業時間."""

    id: int
    project: TimeEntryProject
    user: TimeEntryUser
    activity: Activity
    hours: float
    comments: str
    spent_on: datetime.date
    created_on: datetime.datetime
    updated_on: datetime.datetime
    # レスポンスに issue が存在しない場合があるのでオプションフィールドにする.
    issue: TimeEntryIssue | None = None


@dataclass
class TimeEntriesResponse:
    """GET /time_entries.json API の応答を格納するクラス."""

    time_entries: list[TimeEntry]
    total_count: int
    offset: int
    limit: int


class TimeEntriesApi(RedmineApi):
    """Redmine Time Entries API クラス."""

    def get(self, params: dict | None = None, limit_total: int = 0) -> list[TimeEntry]:
        """API GET Time Entries を実行して TimeEntry データクラスのリストを取得する.

        Args:
            params (dict | None, optional): API のパラメータ (省略可).
                limit と offset は指定しても無視される.
            limit_total (int, optional): 最大取得件数. 0 以下で無制限. 省略時は 0.

        Raises:
            requests.HTTPError: HTTP 200 以外のステータスコード.
            requests.RequestException: リクエスト関連エラーの基底クラス.

        Returns:
            list[TimeEntry]: TimeEntry データクラスのリスト.
        """
        # デフォルトパラメータに指定パラメータをマージ (キー重複時は指定パラメータを優先).
        _params: dict = {"sort": "id"}
        _params |= params if params is not None else {}

        url: Final[str] = f"{self.url}/time_entries.json"
        total_items: list[TimeEntry] = []

        for response in self._get_generator(url, _params, limit_total):
            total_items.extend(TimeEntriesResponse(**response).time_entries)

        return total_items

    def lookup(self, entry_id: int, params: dict | None = None) -> TimeEntry | None:
        """API GET Time Entries を実行して、指定された ID の TimeEntry データクラスを取得する.

        Args:
            entry_id (int): 取得するアイテムの ID.
            params (dict | None, optional): API のパラメータ (省略可).

        Raises:
            requests.HTTPError: HTTP 200 と 404 以外のステータスコード.
            requests.RequestException: リクエスト関連エラーの基底クラス.

        Returns:
            TimeEntry | None: TimeEntry データクラス. 見つからない場合は None を返す.
        """
        url: Final[str] = f"{self.url}/time_entries/{entry_id}.json"
        response: dict = self._get(url, params)

        return TimeEntry(**response["time_entry"]) if response else None
