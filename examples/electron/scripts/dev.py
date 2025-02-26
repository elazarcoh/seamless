import os
from pathlib import Path
import sys

HERE = Path(__file__).parent
sys.path.append(str(HERE.parent))


if __name__ == "__main__":
    import uvicorn

    HOST = os.getenv("UVICORN_HOST")
    if HOST is None:
        raise ValueError("UVICORN_HOST environment variable is not set")

    PORT = os.getenv("UVICORN_PORT")
    if PORT is None:
        raise ValueError("UVICORN_PORT environment variable is not set")
    PORT = int(PORT)

    uvicorn.run(
        "engine.main:app",
        host=HOST,
        port=PORT,
        reload=True,
        reload_dirs=[str(HERE)],
    )

