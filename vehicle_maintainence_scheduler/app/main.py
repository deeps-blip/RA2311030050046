from fastapi import FastAPI
from app.api.endpoints import router
from app.middleware.logging import LoggingMiddleware

app = FastAPI(title="Vehicle Maintenance Scheduler")

app.add_middleware(LoggingMiddleware)
app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
