"""プロジェクト用データクラス."""

import datetime

from pydantic.dataclasses import dataclass


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


@dataclass
class ProjectsResponse:
    """GET /projects.json API の応答を格納するクラス."""

    projects: list[Project]
    total_count: int
    offset: int
    limit: int
