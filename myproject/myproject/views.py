from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import aws_services
from operator import itemgetter
import uuid

# class BookAppointmentView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def post(self, request):
#         user_id = request.user.id # Extracting the user ID from the JWT
#         data = request.data
        
#         # Validate and extract appointment details
#         specialty = data.get("specialty")
#         doctorId = data.get("doctorId")
#         date = data.get("date")
#         time = data.get("time")
                
#         # Check if any of the required fields are missing
#         if not specialty or not doctorId or not date or not time:
#             return Response({"status": "error", "message": "All fields are required"}, status=400)
        
#         # Generate a UUID for the appointment ID
#         appointment_id = str(uuid.uuid4())
        
#         # Prepare the appointment data for DynamoDB
#         appointment_data = {
#             "appointmentId": appointment_id,
#             "userId": user_id,
#             "specialty": specialty,
#             "doctorId": doctorId,
#             "date": date,
#             "time": time,
#             "status": "waiting for payment",
#         }
        
#         # Attempt to put the appointment data into DynamoDB
#         response = aws_services.put_appointment_to_dynamodb(appointment_data)
        
#         if response.get("status") == "error":
#             if response.get("message") == "An appointment already exists at this date and time":
#                 status_code = 409 # Conflict
#             elif response.get("message") == "Doctor does not exist":
#                 status_code = 404
#             else:
#                 status_code = 500
#             return Response({"status": "error", "message": response["message"]}, status=status_code)
        
#         if response.get("status") == "success":
#             # Start the payment workflow
#             workflow_result = aws_services.start_payment_workflow(appointment_id, user_id)
#             if workflow_result and workflow_result.get("success"):
#                 return Response({
#                     "status": "success",
#                     "message": "Appointment booked and payment workflow started successfully",
#                     "appointment_id": appointment_id
#                 }, status=201)
#             else:
#                 return Response({"status": "error", "message": workflow_result.get("message", "Failed to start payment workflow")}, status=500)
            
#         # If the response does not match expected outcomes
#         return Response({"status": "error", "message": "Unexpected response from DynamoDB"}, status=500)

class BookAppointmentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user_id = request.user.id
        data = request.data
        
        # Validate and extract appointment details
        specialty = data.get("specialty")
        doctorId = data.get("doctorId")
        date = data.get("date")
        time = data.get("time")
        
        # Check if any of the required fields are missing
        if not specialty or not doctorId or not date or not time:
            return Response({"status": "error", "message": "All fields are required"}, status=400)
        
        # Start the booking process
        result = aws_services.book_appointment(user_id, specialty, doctorId, date, time)
        
        if result["success"]:
            return Response({
                "status": "success",
                "message": result["message"],
                "appointment_id": result["appointment_id"],
                }, status=201)
        else:            
            if result["message"] == "DoctorNotFound":
                return Response({
                    "status": "error",
                    "message": "Doctor does not exist."
                    }, status=404)
                
            elif result["message"] == "AppointmentConflict":
                return Response({
                    "status": "error",
                    "message": "An appointment already exists at this date and time."
                    },status=409)
                
            return Response({"status": "error", "message": result["message"]}, status=500)


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
    
    
class AppointmentStatusView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, appointment_id):
        user_id = request.user.id
        result = aws_services.get_appointment_status(str(appointment_id), user_id)
        
        if "error" in result:
            return Response({"message": "Server error, please try again later."}, status=500)
        if not result["found"]:
            return Response({"message": "Appointment not found"}, status=404)
        
        return Response({
            "appointment_id": result["appointment_id"],
            "status": result["status"]
        }, status=200)
        
    
class UserAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_id = request.user.id
        result = aws_services.get_user_appointments(user_id)
        
        if result["status"] == "success":
            if not result["appointments"]:
                return Response({
                    "status": "success",
                    "appointments": []
                }, status=200)
            
            sorted_appointments = sorted(result["appointments"], key=itemgetter("date", "time"))
            
            return Response({
                "status": "success",
                "appointments": sorted_appointments
            }, status=200)
        else:
            return Response({
                "status": "error",
                "message": result.get("message", "Failed to retrieve appointments")
            }, status=400)
        