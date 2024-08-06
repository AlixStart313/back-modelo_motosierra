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
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token"
    }

    try:
        body = json.loads(event.get('body', '{}'))

        if not 'brand' in body or not 'model' in body or not 'power' in body or not 'weigth' in body or not 'id' in body:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({
                    "message": "MISSING_FIELDS",
                }),
            }

        id = body.get('id')
        brand = body.get('brand')
        model = body.get('model')
        power = body.get('power')
        weigth = body.get('weigth')

        if not brand or not model or not power or not weigth or not id:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({
                    "message": "MISSING_FIELDS",
                }),
            }

        if int(id) <= 0:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({
                    "message": "INVALID_ID",
                }),
            }

        if not power.isdigit() or int(power) > 2024:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({
                    "message": "INVALID_POWER",
                }),
            }

        if not motosierra_exists(id):
            return {
                "statusCode": 404,
                "headers": headers,
                "body": json.dumps({
                    "message": "ITEM_NOT_FOUND",
                }),
            }

        if update_motosierra(id, brand, model, power, weigth):
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({
                    "message": "ITEM_UPDATED",
                }),
            }
        else:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({
                    "message": "ITEM_NOT_UPDATED",
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

def update_motosierra (id, brand, model, power, weigth):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("UPDATE Motosierras SET brand = %s, model = %s, power = %s, weigth = %s WHERE id = %s", (brand, model, power, weigth, id))
        connection.commit()
        connection.close()
        return True
    except Exception as e:
        return False