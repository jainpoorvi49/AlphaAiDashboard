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




# List of API endpoints
API_ENDPOINTS = [
    "https://django-backend1.azurewebsites.net/user/user2/",
    "https://django-backend1.azurewebsites.net/user/user1/"
]

async def fetch_data(client, endpoint, retries=3):
    for attempt in range(retries):
        try:
            response = await client.get(endpoint)
            response.raise_for_status()
            return {"endpoint": endpoint, "data": response.json()}
        except (httpx.RequestError, httpx.HTTPStatusError) as err:
            if attempt < retries - 1:
                await asyncio.sleep(2 ** attempt)
                continue
            return {"endpoint": endpoint, "error": f"Request error: {str(err)}"}


async def collect_all_data(batch_size=5):
    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
        results = []
        for i in range(0, len(API_ENDPOINTS), batch_size):
            batch = API_ENDPOINTS[i:i + batch_size]
            tasks = [fetch_data(client, endpoint) for endpoint in batch]
            results.extend(await asyncio.gather(*tasks))
        return results

@api_view(['GET'])
def get_all_clients_data(request):
    try:
        results = asyncio.run(collect_all_data())
    except Exception as e:
        return Response(
            {"status": "error", "message": "Critical error during data fetching.", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    successful_responses = [result["data"] for result in results if "data" in result]
    failed_responses = [result for result in results if "error" in result]

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
