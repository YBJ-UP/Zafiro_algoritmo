import uvicorn
from dotenv import load_dotenv
from os import getenv

load_dotenv()
PORT: str | None = getenv("PORT")
assert PORT is not None
port:int = int(PORT)

def main() -> None:
    if __name__ == "__main__":
        uvicorn.run(app="src.routes:app", port=port)