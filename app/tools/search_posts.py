from app.repositories.blog_repository import load_posts


def search_posts(query: str) -> list[dict]:
    query = query.strip().lower()

    if not query:
        return []

    results = []

    for post in load_posts():
        title = str(post.get("title", ""))
        excerpt = str(post.get("excerpt", ""))
        category = str(post.get("category", ""))

        tags = post.get("tags", [])

        if not isinstance(tags, list):
            tags = []

        searchable_text = " ".join(
            [
                title,
                excerpt,
                category,
                *[str(tag) for tag in tags],
            ]
        ).lower()

        if query in searchable_text:
            results.append(
                {
                    "title": post.get("title"),
                    "slug": post.get("slug"),
                    "excerpt": post.get("excerpt"),
                    "category": post.get("category"),
                    "tags": post.get("tags", []),
                }
            )

    return results