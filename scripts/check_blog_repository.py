from app.repositories.blog_repository import load_posts


posts = load_posts()

if not posts:
    raise AssertionError("No published posts available for integration check")

assert all(
    post.get("slug")
    for post in posts
), "存在没有 slug 的文章"

print(f"读取文章数量: {len(posts)}")

for post in posts:
    print(
        post.get("title"),
        "=>",
        post.get("slug")
    )
