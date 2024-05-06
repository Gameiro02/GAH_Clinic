import boto3
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError
import json
import time
from .aws_step_functions_utils import start_execution, get_execution_response, fetch_execution_history, parse_error_from_history, poll_execution_status

# This function puts an appointment into a DynamoDB table.
# It takes the table name and the appointment as parameters.
# It returns the response from the put_item operation.
# def put_appointment_to_dynamodb(appointment):
#     try:
#         # Initialize DynamoDB resource
#         dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
#         doctors_table = dynamodb.Table("Doctors")
#         appointments_table = dynamodb.Table("Appointments")
        
#         # Check if the doctor exists
#         doctor_response = doctors_table.get_item(
#             Key={"doctorId": appointment["doctorId"]}
#         )
#         if 'Item' not in doctor_response:
#             return {
#                 "status": "error",
#                 "message": "Doctor does not exist",
#                 "http_status": 404 # Not Found
#             }
        
#         # Construct the query to find conflicting appointments
#         # Is it supposed to have GSI for date and time queries?
#         response = appointments_table.scan(
#             FilterExpression='#date_attr = :date_val AND #time_attr = :time_val',
#             ExpressionAttributeNames={
#                 '#date_attr': 'date', # Date is a reserved keyword in DynamoDB
#                 '#time_attr': 'time' # Time is a reserved keyword in DynamoDB
#             },
#             ExpressionAttributeValues={
#                 ':date_val': appointment['date'],
#                 ':time_val': appointment['time']
#             }
#         )
        
#         if response['Items']:
#             return {
#                 "status": "error",
#                 "message": "An appointment already exists at this date and time",
#                 "http_status": 409, # Conflict
#             }
            
#         # No conflicting appointments, put the new appointment into the table
#         put_response = appointments_table.put_item(Item=appointment)
#         return {
#             "status": "success",
#             "message": "Appointment booked successfully",
#             "http_status": 201 # Created
#         }
    
#     except ClientError as e:
#         print(e)
#         return {
#             "status": "error",
#             "message": f"Failed to access DynamoDB: {str(e)}",
#             "http_status": 503 # Service Unavailable
#         }
#     except Exception as e:
#         print(e)
#         return {
#             "status": "error",
#             "message": f"An error occurred: {str(e)}",
#             "http_status": 500 # Internal Server Error
#         }

    
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
            UpdateExpression="SET #status = :val",
            ExpressionAttributeNames={
                "#status": "status"
            },
            ExpressionAttributeValues={
                ":val": "scheduled"
            }
        )
        return True
    except Exception as e:
        print(e)
        return False
    

def book_appointment(user_id, specialty, doctor_id, date, appointmentTime):
    input_data = {
        "userId": user_id,
        "specialty": specialty,
        "doctorId": doctor_id,
        "date": date,
        "time": appointmentTime
    }
    
    state_machine_arn = "arn:aws:states:us-east-1:940760857739:stateMachine:BookAppointment"
     
    try:
        execution_info = start_execution(state_machine_arn, input_data)
        execution_arn = execution_info["executionArn"]
        execution_response = poll_execution_status(execution_arn)
                
        # If the execution succeeded, start the payment workflow
        if execution_response['status'] == 'SUCCEEDED':
            output_data = json.loads(execution_response["output"])
            appointment_id = output_data["appointmentData"]["appointmentId"]
            
            return {
                "success": True,
                "message": "Appointment booked and payment workflow started successfully",
                "appointment_id": appointment_id
            }
        
        history_response = fetch_execution_history(execution_arn)
        error_message = parse_error_from_history(history_response)
        
        # If the execution failed, return the error message
        return {
            "success": False,
            "message": error_message
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }
    
def start_payment_workflow(appointment_id, user_id):
    try:
        sfn_client = boto3.client("stepfunctions")
        state_machine_arn = "arn:aws:states:us-east-1:940760857739:stateMachine:WaitForPayment"
        input = {
            "appointment_id": appointment_id,
            "user_id": user_id
        }
        sfn_response = sfn_client.start_execution(
            stateMachineArn=state_machine_arn,
            input=json.dumps(input)
        )
        return {
            "success": "True",
            "message": "Appointment bookend and payment workflow started successfully",
            "executionArn": sfn_response["executionArn"]
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to start workflow: {str(e)}"
        }
        
def get_appointment_status(appointment_id, user_id):
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.Table("Appointments")
    
    try:
        response = table.get_item(Key={
                "appointmentId": appointment_id,
                "userId": user_id,
                })
        if 'Item' in response:
            return {
                "found": True,
                "appointment_id": appointment_id,
                "status": response['Item'].get('status', 'Uknown')
            }
        else:
            return {"found": False}
    except ClientError as e:
        print(f"Failed to get item from DynamoDB: {e}")
        return {"error": str(e)}