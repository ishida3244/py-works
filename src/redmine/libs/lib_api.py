"""Redmine REST API クラス.
https://www.redmine.org/projects/redmine/wiki/Rest_api
"""

from collections.abc import Generator
from typing import Final

import requests


class RedmineApi:
    """Redmine REST API クラス."""

    def __init__(self, key: str, url: str, limit_default: int = 25) -> None:
        """コンストラクタ.

        Args:
            key (str): API キー.
            url (str): Redmine API ホストの URL.
            limit_default (int): 1 回の API 呼び出しで取得するアイテム数.
        """
        self.headers: Final[dict] = {
            "X-Redmine-API-Key": key,
            "Content-Type": "application/json; charset=utf-8",
        }
        self.url: Final[str] = url
        self.limit_default: Final[int] = limit_default

    def _get_generator(
        self, url: str, params: dict, limit_total: int = 0
    ) -> Generator[dict, None, None]:
        """GET リクエストのレスポンスを辞書形式で返すジェネレータ.
        必要に応じて複数回の GET リクエストを実行し、都度レスポンスデータを返す.

        Args:
            url (str): API の URL.
            params (dict): API のパラメータ. limit と offset は指定しても無視される.
            limit_total (int, optional): 最大取得件数. 0 以下で無制限. 省略時は 0.

        Raises:
            requests.HTTPError: HTTP 200 以外のステータスコード.
            requests.RequestException: リクエスト関連エラーの基底クラス.

        Yields:
            dict: レスポンスデータを辞書形式で返す.
        """
        # 最大取得件数 (limit_total) としてデフォルトの limit 値より小さいが指定された場合は、
        # limit = 最大取得件数とする.
        limit: int = (
            limit_total if 0 < limit_total < self.limit_default else self.limit_default
        )

        offset: int = 0

        for _ in range(100):
            response: requests.Response = requests.get(
                url=url,
                headers=self.headers,
                params=params | {"limit": limit, "offset": offset},
                timeout=100,
                verify=False,
            )

            if (rc := response.status_code) != 200:
                raise requests.HTTPError(f"Error: status_code={rc}, '{response.text}'")

            response_dict: dict = response.json()
            yield response_dict

            # 最大取得件数 (limit_total) が指定されなかったか、または総アイテム数 (total_count) が最大
            # 取得件数 (limit_total) より小さい場合は、最大取得件数 = 総アイテム数とする.
            total_count: int = int(response_dict["total_count"])
            if limit_total <= 0 or total_count < limit_total:
                limit_total = total_count

            # offset と limit の合計が最大取得件数以上ならループを脱出する.
            if offset + limit >= limit_total:
                break

            # 次回のループで取得アイテム数の累計が最大取得件数 (limit_total) を超える場合は、次回の
            # 取得アイテム数 (limit) を調整して、累計が最大取得件数を超えないようにする.
            offset += limit
            if offset + limit > limit_total:
                limit = limit_total - offset

    def _get(self, url: str, params: dict | None = None) -> dict:
        """GET リクエストのレスポンスを辞書形式で返す.

        Args:
            url (str): API の URL.
            params (dict | None, optional): API のパラメータ (省略可).

        Raises:
            requests.HTTPError: HTTP 200 と 404 以外のステータスコード.
            requests.RequestException: リクエスト関連エラーの基底クラス.

        Returns:
            dict: レスポンスデータを辞書形式で返す. HTTP 404 で空の辞書を返す.
        """
        response: requests.Response = requests.get(
            url=url,
            headers=self.headers,
            params=params,
            timeout=100,
            verify=False,
        )

        if (rc := response.status_code) != 200:
            if rc == 404:
                return {}
            raise requests.HTTPError(f"Error: status_code={rc}, '{response.text}'")

        return response.json()
