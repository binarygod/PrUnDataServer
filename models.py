from sqlalchemy import Column, String, Integer, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship, backref
from database import Base


def string_to_bool(string_value):
    if string_value == 'TRUE':
        return True
    else:
        return False


class System(Base):
    __tablename__ = 'system'
    id = Column(Integer, primary_key=True, autoincrement=True)
    natural_id = Column(String)
    name = Column(String)
    jmps_prom = Column(Integer)
    jmps_mon = Column(Integer)
    jmps_kat = Column(Integer)


class Planet(Base):
    __tablename__ = 'planet'
    id = Column(Integer, primary_key=True, autoincrement=True)
    natural_id = Column(String)
    name = Column(String)
    system_id = Column(Integer, ForeignKey('system.id'))
    system = relationship(System, backref=backref('planets', uselist=True, cascade='delete,all'))
    fertility = Column(Integer, nullable=True)
    gravity = Column(Float)
    plots = Column(Integer)
    pressure = Column(Float)
    radius = Column(Integer)
    temperature = Column(Integer)
    type = Column(String)
    no_resources = Column(Boolean)
    incomplete = Column(Boolean)
    low_grav = Column(Boolean)
    high_grav = Column(Boolean)
    low_pres = Column(Boolean)
    high_pres = Column(Boolean)
    low_temp = Column(Boolean)
    high_temp = Column(Boolean)
    tier = Column(Integer)


class ResourceCategory(Base):
    __tablename__ = 'resource_category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class Resource(Base):
    __tablename__ = 'resource'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String)
    name = Column(String)
    weight = Column(Float)
    volume = Column(Float)
    is_natural = Column(Boolean)
    category_id = Column(Integer, ForeignKey('resource_category.id'))
    category = relationship(ResourceCategory, backref=backref('resources', uselist=True, cascade='delete,all'))


class ResourceForm(Base):
    __tablename__ = 'resource_form'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class PlanetaryResource(Base):
    __tablename__ = 'planetary_resource'
    id = Column(Integer, primary_key=True, autoincrement=True)
    planet_id = Column(Integer, ForeignKey('planet.id'))
    planet = relationship(Planet, backref=backref('planetary_resources', uselist=True, cascade='delete,all'))
    resource_id = Column(Integer, ForeignKey('resource.id'))
    resource = relationship(Resource, backref=backref('planetary_resources', uselist=True, cascade='delete,all'))
    resource_form_id = Column(Integer, ForeignKey('resource_form.id'))
    resource_form = relationship(ResourceForm,
                                 backref=backref('planetary_resources', uselist=True, cascade='delete,all'))
    concentration = Column(Float)

    def daily_extraction(self):
        if self.resource_form.name == 'Atmospheric':
            return self.concentration * 60
        else:
            return self.concentration * 70
