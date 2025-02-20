import os
from pathlib import Path

HERE = Path(__file__).parent

HOST = os.getenv("HOST")
if HOST is None:
    raise ValueError("HOST environment variable is not set")

PORT = os.getenv("PORT")
if PORT is None:
    raise ValueError("PORT environment variable is not set")
PORT = int(PORT)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api:app",
        host=HOST,
        port=PORT,
        reload=True,
        reload_dirs=[str(HERE)],
    )

