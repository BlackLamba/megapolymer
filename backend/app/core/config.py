import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:ftk.kill@localhost:5432/polymer_db"
)