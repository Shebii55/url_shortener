from fastapi import FastAPI, HTTPException, Depends, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
import crud, models, database

app = FastAPI()

# Initialize the Jinja2 template engine
templates = Jinja2Templates(directory="templates")

# Create all tables
models.Base.metadata.create_all(bind=database.engine)

# Post request to shorten URL
@app.post("/urls/", response_class=HTMLResponse)
async def create_url(request: Request, db: Session = Depends(database.get_db), url: str = Form(...)):
    db_url = crud.create_url(db=db, target_url=url)
    # Dynamically generate the full URL
    full_short_url = f"{request.base_url}{db_url.short_url}"
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "short_url": db_url.short_url,
            "original_url": url,
            "full_short_url": full_short_url,
        },
    )

# Get request to redirect to the target URL
@app.get("/{short_url}")
def forward_to_target(short_url: str, db: Session = Depends(database.get_db)):
    db_url = crud.get_short_url(db, short_url)
    if db_url is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(db_url.target_url)

# Root request that renders the HTML template
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
