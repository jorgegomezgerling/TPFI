import boto3
from botocore.exceptions import BotoCoreError, ClientError
import logging
import json
from SingletonMeta import SingletonMeta

class CorporateData(metaclass=SingletonMeta):
    """Clase que maneja los datos corporativos con implementación Singleton."""
    
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table('CorporateData')
    
    @staticmethod
    def getInstance():
        """Método estático para obtener la instancia única de CorporateData."""
        return CorporateData()

    def getData(self, uuid, uuidCPU, id):
        """
        Retorna información de la sede.
        
        Parámetros:
        - uuid: Identificador de sesión.
        - uuidCPU: Identificador de CPU.
        - id: Identificador de la sede.
        
        Retorna:
        - JSON con los datos de la sede o un mensaje de error.
        """
        logging.debug(f"getData: Buscando datos para ID de sede {id} con session ID {uuid} y CPU ID {uuidCPU}")
        try:
            response = self.table.get_item(Key={'id': id})
            if 'Item' in response:
                return {
                    "ID": response['Item'].get("id"),
                    "Domicilio": response['Item'].get("domicilio"),
                    "Localidad": response['Item'].get("localidad"),
                    "CodigoPostal": response['Item'].get("cp"),
                    "Provincia": response['Item'].get("provincia")
                }
            else:
                return {"error": "Registro no encontrado"}
        except Exception as e:
            logging.error(f"Error en getData: {e}")
            return {"error": f"Error al acceder a la base de datos: {e}"}

    def getCUIT(self, uuid, uuidCPU, id):
        """
        Retorna el CUIT de la sede.
        
        Parámetros:
        - uuid: Identificador de sesión.
        - uuidCPU: Identificador de CPU.
        - id: Identificador de la sede.
        
        Retorna:
        - JSON con el CUIT o un mensaje de error.
        """
        try:
            response = self.table.get_item(Key={'id': id})
            if 'Item' in response:
                return {"CUIT": response['Item'].get("CUIT")}
            else:
                return {"error": "Registro no encontrado"}
        except (BotoCoreError, ClientError) as error:
            return {"error": f"Error al acceder a la base de datos: {error}"}

    def getSeqID(self, uuid, uuidCPU, id):
        """
        Retorna un identificador de secuencia único y lo incrementa en la base de datos.
        
        Parámetros:
        - uuid: Identificador de sesión.
        - uuidCPU: Identificador de CPU.
        - id: Identificador de la sede.
        
        Retorna:
        - JSON con el identificador de secuencia o un mensaje de error.
        """
        try:
            response = self.table.get_item(Key={'id': id})
            if 'Item' in response:
                idSeq = response['Item'].get("idreq", 0) + 1
                self.table.update_item(
                    Key={'id': id},
                    UpdateExpression="set idreq = :val",
                    ExpressionAttributeValues={':val': idSeq}
                )
                return {"idSeq": idSeq}
            else:
                return {"error": "Registro no encontrado"}
        except (BotoCoreError, ClientError) as error:
            return {"error": f"Error al acceder a la base de datos: {error}"}
