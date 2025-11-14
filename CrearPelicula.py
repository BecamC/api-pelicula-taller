import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    # Entrada (json)
    try:
        # Log con información
        log_info = {
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Inicio de la ejecución.",
                "event": event
            }
        }
        print(json.dumps(log_info))  # Imprimir log en formato JSON
        
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]

        # Proceso
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)
        
        # Salida (json) con éxito
        log_info = {
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Operación exitosa",
                "pelicula": pelicula,
                "response": response
            }
        }
        print(json.dumps(log_info))  # Log de éxito en formato JSON
        
        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }
    
    except Exception as e:
        # Log con error
        log_error = {
            "tipo": "ERROR",
            "log_datos": {
                "mensaje": "Error en la ejecución.",
                "error": str(e)
            }
        }
        print(json.dumps(log_error))  # Log de error en formato JSON
        
        return {
            'statusCode': 500,
            'mensaje': 'Error en la creación de la película',
            'error': str(e)
        }
