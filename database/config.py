from sqlmodel import SQLModel, create_engine


SQLALCHEMY_DATABASE_URL = "sqlite:///./db.sqlite3"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


def create_db():
    SQLModel.metadata.create_all(engine)
