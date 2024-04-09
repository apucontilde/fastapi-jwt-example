import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.getenv("DATABASE_URL", "")

JWT_SECRET: str = os.getenv(
    "JWT_SECRET", "a361da88e888b8f5dda220354bb2d898a43160fab3278141"
)
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
JWT_DURATION_SECS: float = os.getenv("JWT_DURATION_SECS", 600)
