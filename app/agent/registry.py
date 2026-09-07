from app.tools.get_post import get_post
from app.tools.get_projects import get_projects
from app.tools.recommend_posts import recommend_posts
from app.tools.search_posts import search_posts


TOOL_REGISTRY = {
    "search_posts": search_posts,
    "get_post": get_post,
    "get_projects": get_projects,
    "recommend_posts": recommend_posts,
}


def execute_tool(name: str, arguments: dict):
    tool = TOOL_REGISTRY.get(name)

    if tool is None:
        raise ValueError(f"未知工具: {name}")

    return tool(**arguments)
