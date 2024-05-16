import boto3
import botocore
from boto3.dynamodb.conditions import Key
from fastapi.responses import JSONResponse
from botocore.exceptions import ClientError
import json
import time
from .aws_step_functions_utils import start_execution, get_execution_response, fetch_execution_history, parse_error_from_history, poll_execution_status
    
import boto3

import boto3

def process_payment(appointment_id, user_id):
    try:
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.Table("Appointments")
        response = table.update_item(
            Key={
                "appointmentId": appointment_id,
                "userId": user_id,
            },
            UpdateExpression="SET #status = :new_status",
            ConditionExpression="#status = :current_status",
            ExpressionAttributeNames={
                "#status": "status"
            },
            ExpressionAttributeValues={
                ":new_status": "scheduled",
                ":current_status": "waiting for payment"
            }
        )
        return True, "Status updated to scheduled"
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            return False, "Payment already made"
    except Exception as e:
        print(e)
        return False, f"An error occurred: {e}"


    

def book_appointment(user_id, specialty, doctorId, date, time):
    input_data = {
        "userId": user_id,
        "specialty": specialty,
        "doctorId": doctorId,
        "date": date,
        "time": time
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
        
def get_user_appointments(user_id):
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    appointments_table = dynamodb.Table("Appointments")
    doctors_table = dynamodb.Table("Doctors")
    try:
        # Query appointments by user ID
        appointments_response = appointments_table.query(
            IndexName="userId-index",
            KeyConditionExpression=Key("userId").eq(user_id)
        )
        appointments = appointments_response.get('Items', [])
        
        # Fetch doctor names for each appointment
        for appointment in appointments:
            doctor_response = doctors_table.get_item(
                Key={"doctorId": appointment["doctorId"]}
            )
            doctor = doctor_response.get("Item", {})
            if doctor:
                appointment["doctorName"] = doctor.get("name", "Unknown Doctor")
        
        if appointments:
            return {"status": "success", "appointments": appointments}
        else:
            print("No appointments found")
            return {"status": "success", "message": "No appointments found", "appointments": []}
        
    except Exception as e:
        print(f"Failed to query items from DynamoDB: {e}")
        return {"status": "error", "message": str(e)}
        
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
    

def get_doctors():
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    table = dynamodb.Table("Doctors")
    
    try:
        response = table.scan()
        doctors = response.get('Items', [])
        return {"status": "success", "doctors": doctors}
    except Exception as e:
        print(f"Failed to scan items from DynamoDB: {e}")
        return {"status": "error", "message": str(e)}


rekognition_client = boto3.client('rekognition', region_name='us-east-1')

def search_faces_by_image(source_bytes):
    try:
        response = rekognition_client.search_faces_by_image(
            CollectionId="faces",
            Image={
                "Bytes": source_bytes,
            },
            MaxFaces=1,
            FaceMatchThreshold=70,
            QualityFilter="AUTO"
        )
        
        face_matches = response.get("FaceMatches", [])
        if face_matches:
            matched_face = face_matches[0]
            return {
                "status": "success",
                "face_id": matched_face['Face']['FaceId'],
                "similarity": round(matched_face["Similarity"])
            }
        else:
            return {
                "status": "error",
                "message": "No faces matched"
            }
            
    except Exception as e:
        print(f"Error: {e}")
        return {
            "status": "error",
            "message": "Failed to process image"
        }
        

def get_user_by_face_id(face_id):
    try:
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.Table("FaceUserID")
        
        response = table.query(
            KeyConditionExpression=Key("faceID").eq(face_id)
        )
        items = response.get("Items", [])
        if items:
            return {
                "status": "success",
                "user_id": items[0]['userID']
            }
        else:
            return {
                "status": "error",
                "message": "No user associated with this face ID"
            }
            
    except Exception as e:
        print(f"Error: {e}")
        return {
            "status": "error",
            "message": "Failed to retrieve user ID"
        }