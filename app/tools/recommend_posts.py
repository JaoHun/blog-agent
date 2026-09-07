from app.repositories.blog_repository import load_posts


MAX_LIMIT = 3


def recommend_posts(query: str, limit: int = MAX_LIMIT) -> list[dict]:
    terms = normalize_query_terms(query)

    if not terms:
        return []

    limit = clamp_limit(limit)
    ranked_posts = []

    for index, post in enumerate(load_posts()):
        score = score_post(post, terms)

        if score == 0:
            continue

        ranked_posts.append((score, index, post))

    ranked_posts.sort(
        key=lambda item: (
            -item[0],
            item[1],
        )
    )

    return [
        format_recommended_post(post)
        for _, _, post in ranked_posts[:limit]
    ]


def normalize_query_terms(query: str) -> list[str]:
    normalized_query = str(query or "").strip().lower()

    if not normalized_query:
        return []

    return [
        term
        for term in normalized_query.split()
        if term
    ]


def clamp_limit(limit: int) -> int:
    normalized_limit = int(limit)

    if normalized_limit < 1:
        return 1

    if normalized_limit > MAX_LIMIT:
        return MAX_LIMIT

    return normalized_limit


def score_post(post: dict, terms: list[str]) -> int:
    title = str(post.get("title") or "").lower()
    category = str(post.get("category") or "").lower()
    excerpt = str(post.get("excerpt") or "").lower()
    tags = post.get("tags", [])

    if not isinstance(tags, list):
        tags = []

    tag_text = " ".join(
        str(tag)
        for tag in tags
    ).lower()

    return (
        score_text(title, terms, 4)
        + score_text(tag_text, terms, 3)
        + score_text(category, terms, 2)
        + score_text(excerpt, terms, 1)
    )


def score_text(text: str, terms: list[str], weight: int) -> int:
    return sum(
        weight
        for term in terms
        if term in text
    )


def format_recommended_post(post: dict) -> dict:
    tags = post.get("tags", [])

    if not isinstance(tags, list):
        tags = []

    return {
        "title": post.get("title"),
        "slug": post.get("slug"),
        "excerpt": post.get("excerpt"),
        "category": post.get("category"),
        "tags": tags,
    }
