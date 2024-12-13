import os
from dotenv import load_dotenv
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, NewUserSerializer
import httpx
import asyncio
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
        # Sample client data for user 1
        data = {
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

        # Return the final response with 'status' and 'data' keys
        return Response({
            "status": "success",
            "data": data
        }, status=status.HTTP_200_OK)

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
        return Response({
            "status": "success",
            "data": data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        # Return an error response in case of an exception
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def master_api(request):
    # Define the URLs of the two APIs
    api_1_url = "https://django-backend1.azurewebsites.net/user/user1"
    api_2_url = "https://django-backend1.azurewebsites.net/user/user2"

    # Initialize data and error containers
    combined_data = {}
    errors = []

    # Call API 1
    try:
        with httpx.Client(follow_redirects=True, timeout=30) as client:
            response_1 = client.get(api_1_url, verify=False)
            response_1.raise_for_status()  # Raise error if the status is not 200
            combined_data['api_1_data'] = response_1.json().get("data", {})
    except httpx.HTTPStatusError as http_err:
        errors.append({"api": api_1_url, "error": f"HTTP error: {http_err.response.status_code}"})
    except Exception as e:
        errors.append({"api": api_1_url, "error": str(e)})

    # Call API 2
    try:
        with httpx.Client(follow_redirects=True, timeout=30) as client:
            response_2 = client.get(api_2_url, verify=False)
            response_2.raise_for_status()  # Raise error if the status is not 200
            combined_data['api_2_data'] = response_2.json().get("data", {})
    except httpx.HTTPStatusError as http_err:
        errors.append({"api": api_2_url, "error": f"HTTP error: {http_err.response.status_code}"})
    except Exception as e:
        errors.append({"api": api_2_url, "error": str(e)})

    # If there are errors, return a partial success response
    if errors:
        return Response(
            {"status": "partial_success", "message": "Some API calls failed.", "data": combined_data, "errors": errors},
            status=207  # Multi-Status
        )

    # Return combined response if both calls succeed
    return Response({"status": "success", "data": combined_data}, status=200)
