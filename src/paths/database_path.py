from pathlib import Path

DATABASE_NAME = "cas_portfolios.db"

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASE = BASE_DIR.joinpath(DATABASE_NAME)

if __name__ == "__main__":
    print(DATABASE)
