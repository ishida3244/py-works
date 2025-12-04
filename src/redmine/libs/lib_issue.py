"""チケット用データクラス."""

import datetime

from pydantic.dataclasses import dataclass


@dataclass
class IssueProject:
    """チケットのプロジェクト."""

    id: int
    name: str


@dataclass
class Tracker:
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
class Author:
    """チケットの起票者."""

    id: int
    name: str


@dataclass
class Issue:
    """GET /issues.json API の応答に含まれる個々のチケット."""

    id: int
    project: IssueProject
    tracker: Tracker
    status: Status
    priority: Priority
    author: Author
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


@dataclass
class IssuesResponse:
    """GET /issues.json API の応答を格納するクラス."""

    issues: list[Issue]
    total_count: int
    offset: int
    limit: int
