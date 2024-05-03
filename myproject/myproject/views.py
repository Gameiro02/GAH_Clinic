from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import aws_services
import uuid

class BookAppointmentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user_id = request.user.id # Extracting the user ID from the JWT
        data = request.data
        
        # Validate and extract appointment details
        specialty = data.get("specialty")
        doctorId = data.get("doctorId")
        date = data.get("date")
                
        # List to collect missing fields
        missing_fields = []
        if not specialty:
            missing_fields.append("specialty")
        if not doctorId:
            missing_fields.append("doctorId")
        if not date:
            missing_fields.append("date")

        # Check if there are any missing fields and respond accordingly
        if missing_fields:
            error_message = "Missing information for the following field(s): " + ", ".join(missing_fields)
            return Response({"status": "error", "message": error_message}, status=400)
        
        # Generate a UUID for the appointment ID
        appointment_id = str(uuid.uuid4())
        
        # Prepare the appointment data for DynamoDB
        appointment_data = {
            "appointmentId": appointment_id,
            "userId": user_id,
            "specialty": specialty,
            "doctorId": doctorId,
            "appointmentDateTime": date,
        }
        
        # Attempt to put the appointment data into DynamoDB
        response = aws_services.put_appointment_to_dynamodb("Appointments", appointment_data)
        
        if isinstance(response, dict) and "ResponseMetadata" in response:
            # Check the HTTP status code in the response Metadata
            http_status_code = response["ResponseMetadata"].get("HTTPStatusCode")
            if http_status_code == 200:
                result = {"status": "success", "message": "Appointment booked successfully"}
                return Response(result, status=201)
            else:
                return Response({"status": "error", "message": "Failed to book appointment"}, status=500)
        else:
            # Handle the case where the response is not as expected
            return Response({"status": "error", "message": "Unexpected response from DynamoDB"}, status=500)
        

class ProcessPaymentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        appointment_id = request.data.get("appointment_id")
        user_id = request.user.id
        
        if not appointment_id or not user_id:
            return Response({"status": "error", "message": "Appointment ID or User ID is required"}, status=400)
        
        payment_successful = self.process_payment(appointment_id)
        
        if payment_successful:
            # Update the appointment status in DynamoDB
            if aws_services.update_payment_status(appointment_id, user_id):
                return Response({"status": "success", "message": "Payment processed successfully"}, status=200)
            else:
                return Response({"status": "error", "message": "Failed to update appointment status"}, status=500)
        else:
            return Response({"status": "error", "message": "Payment processing failed"}, status=400)
    
    def process_payment(self, appointment_id):
        # Simulate payment processing
        return True