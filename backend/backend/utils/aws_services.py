import boto3
import json
import logging
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from fastapi.responses import JSONResponse
from typing import Tuple, Dict, Any

from .aws_step_functions_utils import (
    start_execution,
    get_execution_response,
    fetch_execution_history,
    parse_error_from_history,
    poll_execution_status
)

# Initialize logger
logger = logging.getLogger(__name__)

# AWS Configuration
AWS_REGION = "us-east-1"
APPOINTMENTS_TABLE = "Appointments"
DOCTORS_TABLE = "Doctors"
FACES_TABLE = "FaceUserID"
STATE_MACHIN_ARN_BOOK_APPOINTMENT = "arn:aws:states:us-east-1:940760857739:stateMachine:BookAppointment"
STATE_MACHINE_ARN_WAIT_FOR_PAYMENT = "arn:aws:states:us-east-1:940760857739:stateMachine:WaitForPayment"

# Initialize AWS clients
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
rekognition_client = boto3.client("rekognition", region_name=AWS_REGION)

def process_payment(appointment_id: str, user_id: str) -> Tuple[bool, str]:
    """
    Process payment for the given appointment.

    :param appointment_id: ID of the appointment
    :param user_id: ID of the user
    :return: Tuple indicating success status and message
    """
    try:
        table = dynamodb.Table(APPOINTMENTS_TABLE)
        response = table.update_item(
            Key={"appointmentId": appointment_id, "userId": user_id},
            UpdateExpression="SET #status = :new_status",
            ConditionExpression="#status = :current_status",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={":new_status": "scheduled", ":current_status": "waiting for payment"}
        )
        return True, "Status updated to scheduled"
    except ClientError as e:
        if e.response['Error']['Code'] == "ConditionalCheckFailedException":
            return False, "Payment already made"
        logger.error(f"ClientError: {e}")
    except Exception as e:
        logger.error(f"Error: {e}")
        return False, f"An error occurred: {e}"
    return False, "Failed to process payment"

def book_appointment(user_id: str, specialty: str, doctorId: int, date: str, time: str) -> Dict[str, Any]:
    """
    Book an appointment and start the payment workflow.

    :param user_id: ID of the user
    :param specialty: Specialty for the appointment
    :param doctorId: ID of the doctor
    :param date: Appointment date
    :param time: Appointment time
    :return: Dictionary with booking status and message
    """
    input_data = {"userId": user_id, "specialty": specialty, "doctorId": doctorId, "date": date, "time": time}
            
    try:
        execution_info = start_execution(STATE_MACHIN_ARN_BOOK_APPOINTMENT, input_data)
        execution_arn = execution_info["executionArn"]
        execution_response = poll_execution_status(execution_arn)
                        
        if execution_response['status'] == 'SUCCEEDED':
            output_data = json.loads(execution_response["output"])
            appointment_id = output_data["appointmentData"]["appointmentId"]
            return {"success": True, "message": "Appointment booked and payment workflow started successfully", "appointment_id": appointment_id}
        
        history_response = fetch_execution_history(execution_arn)
        error_message = parse_error_from_history(history_response)
        return {"success": False, "message": error_message}
    except Exception as e:
        logger.error(f"Error booking appointment: {e}")
        return {"success": False, "message": str(e)}
        
def get_user_appointments(user_id: str) -> Dict[str, Any]:
    """
    Retrieve appointments for a specific user.

    :param user_id: ID of the user
    :return: Dictionary with the status and list of appointments
    """
    try:
        appointments_table = dynamodb.Table(APPOINTMENTS_TABLE)
        doctors_table = dynamodb.Table(DOCTORS_TABLE)
        
        appointments_response = appointments_table.query(
            IndexName="userId-index",
            KeyConditionExpression=Key("userId").eq(user_id)
        )
        appointments = appointments_response.get('Items', [])
        
        for appointment in appointments:
            doctor_response = doctors_table.get_item(Key={"doctorId": appointment["doctorId"]})
            doctor = doctor_response.get("Item", {})
            if doctor:
                appointment["doctorName"] = doctor.get("name", "Unknown Doctor")
        
        return {"status": "success", "appointments": appointments or []}
    except Exception as e:
        logger.error(f"Failed to query items from DynamoDB: {e}")
        return {"status": "error", "message": str(e)}
        
def get_appointment_status(appointment_id: str, user_id: str) -> Dict[str, Any]:
    """
    Retrieve the status of an appointment.

    :param appointment_id: ID of the appointment
    :param user_id: ID of the user
    :return: Dictionary with the appointment status
    """    
    try:
        table = dynamodb.Table(APPOINTMENTS_TABLE)
        response = table.get_item(Key={"appointmentId": appointment_id, "userId": user_id, })
        if 'Item' in response:
            return {"found": True, "appointment_id": appointment_id, "status": response['Item'].get('status', 'Uknown')}
        else:
            return {"found": False}
    except ClientError as e:
        logger.error(f"Failed to get item from DynamoDB: {e}")
        return {"error": str(e)}
    

def get_doctors() -> Dict[str, Any]:
    """
    Retrieve the list of doctors.

    :return: Dictionary with the status and list of doctors
    """
    try:
        table = dynamodb.Table(DOCTORS_TABLE)
        response = table.scan()
        doctors = response.get('Items', [])
        return {"status": "success", "doctors": doctors}
    except Exception as e:
        logger.error(f"Failed to scan items from DynamoDB: {e}")
        return {"status": "error", "message": str(e)}

def search_faces_by_image(source_bytes: bytes) -> Dict[str, Any]:
    """
    Search faces in the collection using the provided image.

    :param source_bytes: Image bytes
    :return: Dictionary with the search status and face ID if found
    """
    try:
        response = rekognition_client.search_faces_by_image(
            CollectionId="faces",
            Image={"Bytes": source_bytes},
            MaxFaces=1,
            FaceMatchThreshold=70,
            QualityFilter="AUTO"
        )
        
        face_matches = response.get("FaceMatches", [])
        if face_matches:
            matched_face = face_matches[0]
            return {"status": "success", "face_id": matched_face['Face']['FaceId'], "similarity": round(matched_face["Similarity"])}
        else:
            return {"status": "error", "message": "No faces matched"}
    
    except rekognition_client.exceptions.InvalidParameterException as e:
        logger.error("There are no faces in the image")
        return {"status": "error", "message": "No faces found in the image"}
    except Exception as e:
        logger.error(f"Error searching faces by image: {e}")
        return {"status": "error", "message": "Failed to search faces"}
        

def get_user_by_face_id(face_id: str) -> Dict[str, Any]:
    """
    Search faces in the collection using the provided image.

    :param source_bytes: Image bytes
    :return: Dictionary with the search status and face ID if found
    """
    try:
        table = dynamodb.Table(FACES_TABLE)
        response = table.query(KeyConditionExpression=Key("faceID").eq(face_id))
        items = response.get("Items", [])
        if items:
            return {"status": "success", "user_id": items[0]['userID']}
        else:
            return {"status": "error", "message": "No user associated with this face ID"}
            
    except Exception as e:
        logger.error(f"Error searchind user ID by face: {e}")
        return {"status": "error", "message": "Failed to retrieve user ID"}