from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework import serializers
from .utils import aws_services
from operator import itemgetter
from .authentication import create_token, decode_token
from django.contrib.auth import authenticate

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        
        user = authenticate(username=username, password=password)
        if user is not None:
            token = create_token(user.id)
            return Response({"access": token, "user": user.username})
        else:
            return Response({"error": "Invalid credentials"}, status=400)

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
            return Response({"status": "error", "message": "Invalid data"}, status=400)
                
        result = aws_services.book_appointment(**serializer.validated_data, user_id=request.user.id)
        
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
                }, status=409)

            return Response({"status": "error", "message": result}, status=500)


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
            success, message = aws_services.process_payment(appointment_id, user_id)
            if success:
                return Response({"status": "success", "message": "Payment processed successfully"}, status=200)
            else:
                if message == "Payment already made":
                    return Response({"status": "error", "message": "Payment already made"}, status=409)
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
        result = aws_services.get_appointment_status(
            str(appointment_id), user_id)

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

            sorted_appointments = sorted(
                result["appointments"], key=itemgetter("date", "time"))

            return Response({
                "status": "success",
                "appointments": sorted_appointments
            }, status=200)
        else:
            return Response({
                "status": "error",
                "message": result.get("message", "Failed to retrieve appointments")
            }, status=400)
