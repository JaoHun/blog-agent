import app.tools.recommend_posts as recommend_module
from scripts.blog_check_utils import (
    choose_post_and_search_keyword,
    require_post_slug,
    require_published_posts,
    search_keyword_candidates,
)


assert hasattr(
    recommend_module,
    "recommend_posts",
), "recommend_posts 函数尚未实现"

recommend_posts = recommend_module.recommend_posts
published_posts = require_published_posts()
published_slugs = {
    require_post_slug(post)
    for post in published_posts
}

source_post, keyword = choose_post_and_search_keyword(published_posts)
slug = require_post_slug(source_post)
results = recommend_posts(keyword)

assert results, f"真实关键词应该推荐至少一篇文章: {keyword}"
assert len(results) <= 3, "默认推荐数量最多为 3"
assert any(
    post["slug"] == slug
    for post in results
), f"没有推荐动态选择的文章: {slug}"

for post in results:
    assert post["slug"] in published_slugs, (
        f"推荐结果不在已发布文章列表中: {post}"
    )

    for field in [
        "title",
        "slug",
        "excerpt",
        "category",
        "tags",
    ]:
        assert field in post, f"推荐结果缺少字段 {field}: {post}"


limited_results = recommend_posts(keyword, limit=1)

assert len(limited_results) <= 1, "limit=1 时最多返回 1 篇"


english_keyword = None

for post in published_posts:
    for candidate in search_keyword_candidates(post):
        if any(character.isascii() and character.isalpha() for character in candidate):
            english_keyword = candidate
            break

    if english_keyword:
        break

if english_keyword:
    lower_results = recommend_posts(english_keyword.lower())
    upper_results = recommend_posts(english_keyword.upper())

    assert lower_results == upper_results, (
        f"英文大小写应保持结果一致: {english_keyword}"
    )
else:
    print("SKIP: 当前真实博客没有合适英文关键词，跳过大小写子检查")


missing_results = recommend_posts("__no_matching_blog_topic_9f73a1__")

assert missing_results == [], "无匹配时应该返回空列表"


print("PASS: recommend_posts 真实文章推荐验证通过")
print("关键词:", keyword)

for post in results:
    print(
        post["title"],
        "=>",
        post["slug"],
    )
