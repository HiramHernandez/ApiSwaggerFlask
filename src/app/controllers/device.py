from flask_restx import Resource, reqparse, Namespace, fields
from flask import request
from ..services.device import DeviceService, RecordService, MaintenanceService
from ..schemas.device import (
    DeviceSchema, 
    RecordSchema, 
    EnergySchema, 
    MaintenanceSchema
)
api = Namespace('Dispositivos y Registros', description='Endpoints para mostrar información sobre dispositivos y registros')


class DeviceListController(Resource):
    device_service = DeviceService()
    parser_device = reqparse.RequestParser()
    parser_device.add_argument('device_type_id', type=int, help='Buscar por ID Tipo Dispositivo')
    devices_schema = DeviceSchema(many=True)
    device_schema = DeviceSchema()

    @api.doc(parser=parser_device)
    def get(self):
        if request.args.get("device_type_id"):
            devices = self.device_service.fetch_by_type(request.args.get("device_type_id"))
           
            return {'dispositivos': devices, 'status': 'Ok'}
        devices = self.device_service.fetch()
        if devices:
            return {'dispositivos': self.devices_schema.dump(devices), 'status': 'Ok'}
        return {
            'dispositivos': [] , 
            'status': 'Error al obtener todos los dispositivos'
        }, 404

    def post(self):
        data = request.json
        new_device = self.device_service.create(data)

        if not new_device:
            return {
                'dispositivo': {} , 
                'status': 'Error al guardar el dispositivo'
            }, 404
        return {'dispositivo': self.device_schema.dump(new_device), 'status': 'Creado con exito'}, 201
         


class DeviceController(Resource):
    device_service = DeviceService()
    device_schema = DeviceSchema()

    def get(self, id):
        device = self.device_service.retrieve(id)
        if not device:
            return {
                'dispositivos': {} , 
                'status': 'No se encontro un dispositivo con el id proporcionado'
            }, 404
        
        return {'dispositivo': self.device_schema.dump(device), 'status': 'Ok'}
        

    def put(self, id):
        data = request.json
        if not self.device_service.retrieve(id):
            return {
            'dispositivo': {} , 
            'status': 'Lo sentimos no se encontró dispositivo'
        }, 404
        device = self.device_service.update(id, data)

        if not device:
             return {
                'dispositivo': {} , 
                'status': 'Error al actualizar el dispositivo'
            }, 404
        device_founded = self.device_service.retrieve(id)
        return {'dispositivo': self.device_schema.dump(device_founded), 'status': 'Actualizado con exito'}
       

    def delete(self, id):
        if not self.device_service.retrieve(id):
            return {
            'dispositivo': {} , 
            'status': 'Lo sentimos no se encontró dispositivo'
        }, 404
        device_founded = self.device_service.retrieve(id)
        device = self.device_service.delete(id)
        if not device:
              return {
                'dispositivo': {} , 
                'status': 'Error al eliminar el dispositivo'
                }, 404
        return {'dispositivo': self.device_schema.dump(device_founded), 'status': 'Eliminado con exito'}


class RecordListController(Resource):
    record_service = RecordService()
    device_service = DeviceService()
    parser_record = reqparse.RequestParser()
    parser_record.add_argument('device_type_id', type=int, help='Buscar por ID Tipo Dispositivo')
    parser_record.add_argument('device_id', type=int, help='Buscar por ID Dispositivo')
    record_schema = RecordSchema()
    records_schema = RecordSchema(many=True)


    @api.doc(parser=parser_record)
    def get(self):
        if request.args.get("device_type_id"):
            records = self.record_service.fetch_by_type(request.args.get("device_type_id"))
            return {'registros': self.records_schema.dump(records), 'status': 'Ok'}
        if request.args.get("device_id"):
            records = self.record_service.fetch_by_device(request.args.get("device_id"))
            return {'registros': self.records_schema.dump(records), 'status': 'Ok'}
        records = self.record_service.fetch()
        if not records:
            return {
                'registros': {} , 
                'status': 'Error al obtener todos los registros'
            }, 404
        return {'registros': records, 'status': 'Ok'}
       
    def post(self):
        data = request.json
        if self.device_service.device_is_in_maintence(data["dispositivo_id"]):
            return {
                'registro': {}, 
                'status': 'No se permite registros ya que el dispositivo esta en mantenimiento'
            }, 404
        new_record = self.record_service.create(data)
      
        if not new_record:
            return {
                'dispositivo': {} , 
                'status': 'Error al guardar el registro'
            }, 404
        return {'registro': self.record_schema.dump(new_record), 'status': 'Creado con exito'}, 201
        

class RecordController(Resource):
    record_service = RecordService()
    record_schema = RecordSchema()
    
    def get(self, id):
        record = self.record_service.retrieve(id)
        if not record:
            {
                'Registro': {} , 
                'status': 'No se encontro registro con el id proporcionado'
            }, 404
        return {'registro': self.record_schema.dump(record), 'status': 'Ok'}
        

    def put(self, id):
        data = request.json
        record = self.record_service.update(id, data)
        if not record:
            return {
                'registro': {} , 
                'status': 'Error al actualizar el registro'
            }, 404
        record_founded = self.record_service.retrieve(id)
        return {'registro': self.record_schema.dump(record_founded), 'status': 'Actualizado con exito'}
       

    def delete(self, id):
        record_founded = self.record_service.retrieve(id)
        if not record_founded:
            return {'registro': {}, 'status': 'El id ingresado no existe'}
        record = self.record_service.delete(id)
        if not record:
            return {
                'registro': {} , 
                'status': 'Error al eliminar el registro'
            }, 404
        return {'registro': self.record_schema.dump(record_founded), 'status': 'Eliminado con exito'} 
            
      
class TotalEnergyController(Resource):
    record_service = RecordService()
    energy_schema = EnergySchema()

    def get(self):
        energy = self.record_service.total_energy()
        if not energy:
            return {
                'Registro': {} , 
                'status': 'No se encontraron registros de energia'
            }, 404
        return {'energia': self.energy_schema.dump(energy), 'status': 'Ok'}


class MaintenanceListController(Resource):
    maintenance_service = MaintenanceService()
    maintances_schema = MaintenanceSchema(many=True)
    maintance_schema = MaintenanceSchema()

    def get(self):
        maintenance_devices = self.maintenance_service.fetch()
        if maintenance_devices:
            return {
                'registros': {} , 
                'status': 'Error al obtener todos los dispositivos en mantenimiento'
            }, 404
        return {'dispositivos': self.maintances_schema.dump(maintenance_devices), 'status': 'Ok'}
        

    def post(self):
        data = request.json
        new_maintenance_device = self.maintenance_service.create(data)
        if not new_maintenance_device:
            return {
                'dispositivo': {} , 
                'status': 'Error al guardar el dispositivo en mantenimiento'
            }, 404
        return {'dispositivo': self.maintance_schema.dump(new_maintenance_device), 'status': 'Creado con exito'}, 201
        


class MaintenanceController(Resource):
    maintenance_service = MaintenanceService()
    maintance_schema = MaintenanceSchema()

    def get(self, device_id):
        maintenance_device = self.maintenance_service.retrieve(device_id)
        if not maintenance_device:
            return {
                'registros': {} , 
                'status': 'No se encontraron dispositivos en mantenimiento con el id ingresado'
            }, 404
        return {'dispositivo': self.maintance_schema.dump(maintenance_device), 'status': 'Ok'}
