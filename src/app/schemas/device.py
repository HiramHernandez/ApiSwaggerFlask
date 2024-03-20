from sqlalchemy import DATE
from marshmallow import fields
from ..config.extensions import ma
from ..models.device import Device, Records, Maintenance


class DeviceSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Device

    id = ma.auto_field()
    nombre = ma.auto_field()
    potencia = ma.auto_field()
    estatus_dispositivo_id = ma.auto_field()
    tipo_dispositivo_id = ma.auto_field()
    fecha_alta = fields.Str()
    fecha_actualizacion = fields.Str()


class RecordSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Records
    
    id = ma.auto_field()
    dispositivo_id = ma.auto_field()
    tipo_dispositivo_id = ma.auto_field()
    potencia_actual = ma.auto_field()
    timestamp = fields.Str()


class EnergySchema(ma.SQLAlchemySchema):
    class Meta:
        model = Records

    dispositivo_id = ma.auto_field()
    energia = fields.Integer()


class MaintenanceSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Maintenance

    id = ma.auto_field()
    dispositivo_id = ma.auto_field()
    fecha_ingreso = fields.Str()
