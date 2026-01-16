from fastapi import Depends, FastAPI
from src.db.database import engine,get_db
from src.routers.articles import articles
from src.routers.users import user
from src.db import models
from src.utils.auth_service import authentication
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    dependencies=[Depends(get_db)]
)

app.include_router(articles.router)
app.include_router(user.router)
app.include_router(authentication.router)

@app.get("/")
def root():
    """
    Root endpoint for the social media application.
    """
    return {"message": "Welcome to the FastAPI social media application!"}

models.Base.metadata.create_all(engine)

app.mount("/images", StaticFiles(directory="images"), name="images")