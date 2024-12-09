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
            "margin": "₹20",
            "used_margin": "No data available",
            "capital": "₹80",
            "broker_name": "Upstox",
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
    """
    Master API: Collect and return data from all 7 APIs.
    """
    endpoints = [
        os.getenv("URL1"),
        os.getenv("URL2"),
        # Add more URLs as needed
    ]
    data = []
    try:
        with httpx.Client(follow_redirects=True) as client: 
            for endpoint in endpoints:
                response = client.get(f"{endpoint}")  
                response.raise_for_status()  
                client_data = response.json()

                data.append({
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
                })
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"status": "success", "data": data}, status=status.HTTP_200_OK)
    
