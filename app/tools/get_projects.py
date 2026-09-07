from app.repositories.blog_repository import load_projects


def get_projects() -> list[dict]:
    return load_projects()
