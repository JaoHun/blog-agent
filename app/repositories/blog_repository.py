from pathlib import Path

import json5
import yaml

from app.config import get_blog_posts_dir, get_blog_projects_config_path


def resolve_posts_dir(posts_dir: Path | None = None) -> Path:
    if posts_dir is None:
        posts_dir = get_blog_posts_dir()
    else:
        posts_dir = Path(posts_dir)

    if not posts_dir.is_dir():
        raise RuntimeError(f"Blog posts directory does not exist: {posts_dir}")

    return posts_dir


def read_frontmatter(file_path: Path) -> dict:
    content = file_path.read_text(
        encoding="utf-8"
    )

    if not content.startswith("---"):
        return {}

    parts = content.split("---", 2)

    if len(parts) < 3:
        return {}

    metadata = yaml.safe_load(parts[1])

    if not isinstance(metadata, dict):
        raise ValueError(
            f"Invalid frontmatter in {file_path}: expected a mapping"
        )

    metadata.setdefault(
        "slug",
        file_path.stem
    )

    return metadata


def load_posts(posts_dir: Path | None = None) -> list[dict]:
    posts = []
    resolved_posts_dir = resolve_posts_dir(posts_dir)

    for file_path in resolved_posts_dir.glob("*.mdx"):

        metadata = read_frontmatter(file_path)

        if not metadata:
            continue

        if metadata.get("draft") is True:
            continue

        metadata["source_path"] = str(file_path)

        posts.append(metadata)

    return posts


def get_post_by_slug(
    slug: str,
    posts_dir: Path | None = None,
) -> dict | None:
    resolved_posts_dir = resolve_posts_dir(posts_dir)

    for file_path in resolved_posts_dir.glob("*.mdx"):
        metadata = read_frontmatter(file_path)

        if not metadata:
            continue

        if metadata.get("draft") is True:
            continue

        if metadata.get("slug") != slug:
            continue

        text = file_path.read_text(encoding="utf-8")
        parts = text.split("---", 2)

        if len(parts) < 3:
            body = ""
        else:
            body = parts[2].strip()

        metadata["content"] = body
        metadata["source_path"] = str(file_path)

        return metadata

    return None


def resolve_projects_config_path(
    projects_config_path: Path | None = None,
) -> Path:
    if projects_config_path is None:
        projects_config_path = get_blog_projects_config_path()
    else:
        projects_config_path = Path(projects_config_path)

    if not projects_config_path.is_file():
        raise RuntimeError(
            f"Blog projects config does not exist: {projects_config_path}"
        )

    return projects_config_path


def extract_project_object_texts(source: str) -> list[str]:
    object_texts = []
    marker = "projectSchema.parse("
    search_from = 0

    while True:
        marker_index = source.find(marker, search_from)

        if marker_index == -1:
            break

        object_start = source.find("{", marker_index + len(marker))

        if object_start == -1:
            break

        object_text, object_end = extract_balanced_object(
            source,
            object_start,
        )

        object_texts.append(object_text)
        search_from = object_end + 1

    return object_texts


def extract_balanced_object(source: str, object_start: int) -> tuple[str, int]:
    depth = 0
    in_string = None
    escaped = False

    for index in range(object_start, len(source)):
        character = source[index]

        if in_string is not None:
            if escaped:
                escaped = False
                continue

            if character == "\\":
                escaped = True
                continue

            if character == in_string:
                in_string = None

            continue

        if character in ("'", '"', "`"):
            in_string = character
            continue

        if character == "{":
            depth += 1
            continue

        if character == "}":
            depth -= 1

            if depth == 0:
                return source[object_start:index + 1], index

    raise ValueError(
        "Could not parse projectSchema.parse object: unbalanced braces"
    )


def load_projects(
    projects_config_path: Path | None = None,
) -> list[dict]:
    resolved_config_path = resolve_projects_config_path(projects_config_path)
    source = resolved_config_path.read_text(encoding="utf-8")
    projects = []

    for object_text in extract_project_object_texts(source):
        raw_project = json5.loads(object_text)

        if not isinstance(raw_project, dict):
            raise ValueError(
                "Invalid project config: expected projectSchema.parse object"
            )

        description_by_lang = raw_project.get("descriptionByLang")

        if isinstance(description_by_lang, dict):
            description = (
                description_by_lang.get("zh")
                or raw_project.get("description")
                or ""
            )
        else:
            description = raw_project.get("description") or ""

        tech_stack = raw_project.get("techStack", [])

        if not isinstance(tech_stack, list):
            tech_stack = []

        projects.append(
            {
                "name": str(raw_project.get("name") or ""),
                "description": str(description),
                "tech_stack": [
                    str(technology)
                    for technology in tech_stack
                ],
                "status": str(raw_project.get("status") or ""),
                "featured": bool(raw_project.get("featured", False)),
                "source_url": raw_project.get("sourceUrl"),
                "demo_url": raw_project.get("demoUrl"),
                "article_url": raw_project.get("articleUrl"),
            }
        )

    return projects
