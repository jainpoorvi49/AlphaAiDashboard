import os
from dotenv import load_dotenv
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, NewUserSerializer
import httpx
load_dotenv()


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful!",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_new_user(request):
    if request.method == 'POST':
        serializer = NewUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    


@api_view(['GET'])
def user1(request):
    try:
        data ={
            "user_id": 105,
            "margin": "₹25000",
            "used_margin": "No data available",
            "capital": "₹105430",
            "broker_name": "Angel",
            "return_percentage": "No data available",
            "number_of_orders_pinched": "No data available",
            "last_order_time": "No data available",
            "unfilled_buy_limit_option": "No data available",
            "running_m2m": "No data available"
        }
        return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        # Return an error response in case of an exception
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def user2(request):
    try:
        data ={
            "user_id": 106,
            "margin": "₹25",
            "used_margin": "No data available",
            "capital": "₹100",
            "broker_name": "Angel Broking",
            "return_percentage": "No data available",
            "number_of_orders_pinched": "No data available",
            "last_order_time": "No data available",
            "unfilled_buy_limit_option": "No data available",
            "running_m2m": "No data available"
        }
        return Response(data, status=status.HTTP_200_OK)

    except Exception as e:
        # Return an error response in case of an exception
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def get_all_clients_data(request):
    try:
        # Sample data
        data = [
            {
                "user_id": 106,
                "margin": "₹25",
                "used_margin": "No data available",
                "capital": "₹100",
                "broker_name": "Angel Broking",
                "return_percentage": "No data available",
                "number_of_orders_pinched": "No data available",
                "last_order_time": "No data available",
                "unfilled_buy_limit_option": "No data available",
                "running_m2m": "No data available"
            },
            {
                "user_id": 107,
                "margin": "₹50",
                "used_margin": "₹10",
                "capital": "₹200",
                "broker_name": "Zerodha",
                "return_percentage": "5%",
                "number_of_orders_pinched": "10",
                "last_order_time": "2024-12-12T15:30:00Z",
                "unfilled_buy_limit_option": "₹15",
                "running_m2m": "₹8"
            },
            {
                "user_id": 108,
                "margin": "₹56660",
                "used_margin": "₹10",
                "capital": "₹23300",
                "broker_name": "Zerodha",
                "return_percentage": "25%",
                "number_of_orders_pinched": "10",
                "last_order_time": "2024-12-12T15:30:00Z",
                "unfilled_buy_limit_option": "₹15",
                "running_m2m": "₹8"
            }
        ]

        # Structure response data
        response_data = []
        for client_data in data:
            formatted_data = {
                "user_id": client_data.get("user_id"),
                "margin": client_data.get("margin", "No data available"),
                "used_margin": client_data.get("used_margin", "No data available"),
                "capital": client_data.get("capital", "No data available"),
                "broker_name": client_data.get("broker_name", "No data available"),
                "return_percentage": client_data.get("return_percentage", "No data available"),
                "number_of_orders_pinched": client_data.get("number_of_orders_pinched", "No data available"),
                "last_order_time": client_data.get("last_order_time", "No data available"),
                "unfilled_buy_limit_option": client_data.get("unfilled_buy_limit_option", "No data available"),
                "running_m2m": client_data.get("running_m2m", "No data available"),
            }
            response_data.append(formatted_data)

        return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)

    except Exception as e:
        # Handle any exception and return a 500 response
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)