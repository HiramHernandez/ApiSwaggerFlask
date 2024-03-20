from pymysql import Date
from sqlalchemy import (
    Column,
    Integer,
    VARCHAR,
    DATE
)
from ..config.extensions import db


class Device(db.Model):
    __tablename__ = 'dispositivos'
    __table_args__ = {'implicit_returning': False}
    id = Column(Integer, primary_key=True, nullable=False)
    nombre = Column(VARCHAR(length=100))
    potencia = Column(Integer)
    estatus_dispositivo_id = Column(Integer)
    tipo_dispositivo_id = Column(Integer)
    fecha_alta = Column(DATE)
    fecha_actualizacion = Column(DATE)


class DeviceType(db.Model):
    __tablename__ = 'tipo_dispositivos'
    __table_args__ = {'implicit_returning': False}
    id = Column(Integer, primary_key=True, nullable=False)
    nombre_tipo_dispositivo = Column(VARCHAR(length=100))


class DeviceStatus(db.Model):
    __tablename__ = 'status_dispositivos'
    __table_args__ = {'implicit_returning': False}
    id = Column(Integer, primary_key=True, nullable=False)
    descripcion = Column(VARCHAR(length=100))


class Records(db.Model):
    __tablename__ = 'lecturas'
    __table_args__ = {'implicit_returning': False}
    id = Column(Integer, primary_key=True, nullable=False)
    dispositivo_id = Column(Integer)
    tipo_dispositivo_id = Column(Integer)
    potencia_actual = Column(Integer)
    timestamp = Column(DATE)


class Maintenance(db.Model):
    __tablename__ = 'mantenimientos'
    __table_args__ = {'implicit_returning': False}
    id = Column(Integer, primary_key=True, nullable=False)
    dispositivo_id = Column(Integer)
    fecha_ingreso = Column(DATE)
