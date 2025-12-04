"""API 呼び出しクラス."""

from pprint import PrettyPrinter
from typing import Final

import requests

from .lib_issue import Issue, IssuesResponse
from .lib_project import Project, ProjectsResponse


class RedmineApi:
    """Redmine API クラス."""

    def __init__(self, key: str, url: str) -> None:
        """コンストラクタ.

        Args:
            key (str): API キー.
            url (str): Redmine API ホストの URL.
        """
        self.headers: dict = {
            "X-Redmine-API-Key": key,
            "Content-Type": "application/json; charset=utf-8",
        }
        self.url: Final[str] = url
        self.pp = PrettyPrinter(indent=2)

    def get_issues(self, api_params: dict | None = None) -> list[Issue]:
        """すべてのチケットを Issue データクラスのリストで取得する.

        Args:
            api_params (dict | None, optional): API 'Issues' のパラメータを指定できる.
                'limit'と'offset'は指定しても無視される. 省略時は指定なし.

        Returns:
            list[Issue]: チケットのリスト.
        """
        limit: int = 25
        offset: int = 0
        total_items: list[Issue] = []

        params: dict = {"status_id": "*", "sort": "project,id"}
        params |= {} if api_params is None else api_params

        for _i in range(100):
            response: requests.Response = requests.get(
                url=f"{self.url}/issues.json",
                headers=self.headers,
                params=params | {"limit": limit, "offset": offset},
                timeout=100,
                verify=False,
            )

            if response.status_code != 200:
                print(f"Error: status_code={response.status_code}, '{response.text}'")
                break

            response_data = IssuesResponse(**response.json())
            total_items.extend(response_data.issues)

            offset = response_data.offset
            limit = response_data.limit
            if offset + limit >= response_data.total_count:
                break

            offset += limit

        return total_items

    def get_projects(self, api_params: dict | None = None) -> list[Project]:
        """すべてのプロジェクトを Project データクラスのリストで取得する.

        Args:
            api_params (dict | None, optional): API 'Project' のパラメータを指定できる.
                'limit'と'offset'は指定しても無視される. 省略時は指定なし.

        Returns:
            list[Project]: プロジェクトのリスト.
        """
        limit: int = 25
        offset: int = 0
        total_items: list[Project] = []

        params: dict = {"sort": "id"}
        params |= {} if api_params is None else api_params

        for _i in range(100):
            response: requests.Response = requests.get(
                url=f"{self.url}/projects.json",
                headers=self.headers,
                params=params | {"limit": limit, "offset": offset},
                timeout=100,
                verify=False,
            )

            if response.status_code != 200:
                print(f"Error: status_code={response.status_code}, '{response.text}'")
                break

            response_data = ProjectsResponse(**response.json())
            total_items.extend(response_data.projects)

            offset = response_data.offset
            limit = response_data.limit
            if offset + limit >= response_data.total_count:
                break

            offset += limit

        return total_items

    def pprint(self, obj: object):
        """pprint.PrettyPrinter.pprint()のラッパーメソッド.

        Args:
            obj (object): 出力するオブジェクト.
        """
        self.pp.pprint(obj)
