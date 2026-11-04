from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL= "sqlite:///./users.db"
#below for postgresql
# DATABASE_URL= "postgresql://fastapi_login_user:root@localhost:5432/telugupy_fastapi"
engine = create_engine(DATABASE_URL, echo=True)


def create_tables_database():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
