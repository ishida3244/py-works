"""チケットクラス.
https://www.redmine.org/projects/redmine/wiki/Rest_Issues
"""

import datetime
from typing import Final

from pydantic.dataclasses import dataclass

from .lib_api import RedmineApi


@dataclass
class IssueProject:
    """チケットのプロジェクト."""

    id: int
    name: str


@dataclass
class IssueTracker:
    """チケットのトラッカー."""

    id: int
    name: str


@dataclass
class Status:
    """チケットのステータス."""

    id: int
    name: str
    is_closed: bool


@dataclass
class Priority:
    """チケットの優先度."""

    id: int
    name: str


@dataclass
class IssueUser:
    """チケットの起票、履歴更新ユーザー."""

    id: int
    name: str


@dataclass
class IssueJournalDetail:
    """チケットの履歴の詳細."""

    name: str
    property: str
    new_value: str | None
    old_value: str | None


@dataclass
class IssueJournal:
    """チケットの履歴."""

    id: int
    user: IssueUser
    details: list[IssueJournalDetail]
    notes: str
    created_on: datetime.datetime
    updated_on: datetime.datetime
    private_notes: bool


@dataclass
class IssueChild:
    """子チケット."""

    id: int
    subject: str
    tracker: IssueTracker


@dataclass
class IssueAttachment:
    """チケットの添付ファイル."""

    id: int
    author: IssueUser
    content_type: str
    content_url: str
    created_on: datetime.datetime
    description: str
    filename: str
    filesize: int
    thumbnail_url: str | None = None


@dataclass
class IssueRelation:
    """チケットの関連チケット."""

    id: int
    issue_id: int
    issue_to_id: int
    relation_type: str
    delay: int | None


@dataclass
class Issue:
    """GET /issues.json API の応答に含まれる個々のチケット."""

    id: int
    project: IssueProject
    tracker: IssueTracker
    status: Status
    priority: Priority
    author: IssueUser
    subject: str
    description: str
    start_date: datetime.date | None
    due_date: datetime.date | None
    done_ratio: int
    is_private: bool
    estimated_hours: float | None
    total_estimated_hours: float | None
    spent_hours: float
    created_on: datetime.datetime
    updated_on: datetime.datetime | None
    closed_on: datetime.datetime | None
    # 以下は include を指定した場合のみ取得できるオプションフィールド.
    children: list[IssueChild] | None = None
    attachments: list[IssueAttachment] | None = None
    relations: list[IssueRelation] | None = None
    changesets: list | None = None
    journals: list[IssueJournal] | None = None
    watchers: list[IssueUser] | None = None
    allowed_statuses: list[Status] | None = None


@dataclass
class IssuesResponse:
    """GET /issues.json API の応答を格納するクラス."""

    issues: list[Issue]
    total_count: int
    offset: int
    limit: int


class IssuesApi(RedmineApi):
    """Redmine Issues API クラス."""

    def get(self, params: dict | None = None, limit_total: int = 0) -> list[Issue]:
        """API GET Issues を実行して Issue データクラスのリストを取得する.

        Args:
            params (dict | None, optional): API のパラメータ (省略可).
                limit と offset は指定しても無視される.
            limit_total (int, optional): 最大取得件数. 0 以下で無制限. 省略時は 0.

        Raises:
            requests.HTTPError: HTTP 200 以外のステータスコード.
            requests.RequestException: リクエスト関連エラーの基底クラス.

        Returns:
            list[Issue]: Issue データクラスのリスト.
        """
        # デフォルトパラメータに指定パラメータをマージ (キー重複時は指定パラメータを優先).
        _params: dict = {"sort": "project,id"}
        _params |= params if params is not None else {}

        url: Final[str] = f"{self.url}/issues.json"
        total_items: list[Issue] = []

        for response in self._get_generator(url, _params, limit_total):
            total_items.extend(IssuesResponse(**response).issues)

        return total_items

    def lookup(self, issue_id: int, params: dict | None = None) -> Issue | None:
        """API GET Issues を実行して、指定された ID の Issue データクラスを取得する.

        Args:
            issue_id (int): 取得するアイテムの ID.
            params (dict | None, optional): API のパラメータ (省略可).

        Raises:
            requests.HTTPError: HTTP 200 と 404 以外のステータスコード.
            requests.RequestException: リクエスト関連エラーの基底クラス.

        Returns:
            Issue | None: Issue データクラス. 見つからない場合は None を返す.
        """
        url: Final[str] = f"{self.url}/issues/{issue_id}.json"
        response: dict = self._get(url, params)

        return Issue(**response["issue"]) if response else None
