from app.agent.agent import run_agent_with_trace
from app.config import get_deepseek_api_key
from scripts.blog_check_utils import (
    choose_post_and_search_keyword,
    require_post_slug,
    require_published_posts,
)


get_deepseek_api_key()


def check_case(question: str, expected_tool: str | None) -> list[str]:
    print("\nQuestion:", question)

    reply, tools_used = run_agent_with_trace(question)

    print("Tools used:", tools_used)
    print("Answer:", reply)

    passed = bool(reply)

    if expected_tool is None:
        passed = passed and tools_used == []
    else:
        passed = passed and expected_tool in tools_used

    print("PASS" if passed else "FAIL")

    if not passed:
        if expected_tool is None:
            raise AssertionError(
                f"本场景不应该调用工具: {tools_used}"
            )

        raise AssertionError(
            f"预期调用 {expected_tool}，实际调用 {tools_used}"
        )

    return tools_used


posts = require_published_posts()
source_post, keyword = choose_post_and_search_keyword(posts)
slug = require_post_slug(source_post)


scene_1_tools = check_case(
    f"请搜索我的博客中和 {keyword} 有关的文章，只能根据博客真实数据回答。",
    "search_posts",
)

scene_2_tools = check_case(
    f"请读取 slug 为 {slug} 的博客文章，并概括主要内容。",
    "get_post",
)

scene_3_tools = check_case(
    "你好",
    None,
)

scene_4_tools = check_case(
    "你博客里有哪些项目？简单介绍一下。",
    "get_projects",
)

_, recommendation_topic = choose_post_and_search_keyword(posts)

scene_5_tools = check_case(
    f"我想了解 {recommendation_topic}，推荐几篇你博客里的相关文章。",
    "recommend_posts",
)

print("\nScene 1 ->", scene_1_tools)
print("Scene 2 ->", scene_2_tools)
print("Scene 3 ->", scene_3_tools)
print("Scene 4 ->", scene_4_tools)
print("Scene 5 ->", scene_5_tools)
print("\nPASS: Agent four-tool calling validation passed")
