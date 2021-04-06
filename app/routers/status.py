from sqlalchemy.orm import Session
from app.dependency import get_db
from app import models
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from app import settings

router = APIRouter()


# Test accessing the database for a specific known record
@router.get("/")
async def root(db: Session = Depends(get_db)):
    planet: models.Planet = db.query(models.Planet).filter(models.Planet.natural_id == 'CR-409e').one()
    if planet.name == 'Promitor':
        return {
            'db_status': 'connected',
            'api_status': 'online',
            'message': f'See {settings.BASE_URL}/docs or {settings.BASE_URL}/redoc for API Documentation'
        }
    return {"message": 'Something is wrong...'}