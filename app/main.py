from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles 
from app import models
from app.database import engine
from app.routers import post, users, vote
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# CORS settings
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Templates setup
templates = Jinja2Templates(directory="templates")

# Static files setup
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(post.router)
app.include_router(users.router)
app.include_router(vote.router)


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello, {name.capitalize()}"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)