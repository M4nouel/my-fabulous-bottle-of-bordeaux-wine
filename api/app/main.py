import pickle
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from fastapi.openapi.utils import get_openapi
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.staticfiles import StaticFiles

from . import crud, models, schemas, recommender
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(docs_url=None, redoc_url=None, root_path="/api")
app.mount("/static", StaticFiles(directory="static"), name="static")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

KNN = pickle.load(open('./app/knn_model.sav', 'rb'))


# Routes
@app.get("/wines/kneighbors", response_model=List[schemas.Wine])
def read_kneighbors_of_wine(name: str,
                            millesime: str,
                            count: int,
                            db: Session = Depends(get_db)):
    if count < 1 or count > 10:
        raise HTTPException(status_code=403, detail="Count must be between 1 and 10")

    chosen_wine = crud.get_wine_by_name_and_millesime(db, name, millesime)
    if chosen_wine is None:
        raise HTTPException(status_code=404, detail="Wine named {}, millesime {} not found".format(name, millesime))

    wines = recommender.kneighbors_of_wine_by_id(db, KNN, chosen_wine.id, count)
    return wines

@app.get("/wines/kneighbors/id/{wine_id}", response_model=List[schemas.Wine])
def read_kneighbors_of_wine_by_id(wine_id: int, limit: int = 10, db: Session = Depends(get_db)):
    wines = recommender.kneighbors_of_wine_by_id(db, KNN, wine_id, limit)
    return wines

@app.get("/wines/search", response_model=schemas.SearchedWines)
def search_wines(name: str,
                millesime: str = "",
                skip: int = 0,
                count: int = 10,
                db: Session = Depends(get_db)):
    wines = crud.get_wines_like_name_and_millesime(db, name, millesime, skip, count)
    return wines


# Dummy
@app.get("/wine/{wine_id}/", response_model=schemas.Wine)
def read_wine(wine_id: int, db: Session = Depends(get_db)):
    wine = crud.get_wine_by_id(db, wine_id=wine_id)
    return wine

@app.get("/test/wines/", response_model=List[schemas.Wine])
def read_wines(db: Session = Depends(get_db)):
    wines = crud.get_ten_wines(db)
    return wines


# OPEN API
# def custom_openapi():
#     if app.openapi_schema:
#         return app.openapi_schema
#     openapi_schema = get_openapi(
#         title="Bordeaux Wines",
#         version="0.0.3",
#         description="This is an API-zed ML model that seggests Bordeaux Wines",
#         routes=app.routes,
#     )
#     openapi_schema["info"]["x-logo"] = {
#         "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
#     }
#     app.openapi_schema = openapi_schema
#     return app.openapi_schema

# app.openapi = custom_openapi

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/api/openapi.json",
        title=app.title + " - Swagger UI",
        swagger_js_url="/api/static/swagger-ui-bundle.js",
        swagger_css_url="/api/static/swagger-ui.css",
    )

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url="/api/openapi.json",
        title=app.title + " - ReDoc",
        redoc_js_url="/api/static/redoc.standalone.js",
    )