import uvicorn

def main() -> None:
    if __name__ == "__main__":
        uvicorn.run(app="src.routes:app", port=8000, reload=True)