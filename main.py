from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import SQLModel, Session, select
from auth import create_access_token, get_current_user
from database import engine, get_sesssion
from models import Event, User
from schema import Token
from utils import get_password_hash, verify_password

app = FastAPI()

SQLModel.metadata.create_all(engine)


@app.get("/")
def root_route():
    return {"message": "Welcome to the Calendar API!"}


@app.post("/create_event")
def create_event(event: Event, session: Session = Depends(get_sesssion), user: User = Depends(get_current_user)):
    """Endpoint to create a new event."""
    session.add(event)
    session.commit()
    session.refresh(event)

    return {"message": "Event created successfully", "event": event}


@app.get("/events")
def get_events(session: Session = Depends(get_sesssion)):
    """Endpoint to retrieve all events from database."""
    statement = select(Event)
    events = session.exec(statement).all()

    if not events:
        raise HTTPException(status_code=404, detail="No events found")

    return {"Events": events}


@app.put("/update_event/{id}")
def update_event(id: int, event: Event, session: Session = Depends(get_sesssion), user: User = Depends(get_current_user)):
    """Endpoint to update an existing event."""
    existing_event = session.query(Event).filter(Event.id == id).first()
    if not existing_event:
        raise HTTPException(status_code=404, detail="Event not found")

    existing_event.title = event.title
    existing_event.description = event.description
    session.commit()
    session.refresh(existing_event)

    return {"message": "Event updated successfully",
            "event": existing_event}


@app.get("/event/{id}")
def get_event_byID(id: int, session: Session = Depends(get_sesssion)):
    """Endpoint to retrieve a specific event by ID."""

    event = session.query(Event).filter(Event.id == id).first()
    if not event:
        raise HTTPException(
            status_code=404, detail=f"Event with id {id} not found")

    return event


@app.delete("/delete/{id}")
def delete_event(id: int, session: Session = Depends(get_sesssion)):
    """Endpoint for deleting event"""

    event = session.query(Event).filter(Event.id == id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    session.delete(event)
    session.commit()

    return {"message": "event deleted successfully"}


@app.post("/create_user")
def create_user(user: User, session: Session = Depends(get_sesssion)):
    user.password = get_password_hash(user.password)
    new_user = User(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"Message": "User account created!!", "user_info": new_user.username}


@app.post("/login")
def user_login(user_credentials: User, session: Session = Depends(get_sesssion)):
    user = session.query(User).filter(
        User.username == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid user credentials")

    access = create_access_token(data={"id": user.id})
    return {"Access Token": access, "Token Type": "Bearer"}
