import app.tools.search_posts as search_module
from scripts.blog_check_utils import (
    choose_post_and_search_keyword,
    require_post_slug,
    require_published_posts,
)


assert hasattr(
    search_module,
    "search_posts"
), "search_posts 函数尚未实现"

search_posts = search_module.search_posts


source_post, keyword = choose_post_and_search_keyword(
    require_published_posts()
)
slug = require_post_slug(source_post)
results = search_posts(keyword)

assert results, f"搜索动态关键词没有找到任何文章: {keyword}"

assert any(
    post["slug"] == slug
    for post in results
), f"没有找到动态选择的文章: {slug}"


lowercase_results = search_posts(keyword.lower())

assert any(
    post["slug"] == slug
    for post in lowercase_results
), "搜索应该忽略英文大小写"


empty_results = search_posts("完全不存在的关键词123456")

assert empty_results == [], "不存在的关键词应该返回空列表"


print("PASS: search_posts 基础搜索验证通过")

for post in results:
    print(
        post["title"],
        "=>",
        post["slug"]
    )
