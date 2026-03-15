import uvicorn

from src.app import make_app
from src.config.config import Settings

if __name__ == "__main__":
    uvicorn.run(app=make_app(), host="0.0.0.0", port=Settings().port)
