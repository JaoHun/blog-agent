import os
from pathlib import Path
from tempfile import TemporaryDirectory

from app.config import get_blog_posts_dir
from app.repositories.blog_repository import load_posts


def expect_exception(func, expected_message: str):
    try:
        func()
    except Exception as exc:
        message = str(exc)

        assert expected_message in message, (
            f"Expected error to contain {expected_message!r}, got {message!r}"
        )

        return

    raise AssertionError(f"Expected exception containing {expected_message!r}")


class temporary_blog_root:
    def __init__(self, value: str | None):
        self.value = value
        self.previous = os.environ.get("BLOG_ROOT")

    def __enter__(self):
        if self.value is None:
            os.environ.pop("BLOG_ROOT", None)
        else:
            os.environ["BLOG_ROOT"] = self.value

    def __exit__(self, exc_type, exc, traceback):
        if self.previous is None:
            os.environ.pop("BLOG_ROOT", None)
        else:
            os.environ["BLOG_ROOT"] = self.previous


with temporary_blog_root(None):
    expect_exception(
        get_blog_posts_dir,
        "BLOG_ROOT environment variable is not set",
    )


with TemporaryDirectory() as temp_dir:
    with temporary_blog_root(temp_dir):
        expect_exception(
            load_posts,
            "Blog posts directory does not exist",
        )


with TemporaryDirectory() as temp_dir:
    posts_dir = Path(temp_dir)
    invalid_post = posts_dir / "invalid-frontmatter.mdx"
    invalid_post.write_text(
        "---\n- foo\n- bar\n---\ncontent\n",
        encoding="utf-8",
    )

    expect_exception(
        lambda: load_posts(posts_dir),
        "expected a mapping",
    )


with TemporaryDirectory() as temp_dir:
    posts_dir = Path(temp_dir)
    invalid_post = posts_dir / "empty-frontmatter.mdx"
    invalid_post.write_text(
        "---\n---\ncontent\n",
        encoding="utf-8",
    )

    expect_exception(
        lambda: load_posts(posts_dir),
        "expected a mapping",
    )


print("PASS: Blog repository error handling validation passed")
