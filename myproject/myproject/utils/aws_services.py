import boto3
from fastapi.responses import JSONResponse

def invoke_lambda(function_name, payload):
    client = boto3.client("lambda")
    response = client.invoke(
        FunctionName=function_name,
        InvocationType="RequestResponse",
        Payload=payload
    )
    return respone['Payload'].read()

def get_appointment_from_dynamodb(table_name, appointment_id):
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.Table(table_name)
    response = table.get_item(Key={"id": appointment_id})
    return response.get("Item")


# This function puts an appointment into a DynamoDB table.
# It takes the table name and the appointment as parameters.
# It returns the response from the put_item operation.
def put_appointment_to_dynamodb(table_name, appointment):
    try:
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.Table(table_name)
        response = table.put_item(Item=appointment)
        return response
    except Exception as e:
        print(e)
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
    
    
def update_payment_status(appointment_id, user_id):
    # Update payment status in DynamoDB
    try:
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.Table("Appointments")
        response = table.update_item(
            Key={
                "appointmentId": appointment_id,
                "userId": user_id,
                },
            UpdateExpression="SET paymentMade = :val",
            ExpressionAttributeValues={
                ":val": True
            }
        )
        return True
    except Exception as e:
        print(e)
        return False