import uvicorn

from api.config import settings

if __name__ == "__main__":
    host = settings.run.host
    port = settings.run.port

    uvicorn.run(app="main:app", host=host, port=port, reload=settings.run.reload)
