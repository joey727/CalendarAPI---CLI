from sqlmodel import create_engine, Session

sq_lite = 'events_data.db'

engine = create_engine(f'sqlite:///{sq_lite}', echo=True)


def get_sesssion():
    """Create a new session for database operations."""
    try:
        session = Session(engine)
        yield session
    finally:
        session.close()
