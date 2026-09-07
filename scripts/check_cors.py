from fastapi.middleware.cors import CORSMiddleware

from app.main import app


cors_middlewares = [
    middleware
    for middleware in app.user_middleware
    if middleware.cls is CORSMiddleware
]

assert cors_middlewares, "FastAPI app has no CORSMiddleware configured"

cors_config = cors_middlewares[0].kwargs
origins = cors_config.get("allow_origins", [])

assert "http://localhost:3000" in origins, (
    "CORS must allow the Next.js dev origin http://localhost:3000"
)
assert "http://127.0.0.1:3000" in origins, (
    "CORS must allow the Next.js dev origin http://127.0.0.1:3000"
)
assert cors_config.get("allow_methods") == ["*"], (
    "CORS must allow all methods for browser preflight"
)
assert cors_config.get("allow_headers") == ["*"], (
    "CORS must allow all headers for JSON requests"
)

print("PASS: FastAPI CORS configuration validation passed")
