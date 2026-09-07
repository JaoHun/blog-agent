import app.tools.get_post as get_post_module
from scripts.blog_check_utils import require_post_slug, require_published_posts


assert hasattr(
    get_post_module,
    "get_post"
), "get_post 函数尚未实现"

get_post = get_post_module.get_post


source_post = require_published_posts()[0]
slug = require_post_slug(source_post)
post = get_post(slug)

assert post is not None, f"没有找到动态选择的文章: {slug}"

assert post["slug"] == slug
assert post["title"], "文章缺少 title"
assert post["content"], "文章正文为空"


missing_post = get_post("not-exist-post-123456")

assert missing_post is None, "不存在的文章应该返回 None"


print("PASS: get_post 基础验证通过")
print(post["title"])
print("slug:", post["slug"])
print("正文长度:", len(post["content"]))
