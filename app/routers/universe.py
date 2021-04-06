from sqlalchemy.orm import Session
from app.dependency import get_db
from app import models
from fastapi import Depends, Query, Path
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from typing import List
from app import schemas

router = APIRouter()


@router.post("/search/resource", tags=['items'])
async def search_resource(search: models.ResourceSearch, db: Session = Depends(get_db)):
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


@router.get("/lists/resources")
async def list_resources(db: Session = Depends(get_db)):
    resources = db.query(models.Resource).filter(models.Resource.is_natural == True).order_by(
        models.Resource.ticker.asc())
    results = []

    for resource in resources:
        results.append(resource.ticker)

    return JSONResponse(results)


@router.get('/systems', tags=['universe'], response_model=List[schemas.System],
            response_description='List of Systems in Universe')
async def systems(db: Session = Depends(get_db)):
    results = db.query(models.System).all()
    return results


@router.get('/system/{natural_id}', tags=['universe'], response_model=schemas.System)
async def system(natural_id: str = Path(None, description='Natural ID of the system.', example='CR-409'), db: Session = Depends(get_db)):
    return db.query(models.System).filter(models.System.natural_id == natural_id).first()


@router.get('/system/{natural_id}/planets', tags=['universe'], response_model=List[schemas.Planet])
async def planets(natural_id: str, db: Session = Depends(get_db)):
    system = db.query(models.System).filter(models.System.natural_id == natural_id).first()
    results = db.query(models.Planet).filter(models.Planet.system_id == system.id).all()
    return results
