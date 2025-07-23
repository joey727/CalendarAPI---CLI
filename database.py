from sqlmodel import SQLModel, create_engine, Session

sq_lite = 'data.db'

engine = create_engine(f'sqlite:///{sq_lite}', echo=True)


def get_sesssion():
    """Create a new sessioin for database operations."""

    with Session(engine) as session:
        yield session
