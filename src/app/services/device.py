from datetime import datetime
from sqlalchemy.sql import func
from ..config.extensions import db
from ..models.device import Device, Records, Maintenance


class DeviceService:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def fetch(self):
        try:
            return  db.session.query(Device).all()
        except  Exception as e:
            return None
    
    def fetch_by_type(self, type_id):
        try:
            return db.session.query(Device)\
                .filter(Device.tipo_dispositivo_id == type_id ).all()
        except Exception as e:
            return None
    
    def retrieve(self, id):
        try:
           return db.session.query(Device).filter(Device.id == id).first()   
        except Exception as e:
            return None

    def create(self, data):
        try:
            new_device = Device(
                nombre = data['nombre'],
                potencia = data['potencia'],
                estatus_dispositivo_id = data['estatus_dispositivo_id'],
                tipo_dispositivo_id = data['tipo_dispositivo_id'],
                fecha_alta = datetime.now()
            )
            db.session.add(new_device)
            db.session.commit()
            return new_device
        except Exception as e:
            return None

    def update(self, device_id, data):
        try:
            db.session.query(Device).filter(Device.id == device_id).update(
                {
                    'nombre': data['nombre'],
                    'potencia': data['potencia'],
                    'estatus_dispositivo_id': data['estatus_dispositivo_id'],
                    'tipo_dispositivo_id': data['tipo_dispositivo_id'],
                    'fecha_actualizacion': datetime.now()
                }
                ,synchronize_session=False)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def delete(self, device_id):
        try:
            Device.query.filter(Device.id == device_id).delete()
            db.session.commit()
            return True
        except:
            return False
        
    def device_is_in_maintence(self, id):
        device = Device.query\
                .filter(
                    Device.id == id,
                    Device.estatus_dispositivo_id == 2
                ).first()
        return True if device else False


class RecordService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def fetch(self):
        try:           
            return db.session.query(Records).all()
        except Exception as e:
            return None

    def fetch_by_type(self, type_id):
        try:
            return db.session.query(Records)\
                .filter(Records.tipo_dispositivo_id == type_id) \
                .all()
        except Exception as e:
            return None

    def fetch_by_device(self, device_id):
        try:
            return db.session.query(Records)\
                .filter(Records.dispositivo_id == device_id) \
                .all()
        except Exception as e:
            return None

    def retrieve(self, id):
        try:
            return db.session.query(Records) \
                .filter(Records.id == id) \
                .first()
        except Exception as e:
            return None

    def create(self, data):
        try:
            '''device = Device.query\
                .filter(
                    Device.id == data['dispositivo_id'],
                    Device.estatus_dispositivo_id == 2
                ).first()'''
            '''if device:
                return False'''
            new_record = Records(
                tipo_dispositivo_id = data['tipo_dispositivo_id'],
                potencia_actual = data['potencia_actual'],
                dispositivo_id = data['dispositivo_id'],
                timestamp = datetime.now()
            )
            db.session.add(new_record)
            db.session.commit()
            return new_record
        except Exception as e:
            return None

    def update(self, record_id, data):
        try:
            db.session.query(Records).filter(Records.id == record_id).update(
                {
                    'tipo_dispositivo_id': data['tipo_dispositivo_id'],
                    'potencia_actual': data['potencia_actual'],
                    'dispositivo_id': data['dispositivo_id'],
                }
                ,synchronize_session=False)
            db.session.commit()
            # Update device power
            db.session.query(Device).filter(Device.id == data['dispositivo_id']).update(
                {
                    'potencia': data['potencia_actual'],
                    'fecha_actualizacion': datetime.now()
                }
                ,synchronize_session=False)
            db.session.commit()
            #record_updated = db.session.query(Records).filter(Records.id == record_id).first()
            return True #record_schema.dump(record_updated)

        except Exception as e:
            return False

    def delete(self, record_id):
        try:
            #record_schema = RecordSchema()
            record = Records.query.filter(Records.id == record_id).first()
            '''if record:
                
                return record_schema.dump(record)'''
            Records.query.filter(Records.id == record_id).delete()
            db.session.commit()
            return True
        except:
            return False

    def total_energy(self):
        try:
            #energy_schema = EnergySchema(many=True)
           return db.session\
                .query(
                    Records.dispositivo_id,
                    func.sum(Records.potencia_actual).label('energia')
                )\
                .group_by(Records.dispositivo_id)\
                .all()
        except Exception as e:
            return None


class MaintenanceService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def fetch(self):
        try:
            #maintenance_devices_schema = MaintenanceSchema(many=True)
            return db.session.query(Maintenance).all()
        except Exception as e:
            return None

    def create(self, data):
        try:
            #maintenance_devices_schema = MaintenanceSchema()
            new_maintenance_device = Maintenance(
                dispositivo_id = data['dispositivo_id'],
                fecha_ingreso = datetime.now()
            )
            db.session.add(new_maintenance_device)
            db.session.commit()
            # Device status changed to in maintenance
            DEVICE_IN_MAINTENANCE = 2
            db.session.query(Device).filter(Device.id == data['dispositivo_id']).update(
                {
                    'estatus_dispositivo_id': DEVICE_IN_MAINTENANCE
                }
                ,synchronize_session=False)
            db.session.commit()
            return new_maintenance_device
        except Exception as e:
            return None

    def retrieve(self, device_id):
        try:
            #maintenance_devices_schema = MaintenanceSchema()
            return db.session.query(Maintenance)\
                .filter(Maintenance.dispositivo_id == device_id)\
                .first()
        except Exception as e:
            return None