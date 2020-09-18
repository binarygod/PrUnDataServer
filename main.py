import uvicorn
import json
import models
from database import SessionLocal, engine
from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class ResourceSearch(BaseModel):
    ticker1: str
    ticker2: str


models.Base.metadata.create_all(bind=engine)

# Start the FastAPI
app = FastAPI()
# Setup Cross Origin Scripting to allow requests from Apex
app.add_middleware(CORSMiddleware, allow_origins=['*'])


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Sample Get Method
@app.get("/")
async def root(db: Session = Depends(get_db)):
    planet: models.Planet = db.query(models.Planet).filter(models.Planet.natural_id == 'CR-409e').one()
    return {"message": planet.name}

@app.post("/search/resource")
async def search_resource(search: ResourceSearch, db: Session = Depends(get_db)):
    resource: models.Resource = db.query(models.Resource).filter(models.Resource.ticker == search.ticker1).one()
    results = []

    for planetary_resource in resource.planetary_resources:
        item = {
            'planet_id': planetary_resource.planet.natural_id,
            'ticker': search.ticker1,
            'form': planetary_resource.resource_form.name,
            'concentration': "{:.2f}%".format((planetary_resource.concentration * 100)),
            'extraction': "{:.2f}".format(planetary_resource.daily_extraction()),
            'dist_hortus': planetary_resource.planet.system.jmps_prom,
            'dist_moria': planetary_resource.planet.system.jmps_mon,
            'dist_benten': planetary_resource.planet.system.jmps_kat,
            'type': planetary_resource.planet.type,
            'no_resources': planetary_resource.planet.no_resources,
            'grav': 'Normal',
            'pres': 'Normal',
            'temp': 'Normal',
            'tier': planetary_resource.planet.tier
        }

        if planetary_resource.planet.low_grav == True:
            item['grav'] = 'Low'
        elif planetary_resource.planet.high_grav == True:
            item['grav'] = 'High'

        if planetary_resource.planet.low_pres == True:
            item['pres'] = 'Low'
        elif planetary_resource.planet.high_pres == True:
            item['pres'] = 'High'

        if planetary_resource.planet.low_temp == True:
            item['temp'] = 'Low'
        elif planetary_resource.planet.high_temp == True:
            item['temp'] = 'High'

        results.append(item)
    return JSONResponse(content=results)

@app.get("/lists/resources")
async def list_resources(db: Session = Depends(get_db)):
    resources = db.query(models.Resource).filter(models.Resource.is_natural == True).order_by(models.Resource.ticker.asc())
    results = []

    for resource in resources:
        results.append(resource.ticker)

    return JSONResponse(results)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
