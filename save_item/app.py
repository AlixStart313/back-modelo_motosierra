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
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type, X-Amz-Date, Authorization, X-Api-Key, X-Amz-Security-Token"
    }

    try:
        body = json.loads(event.get('body', '{}'))

        if not 'brand' in body or not 'model' in body or not 'year' in body or not 'color' in body:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({
                    "message": "MISSING_FIELDS",
                }),
            }

        brand = body.get('brand')
        model = body.get('model')
        power = body.get('year')
        weigth = body.get('color')

        if not brand or not model or not power or not weigth:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({
                    "message": "MISSING_FIELDS",
                }),
            }

        if not power.isdigit() or int(power) > 2024:
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({
                    "message": "INVALID_POWER"
                }),
            }

        if motosierra(brand, model, power, weigth):
            return {
                "statusCode": 400,
                "headers": headers,
                "body": json.dumps({
                    "message": "MOTOSIERRA_EXISTS",
                }),
            }

        return save_motosierra(brand, model, power, weigth, headers)

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

def motosierra(brand, model, power, weigth):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("select * from Motosierras where brand = %s and model = %s and power = %s and weigth = %s;", (brand, model, power, weigth))
    result = cursor.fetchall()
    return len(result) > 0

def save_motosierra(brand, model, power, weigth, headers):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO MotoSierras (brand, model, power, weigth) VALUES (%s, %s, %s, %s)", (brand, model, power, weigth))
        connection.commit()

        return {
            "statusCode": 201,
            "headers": headers,
            "body": json.dumps({
                "message": "ITEM_SAVED",
            }),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": headers,
            "body": json.dumps({
                "message": "ERROR_SAVING_ITEM",
                "error": str(e)
            }),
        }
