from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from src.config import settings

# Constructing the database URL based on the database type
if settings.database_type == 'sqlite':
    DATABASE_URL = f"{settings.database_type}:///./{settings.database_name}.db"
elif settings.database_type == 'postgresql':
    DATABASE_URL = f"{settings.database_type}://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"
elif settings.database_type == 'bigquery':
    raise ValueError("BigQuery is not supported as a database for SQLAlchemy.")

# Creating the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={
    "check_same_thread": False
    # ,"foreign_keys": "ON" if settings.database_type == 'sqlite' else {}
    },execution_options={"sqlite_pragma_foreign_keys": True} if settings.database_type == 'sqlite' else {})

# Creating a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()