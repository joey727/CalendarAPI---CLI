from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from database import engine, get_sesssion
from models import Event

app = FastAPI()

SQLModel.metadata.create_all(engine)


@app.get("/")
def root_route():
    return {"message": "Welcome to the Calendar API!"}


@app.post("/create_event")
def create_event(event: Event, session: Session = Depends(get_sesssion)):
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
def update_event(id: int, event: Event, session: Session = Depends(get_sesssion)):
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
