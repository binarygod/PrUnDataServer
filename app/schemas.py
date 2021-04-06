from typing import List, Optional
from pydantic import BaseModel


class ORMBase(BaseModel):
    id: int

    class Config:
        orm_mode = True


class System(ORMBase):
    natural_id: str
    name: str
    jmps_prom: int
    jmps_mon: int
    jmps_kat: int


class Planet(ORMBase):
    natural_id: str
    name: str
    system_id: int
    fertility: int
    gravity: float
    plots: int
    pressure: float
    radius: int
    temperature: int
    type: str
    no_resources: bool
    incomplete: bool
    low_grav: bool
    high_grav: bool
    low_pres: bool
    high_pres: bool
    low_temp: bool
    high_temp: bool
    tier: int
