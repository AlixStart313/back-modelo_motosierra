import json
import pymysql

# Configuración de la conexión a la base de datos
rds_host = "database-cafe-balu.cziym6ii4nn7.us-east-2.rds.amazonaws.com"
rds_user = "baluroot"
rds_password = "baluroot"
rds_db = "MotosierraDB"

def lambda_handler(event, __):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token"
    }

    if event['httpMethod'] == 'OPTIONS':
        return {
            "statusCode": 200,
            "headers": headers
        }

    try:
        if 'pathParameters' not in event or 'id' not in event['pathParameters']:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({
                    "message": "MISSING_ITEM_ID"
                }),
            }

        id = event['pathParameters']['id']

        if int(id) <= 0:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({
                    "message": "INVALID_MOTOSIERRA_ID"
                }),
            }

        if not motosierra_exists(id):
            return {
                "statusCode": 404,
                "headers": headers,
                "body": json.dumps({
                    "message": "MOTOSIERRA_NOT_FOUND"
                }),
            }

        if delete_motosierra(id):
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({
                    "message": "MOTOSIERRA_DELETED"
                }),
            }
        else:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({
                    "message": "MOTOSIERRA_NOT_DELETED"
                }),
            }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({
                "message": "INTERNAL_SERVER_ERROR",
                "error": str(e)
            }),
        }

def connect_to_database():
    try:
        connection = pymysql.connect(host=rds_host, user=rds_user, password=rds_password, db=rds_db)
        return connection
    except pymysql.MySQLError as e:
        raise Exception("ERROR CONNECTING TO DATABASE: " + str(e))

def motosierra_exists(id):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("select * from Motosierras where id = %s", (id,))
    result = cursor.fetchone()
    connection.close()
    return result is not None

def delete_motosierra(id):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("delete from Motosierras where id = %s", (id,))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        return False