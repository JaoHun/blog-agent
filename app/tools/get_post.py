from app.repositories.blog_repository import get_post_by_slug


def get_post(slug: str) -> dict | None:
    slug = slug.strip()

    if not slug:
        return None

    post = get_post_by_slug(slug)

    if post is None:
        return None

    return {
        "title": post.get("title"),
        "slug": post.get("slug"),
        "excerpt": post.get("excerpt"),
        "category": post.get("category"),
        "tags": post.get("tags", []),
        "content": post.get("content", ""),
    }