from app.repositories.blog_repository import load_posts


def require_published_posts() -> list[dict]:
    posts = load_posts()

    if not posts:
        raise AssertionError("No published posts available for integration check")

    return posts


def require_post_slug(post: dict) -> str:
    slug = post.get("slug")

    if not slug:
        raise AssertionError("Selected post does not have a slug")

    return str(slug)


def choose_post_and_search_keyword(posts: list[dict]) -> tuple[dict, str]:
    for post in posts:
        keyword = choose_search_keyword_with_ascii(post)

        if keyword:
            return post, keyword

    for post in posts:
        keyword = choose_any_search_keyword(post)

        if keyword:
            return post, keyword

    raise AssertionError("No published posts have searchable metadata")


def choose_search_keyword(post: dict) -> str:
    keyword = choose_search_keyword_with_ascii(post)

    if keyword:
        return keyword

    return choose_any_search_keyword(post)


def choose_search_keyword_with_ascii(post: dict) -> str | None:
    for keyword in search_keyword_candidates(post):
        if any(character.isascii() and character.isalpha() for character in keyword):
            return keyword

    return None


def choose_any_search_keyword(post: dict) -> str:
    for keyword in search_keyword_candidates(post):
        return keyword

    raise AssertionError("Selected post has no searchable title, tag, category, or excerpt")


def search_keyword_candidates(post: dict) -> list[str]:
    keywords = []
    candidates = [
        post.get("title"),
        post.get("category"),
        post.get("excerpt"),
    ]

    tags = post.get("tags", [])

    if isinstance(tags, list):
        candidates.extend(tags)

    for candidate in candidates:
        keyword = str(candidate or "").strip()

        if keyword:
            keywords.append(keyword)

    return keywords
