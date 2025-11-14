import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    try:
        # Entrada (json)
        # Log del evento de entrada en formato estándar (INFO)
        log_info = {
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Evento de entrada",
                "evento": event
            }
        }
        print(json.dumps(log_info))

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

        # Log de la película creada (éxito) en formato estándar (INFO)
        log_info = {
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Película creada exitosamente",
                "pelicula": pelicula,
                "response": response
            }
        }
        print(json.dumps(log_info))

        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }

    except Exception as e:
        # Log del error en formato estándar (ERROR)
        log_error = {
            "tipo": "ERROR",
            "log_datos": {
                "mensaje": "Error al crear la película",
                "error": str(e),
                "evento": event
            }
        }
        print(json.dumps(log_error))

        return {
            'statusCode': 500,
            'error': str(e)
        }
