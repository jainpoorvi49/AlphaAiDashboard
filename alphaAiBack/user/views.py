import os
from dotenv import load_dotenv
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, NewUserSerializer
from concurrent.futures import ThreadPoolExecutor, as_completed
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
def user2(request):
    try:
        data ={
            "user_id": 105,
            "margin": "₹250",
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
    Master API: Collect and return data from multiple APIs with load balancing and optimized concurrency.
    """
    # Define the endpoint URLs (distribute across backend servers if needed)
    endpoints = [
        "https://django-backend1.azurewebsites.net/user/user2/",
        "https://django-backend1.azurewebsites.net/user/user1/"
    ]

    # Ensure all endpoints are valid
    if not endpoints:
        return Response(
            {"status": "error", "message": "No endpoints configured."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Container for successful and failed responses
    successful_responses = []
    failed_responses = []

    # Function to fetch data from an API endpoint
    def fetch_data(endpoint):
        try:
            with httpx.Client(follow_redirects=True, verify=False, timeout=15) as client:
                response = client.get(endpoint)
                response.raise_for_status()  # Raise error for HTTP status codes 4xx/5xx
                return {"endpoint": endpoint, "data": response.json()}
        except httpx.RequestError as req_err:
            return {"endpoint": endpoint, "error": f"Request error: {str(req_err)}"}
        except httpx.HTTPStatusError as http_err:
            return {"endpoint": endpoint, "error": f"HTTP error: {http_err.response.status_code}"}
        except Exception as e:
            return {"endpoint": endpoint, "error": str(e)}

    # Use ThreadPoolExecutor for concurrent API calls
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_endpoint = {executor.submit(fetch_data, url): url for url in endpoints}
        for future in as_completed(future_to_endpoint):
            result = future.result()
            if "data" in result:
                successful_responses.append(result["data"])
            else:
                failed_responses.append(result)

    # Final response
    if failed_responses:
        return Response(
            {
                "status": "partial_success",
                "message": "Some endpoints failed.",
                "data": successful_responses,
                "errors": failed_responses,
            },
            status=status.HTTP_207_MULTI_STATUS,
        )

    return Response({"status": "success", "data": successful_responses}, status=status.HTTP_200_OK)