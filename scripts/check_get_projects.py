import os
from tempfile import TemporaryDirectory

import app.tools.get_projects as get_projects_module


VALID_STATUSES = {
    "active",
    "maintained",
    "archived",
    "planned",
}


def expect_exception(func, expected_message: str):
    try:
        func()
    except Exception as exc:
        message = str(exc)

        assert expected_message in message, (
            f"Expected error to contain {expected_message!r}, got {message!r}"
        )

        return

    raise AssertionError(f"Expected exception containing {expected_message!r}")


class temporary_blog_root:
    def __init__(self, value: str | None):
        self.value = value
        self.previous = os.environ.get("BLOG_ROOT")

    def __enter__(self):
        if self.value is None:
            os.environ.pop("BLOG_ROOT", None)
        else:
            os.environ["BLOG_ROOT"] = self.value

    def __exit__(self, exc_type, exc, traceback):
        if self.previous is None:
            os.environ.pop("BLOG_ROOT", None)
        else:
            os.environ["BLOG_ROOT"] = self.previous


assert hasattr(
    get_projects_module,
    "get_projects",
), "get_projects 函数尚未实现"

projects = get_projects_module.get_projects()

assert isinstance(projects, list), "get_projects 应返回 list"
assert projects, "真实 projects.ts 至少应读取到 1 个项目"

for project in projects:
    for field in [
        "name",
        "description",
        "tech_stack",
        "status",
        "featured",
    ]:
        assert field in project, f"项目缺少字段 {field}: {project}"

    assert project["name"], f"项目 name 为空: {project}"
    assert project["description"], f"项目 description 为空: {project}"
    assert isinstance(
        project["tech_stack"],
        list,
    ), f"tech_stack 应为 list: {project}"
    assert project["status"] in VALID_STATUSES, (
        f"项目 status 非法: {project['status']}"
    )
    assert isinstance(
        project["featured"],
        bool,
    ), f"featured 应为 bool: {project}"


with TemporaryDirectory() as temp_dir:
    with temporary_blog_root(temp_dir):
        expect_exception(
            get_projects_module.get_projects,
            "Blog projects config does not exist",
        )


print("PASS: get_projects 真实项目读取验证通过")
print(f"项目数量: {len(projects)}")

for project in projects:
    print(
        project["name"],
        "=>",
        project["status"],
        project["tech_stack"],
    )
