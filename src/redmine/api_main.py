"""API 呼び出し."""

from pprint import PrettyPrinter

from consts import API_KEY, API_URL
from libs.lib_issue import IssuesApi
from libs.lib_project import ProjectsApi
from libs.lib_time_entry import TimeEntriesApi
from libs.lib_user import UsersApi

pp = PrettyPrinter(indent=2)

# チケット.
issues_api = IssuesApi(key=API_KEY, url=API_URL)
pp.pprint(issues_api.lookup(issue_id=13))
pp.pprint(issues_api.lookup(issue_id=86, params={"include": "journals"}))
print(f"count={len(issues_api.get())}")
print(f"count={len(issues_api.get(limit_total=5))}")
print(f"count={len(issues_api.get({"status_id": "*"}, limit_total=55))}")
print(f"count={len(issues_api.get({"status_id": "*"}, limit_total=73))}")
print(f"count={len(issues_api.get({"status_id": "*"}, limit_total=80))}")

# プロジェクト.
projects_api = ProjectsApi(key=API_KEY, url=API_URL)
pp.pprint(projects_api.lookup(project_id=14, params={"include": "issue_categories"}))
print(f"count={len(projects_api.get())}")

# 有効なユーザー.
users_api = UsersApi(key=API_KEY, url=API_URL)
pp.pprint(users_api.lookup(user_id=5))
pp.pprint(users_api.lookup(user_id=13, params={"include": "memberships,groups"}))
print(f"count={len(users_api.get({"status": 1}))}")

# 作業時間.
time_entries_api = TimeEntriesApi(key=API_KEY, url=API_URL)
pp.pprint(time_entries_api.lookup(entry_id=135))
print(f"count={len(time_entries_api.get())}")
