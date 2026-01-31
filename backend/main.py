from fastapi import FastAPI, Request, Depends, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import engine, SessionLocal
from .models import Base, User, Incident, IncidentTimeline, Session as DBSession
from .seed import seed
from .auth import (
    get_db,
    get_current_user,
    verify_password,
    create_session
)
from .search import search_incidents

# -------------------------------------------------
# APP INIT
# -------------------------------------------------

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# -------------------------------------------------
# STARTUP: SEED DATA
# -------------------------------------------------

@app.on_event("startup")
def startup():
    db = SessionLocal()
    seed(db)
    db.close()

# -------------------------------------------------
# AUTH
# -------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter_by(username=username, active=True).first()
    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            "error.html",
            {"request": {}, "message": "Invalid credentials"},
            status_code=401,
        )

    session_id = create_session(db, user.id)
    response = RedirectResponse("/dashboard", status_code=302)
    response.set_cookie("SESSION_ID", session_id, httponly=True)
    return response


@app.post("/logout")
def logout(request: Request, db: Session = Depends(get_db)):
    sid = request.cookies.get("SESSION_ID")
    if sid:
        db.query(DBSession).filter_by(id=sid).delete()
        db.commit()

    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("SESSION_ID")
    return response

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    request: Request,
    user: User = Depends(get_current_user)
):
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user}
    )

# -------------------------------------------------
# INCIDENT LIST + SEARCH PAGE
# -------------------------------------------------

@app.get("/incidents", response_class=HTMLResponse)
def incidents_page(
    request: Request,
    severity: str | None = None,
    status: str | None = None,
    service_name: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    incidents = search_incidents(
        db,
        severity=severity,
        status=status,
        service_name=service_name
    )

    return templates.TemplateResponse(
        "incidents.html",
        {
            "request": request,
            "incidents": incidents,
            "user": user
        }
    )

# -------------------------------------------------
# INCIDENT DETAIL PAGE
# -------------------------------------------------

@app.get("/incidents/{incident_id}", response_class=HTMLResponse)
def incident_detail(
    incident_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    incident = db.query(Incident).get(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    timeline = (
        db.query(IncidentTimeline)
        .filter_by(incident_id=incident_id)
        .order_by(IncidentTimeline.timestamp.asc())
        .all()
    )

    return templates.TemplateResponse(
        "incident_detail.html",
        {
            "request": request,
            "incident": incident,
            "timeline": timeline,
            "user": user
        }
    )

# -------------------------------------------------
# SEARCH API (JSON – OPTIONAL, USED BY AI LATER)
# -------------------------------------------------

@app.get("/api/incidents/search")
def search_incidents_api(
    severity: str | None = None,
    status: str | None = None,
    service_name: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return search_incidents(
        db,
        severity=severity,
        status=status,
        service_name=service_name
    )
