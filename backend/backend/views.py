from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import JSONParser
from rest_framework import status, serializers
from rest_framework import serializers
from .utils import aws_services
from operator import itemgetter
from .authentication import create_token
from django.contrib.auth import authenticate
import base64

# CONSTANT for status codes
STATUS_SUCCESS = "success"
STATUS_ERROR = "error"

# Utility function for creating error responses
def create_error_response(message, status_code):
    return Response({"status": STATUS_ERROR, "message": message}, status=status_code)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(username=username, password=password)
        if user is not None:
            token = create_token(user.id)
            return Response({"access": token, "user": user.username, "userId": user.id}, status=200)
        else:
            return create_error_response("Invalid credentials", status.HTTP_401_UNAUTHORIZED)

class AppointmentSerializer(serializers.Serializer):
    specialty = serializers.CharField(required=True)
    doctorId = serializers.IntegerField(required=True)
    date = serializers.CharField(required=True)
    time = serializers.CharField(required=True)

class BookAppointmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if not serializer.is_valid():
            return create_error_response("Invalid data", status.HTTP_400_BAD_REQUEST)
                
        result = aws_services.book_appointment(**serializer.validated_data, user_id=request.user.id)
        
        if result["success"]:
            return Response({
                "status": "success",
                "appointment_id": result["appointment_id"],
                "message": result["message"],
            }, status=201)
        else:
            return self.handle_booking_error(result)
        
    def handle_booking_error(self, result):
        error_message = result["message"]
        if error_message == "DoctorNotFound":
            return create_error_response("Doctor does not exist", status.HTTP_404_NOT_FOUND)
        elif error_message == "AppointmentConflict":
            return create_error_response("An appointment already exists at this date and time", status.HTTP_409_CONFLICT)
        return create_error_response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProcessPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        appointment_id = request.data.get("appointment_id")
        user_id = request.user.id
        
        if not user_id:
            return create_error_response("Unauthorized, token missing or invalid", status.HTTP_401_UNAUTHORIZED)

        if not appointment_id:
            return create_error_response("Appointment ID required", status.HTTP_400_BAD_REQUEST)
        
        if self.process_payment(appointment_id):
            return self.update_payment_status(appointment_id, user_id)
        else:
            return create_error_response("Payment processing failed", status.HTTP_400_BAD_REQUEST)


    def process_payment(self, appointment_id):
        # Simulate payment processing
        return True
    
    def update_payment_status(self, appointment_id, user_id):
        success, message = aws_services.process_payment(appointment_id, user_id)
        if success:
            return Response({"status": STATUS_SUCCESS, "message": "Payment processed successfully"}, status=status.HTTP_200_OK)
        else:
            if message == "Payment already made":
                return create_error_response("Payment already made", status.HTTP_409_CONFLICT)
            return create_error_response("Failed to update appointment status", status.HTTP_500_INTERNAL_SERVER_ERROR)


class AppointmentStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, appointment_id):
        user_id = request.user.id
        result = aws_services.get_appointment_status(str(appointment_id), user_id)

        if "error" in result:
            return create_error_response("Server error, please try again later", status.HTTP_500_INTERNAL_SERVER_ERROR)
        if not result["found"]:
            return create_error_response("Appointment not found", status.HTTP_404_NOT_FOUND)

        return Response({
            "appointment_id": result["appointment_id"],
            "status": result["status"]
        }, status=status.HTTP_200_OK)


class UserAppointmentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        result = aws_services.get_user_appointments(user_id)

        if result["status"] == STATUS_SUCCESS:
            sorted_appointments = sorted(result["appointments"], key=itemgetter("date", "time"))
            return Response({"status": STATUS_SUCCESS, "appointments": sorted_appointments}, status=status.HTTP_200_OK)
        else:
            return create_error_response("message", "Failed to retrieve appointments", status.HTTP_400_BAD_REQUEST)
            

class DoctorsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        result = aws_services.get_doctors()

        if result["status"] == STATUS_SUCCESS:
            return Response({"status": STATUS_SUCCESS, "doctors": result["doctors"]}, status=status.HTTP_200_OK)
        else:
            return create_error_response(result.get("message", "Failed to retrieve doctors"), status.HTTP_400_BAD_REQUEST)
            
                        
class ClinicLoginView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]
    
    def post(self, request, *args, **kwargs):
        image_data = request.data.get("image")
        if not image_data:
            return create_error_response("Image data is required", status.HTTP_400_BAD_REQUEST)
        
        image_bytes = self.decode_image_data(image_data)
        if not image_bytes:
            return create_error_response("Invalid image data", status.HTTP_400_BAD_REQUEST)
            
        result = aws_services.search_faces_by_image(image_bytes)
        if result["status"] == STATUS_SUCCESS:
            return self.handle_face_recognition_success(result)
        else:
            return self.handle_face_recognition_failure(result)
    
    def decode_image_data(self, image_data):
        try:
            return base64.b64decode(image_data)
        except Exception as e:
            return None
        
    def handle_face_recognition_success(self, result):
        face_id = result["face_id"]
        user_result = aws_services.get_user_by_face_id(face_id)
        
        if user_result["status"] == STATUS_SUCCESS:
            return Response({"message": "Entered in the clinic successfully", "user_id": user_result["user_id"]}, status=status.HTTP_200_OK)
        else:
            return create_error_response(message, status.HTTP_404_NOT_FOUND if message == "No user associated with this face ID" else status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def handle_face_recognition_failure(self, result):
        message = result["message"]
        if message == "No faces found in the image":
            return create_error_response("No faces found in the image", status.HTTP_400_BAD_REQUEST)
        return create_error_response(message, status.HTTP_404_NOT_FOUND if message == "Unrecognized user" else status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
                            
