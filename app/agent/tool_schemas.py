TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_posts",
            "description": (
                "搜索个人博客中已经发布的文章。"
                "当用户询问有哪些文章、某个主题相关的文章、"
                "或者想查找博客内容时使用。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "用于搜索博客文章的关键词，"
                            "例如 Agent、博客、Python"
                        ),
                    }
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_post",
            "description": (
                "根据文章 slug 读取一篇已经发布的博客文章完整内容。"
                "当用户要求查看、解释或总结某篇具体文章时使用。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "slug": {
                        "type": "string",
                        "description": (
                            "博客文章的唯一 slug，"
                            "例如 article-slug"
                        ),
                    }
                },
                "required": ["slug"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_projects",
            "description": (
                "获取博客作者公开展示的真实项目列表，"
                "包括项目描述、技术栈、状态以及可用链接。"
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "recommend_posts",
            "description": (
                "根据用户感兴趣的主题，"
                "从博客现有已发布文章中推荐相关内容。"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "用户感兴趣的主题或关键词",
                    },
                    "limit": {
                        "type": "integer",
                        "minimum": 1,
                        "maximum": 3,
                        "default": 3,
                    },
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
]
