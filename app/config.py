import os
from pathlib import Path


def get_blog_root() -> Path:
    blog_root = os.environ.get("BLOG_ROOT")

    if blog_root is None or not blog_root.strip():
        raise RuntimeError("BLOG_ROOT environment variable is not set")

    return Path(blog_root)


def get_blog_posts_dir() -> Path:
    posts_dir = (
        get_blog_root()
        / "frontend"
        / "content"
        / "posts"
    )

    if not posts_dir.is_dir():
        raise RuntimeError(f"Blog posts directory does not exist: {posts_dir}")

    return posts_dir


def get_blog_projects_config_path() -> Path:
    return (
        get_blog_root()
        / "frontend"
        / "config"
        / "projects.ts"
    )
