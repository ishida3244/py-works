"""プロジェクトクラス.
https://www.redmine.org/projects/redmine/wiki/Rest_Projects
"""

import datetime
from typing import Final

from pydantic.dataclasses import dataclass

from .lib_api import RedmineApi


@dataclass
class ProjectTracker:
    """プロジェクトのトラッカー."""

    id: int
    name: str


@dataclass
class IssueCategory:
    """チケットのカテゴリ."""

    id: int
    name: str


@dataclass
class ProjectModule:
    """プロジェクトのモジュール."""

    id: int
    name: str


@dataclass
class ProjectTimeEntryActivity:
    """プロジェクトの時間管理"""

    id: int
    name: str


@dataclass
class Project:
    """GET /projects.json API の応答に含まれる個々のプロジェクト."""

    id: int
    name: str
    identifier: str
    description: str
    homepage: str
    status: int
    is_public: bool
    inherit_members: bool
    created_on: datetime.datetime
    updated_on: datetime.datetime | None
    # 以下は include を指定した場合のみ取得できるオプションフィールド.
    trackers: list[ProjectTracker] | None = None
    issue_categories: list[IssueCategory] | None = None
    enabled_modules: list[ProjectModule] | None = None
    time_entry_activities: list[ProjectTimeEntryActivity] | None = None
    issue_custom_fields: list | None = None


@dataclass
class ProjectsResponse:
    """GET /projects.json API の応答を格納するクラス."""

    projects: list[Project]
    total_count: int
    offset: int
    limit: int


class ProjectsApi(RedmineApi):
    """Redmine Projects API クラス."""

    def get(self, params: dict | None = None, limit_total: int = 0) -> list[Project]:
        """API GET Projects を実行して Project データクラスのリストを取得する.

        Args:
            params (dict | None, optional): API のパラメータ (省略可).
                limit と offset は指定しても無視される.
            limit_total (int, optional): 最大取得件数. 0 以下で無制限. 省略時は 0.

        Raises:
            requests.HTTPError: HTTP 200 以外のステータスコード.
            requests.RequestException: リクエスト関連エラーの基底クラス.

        Returns:
            list[Project]: Project データクラスのリスト.
        """
        # デフォルトパラメータに指定パラメータをマージ (キー重複時は指定パラメータを優先).
        _params: dict = {"sort": "id"}
        _params |= params if params is not None else {}

        url: Final[str] = f"{self.url}/projects.json"
        total_items: list[Project] = []

        for response in self._get_generator(url, _params, limit_total):
            total_items.extend(ProjectsResponse(**response).projects)

        return total_items

    def lookup(self, project_id: int, params: dict | None = None) -> Project | None:
        """API GET Projects を実行して、指定された ID の Project データクラスを取得する.

        Args:
            project_id (int): 取得するアイテムの ID.
            params (dict | None, optional): API のパラメータ (省略可).

        Raises:
            requests.HTTPError: HTTP 200 と 404 以外のステータスコード.
            requests.RequestException: リクエスト関連エラーの基底クラス.

        Returns:
            Project | None: Project データクラス. 見つからない場合は None を返す.
        """
        url: Final[str] = f"{self.url}/projects/{project_id}.json"
        response: dict = self._get(url, params)

        return Project(**response["project"]) if response else None
