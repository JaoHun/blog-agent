\# Blog Agent



基于 Python + FastAPI 开发的个人博客智能 Agent 后端项目。



\## 当前进度



已完成并验证：



\- FastAPI 后端基础服务

\- `GET /health` 健康检查接口

\- `POST /chat` 聊天接口

\- Pydantic 请求与响应模型

\- DeepSeek API 调用封装

\- FastAPI → DeepSeek API → LLM Response 完整调用链路



\## 技术栈



\- Python

\- FastAPI

\- Pydantic

\- Requests

\- DeepSeek API

\- Uvicorn



\## 当前架构



```text

Client

&#x20; ↓

FastAPI /chat

&#x20; ↓

Pydantic

&#x20; ↓

DeepSeek Client

&#x20; ↓

DeepSeek API

