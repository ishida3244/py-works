"""ユーザークラス.
https://www.redmine.org/projects/redmine/wiki/Rest_Users
"""

import datetime
from typing import Final

from pydantic.dataclasses import dataclass

from .lib_api import RedmineApi


@dataclass
class MembershipProject:
    """GET /users/id.json API の応答に含まれる個々のメンバーシップのプロジェクト."""

    id: int
    name: str


@dataclass
class MembershipRole:
    """GET /users/id.json API の応答に含まれる個々のメンバーシップのロール."""

    id: int
    name: str
    # レスポンスに inherited が存在しない場合があるのでオプションフィールドにする.
    inherited: bool | None = None


@dataclass
class Membership:
    """GET /users/id.json API の応答に含まれる個々のメンバーシップ."""

    id: int
    project: MembershipProject
    roles: list[MembershipRole]


@dataclass
class Group:
    """GET /users/id.json API の応答に含まれる個々のグループ."""

    id: int
    name: str


@dataclass
class User:
    """GET /users.json API の応答に含まれる個々のユーザー."""

    id: int
    admin: bool
    updated_on: datetime.datetime | None
    passwd_changed_on: datetime.datetime | None
    avatar_url: str | None
    twofa_scheme: str | None
    # 以下は対象ユーザーのロック状態と API 呼び出しの権限によって存在しない場合がある.
    firstname: str | None = None
    lastname: str | None = None
    mail: str | None = None
    created_on: datetime.datetime | None = None
    last_login_on: datetime.datetime | None = None
    login: str | None = None
    api_key: str | None = None
    status: int | None = None
    # 以下は include を指定した場合のみ取得できるオプションフィールド.
    memberships: list[Membership] | None = None
    groups: list[Group] | None = None


@dataclass
class UsersResponse:
    """GET /users.json API の応答を格納するクラス."""

    users: list[User]
    total_count: int
    offset: int
    limit: int


class UsersApi(RedmineApi):
    """Redmine Users API クラス."""

    def get(self, params: dict | None = None, limit_total: int = 0) -> list[User]:
        """API GET Users を実行して User データクラスのリストを取得する.

        Args:
            params (dict | None, optional): API のパラメータ (省略可).
                limit と offset は指定しても無視される.
            limit_total (int, optional): 最大取得件数. 0 以下で無制限. 省略時は 0.

        Raises:
            requests.HTTPError: HTTP 200 以外のステータスコード.
            requests.RequestException: リクエスト関連エラーの基底クラス.

        Returns:
            list[User]: User データクラスのリスト.
        """
        # デフォルトパラメータに指定パラメータをマージ (キー重複時は指定パラメータを優先).
        _params: dict = {"sort": "id"}
        _params |= params if params is not None else {}

        url: Final[str] = f"{self.url}/users.json"
        total_items: list[User] = []

        for response in self._get_generator(url, _params, limit_total):
            total_items.extend(UsersResponse(**response).users)

        return total_items

    def lookup(self, user_id: int, params: dict | None = None) -> User | None:
        """API GET Users を実行して、指定された ID の User データクラスを取得する.

        Args:
            user_id (int): 取得するアイテムの ID.
            params (dict | None, optional): API のパラメータ (省略可).

        Raises:
            requests.HTTPError: HTTP 200 と 404 以外のステータスコード.
            requests.RequestException: リクエスト関連エラーの基底クラス.

        Returns:
            User | None: User データクラス. 見つからない場合は None を返す.
        """
        url: Final[str] = f"{self.url}/users/{user_id}.json"
        response: dict = self._get(url, params)

        return User(**response["user"]) if response else None
