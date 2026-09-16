import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOTENV_PATH = PROJECT_ROOT / ".env"


def load_environment(env_file: Path | str = DOTENV_PATH) -> None:
    load_dotenv(dotenv_path=env_file, override=False)


load_environment()


def get_required_env(name: str) -> str:
    value = os.environ.get(name)

    if value is None or not value.strip():
        raise RuntimeError(f"{name} environment variable is not set")

    return value.strip()


def get_deepseek_api_key() -> str:
    return get_required_env("DEEPSEEK_API_KEY")


def get_blog_root() -> Path:
    return Path(get_required_env("BLOG_ROOT"))


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
