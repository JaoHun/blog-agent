from app.agent.registry import TOOL_REGISTRY, execute_tool
from app.agent.tool_schemas import TOOLS
from scripts.blog_check_utils import (
    choose_post_and_search_keyword,
    require_post_slug,
    require_published_posts,
)


source_post, keyword = choose_post_and_search_keyword(
    require_published_posts()
)
slug = require_post_slug(source_post)

expected_tools = {
    "search_posts",
    "get_post",
    "get_projects",
    "recommend_posts",
}

assert set(TOOL_REGISTRY) == expected_tools, (
    f"Registry tools mismatch: {set(TOOL_REGISTRY)}"
)

schema_names = {
    tool["function"]["name"]
    for tool in TOOLS
}

assert schema_names == expected_tools, (
    f"Tool schema names mismatch: {schema_names}"
)

result = execute_tool(
    "search_posts",
    {"query": keyword}
)

assert isinstance(result, list)
assert result, "search_posts 没有返回结果"

post = execute_tool(
    "get_post",
    {"slug": slug}
)

assert post is not None
assert post["slug"] == slug

projects = execute_tool(
    "get_projects",
    {}
)

assert isinstance(projects, list)
assert projects, "get_projects 没有返回真实项目"

recommendations = execute_tool(
    "recommend_posts",
    {
        "query": keyword,
        "limit": 1,
    }
)

assert isinstance(recommendations, list)
assert len(recommendations) <= 1

try:
    execute_tool(
        "unknown_tool",
        {}
    )
except ValueError:
    pass
else:
    raise AssertionError("未知工具应该抛出 ValueError")

print("PASS: Tool Registry 四工具验证通过")
print("search_posts:", len(result))
print("get_post:", post["title"])
print("get_projects:", len(projects))
print("recommend_posts:", len(recommendations))
