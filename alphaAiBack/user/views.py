import os
from dotenv import load_dotenv
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import LoginSerializer, NewUserSerializer
import httpx
from .utils import format_indian_number
import concurrent.futures
import requests
from kiteconnect import KiteConnect
import pandas as pd
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
    
@api_view(['GET'])
def fetch_data_for_all_clients(request):
    # Define the user IDs and directly specify the URLs
    urls = [
        'http://localhost:8000/user/EC2853',
        'http://localhost:8000/user/ZZ4237'
    ]

    # Use a ThreadPoolExecutor to fetch data concurrently from each URL
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Directly pass the list of URLs in the executor.map() call
        results = list(executor.map(requests.get, urls))

    # Parse the JSON response from each request
    client_data = [result.json() for result in results]

    # Format the data in the specified structure
    formatted_data = []
    for client in client_data:
        formatted_data.append({
            "user_id": client.get("client_id"),
            "margin": client.get("available_margin", "No data available"),
            "used_margin": client.get("used_margin", "No data available"),
            "capital": client.get("capital", "No data available"),
            "broker_name": "Broker Name Placeholder",  # You can replace this with actual data if available
            "return_percentage": client.get("return (%)", "No data available"),
            "number_of_orders_pinched": client.get("number_of_orders_punched", "No data available"),
            "last_order_time": client.get("last_order_time", "No data available"),
            "unfilled_buy_limit_option": client.get("unfilled_buy_limit_option", "No data available"),
            "running_m2m": "Running M2M Placeholder",  # Replace with actual data if available
        })

    # Return the formatted data as an array of objects
    return Response(formatted_data)

@api_view(['GET'])
def fetch_data_for_client1(request):
    user_id = 'EC2853'
    login = pd.read_csv('user\\data\\login.csv')
    access_token_value = login.loc[login['login ID'] == user_id, 'access_token'].values
    api_k_value = login.loc[login['login ID'] == user_id, 'api_k'].values
    api_s_value = login.loc[login['login ID'] == user_id, 'api_s'].values
    
    api_k = api_k_value[0]
    api_s = api_s_value[0]
    access_token = access_token_value[0]

    kite = KiteConnect(api_key=api_k)
    kite.set_access_token(access_token)
    print("I am here ")
    
    try:
        margin_data = kite.margins(segment="equity")
        available_margin = margin_data['net']
        used_margin = margin_data['utilised']['exposure'] + margin_data['utilised']['span']
        capital = int(available_margin + used_margin)
        print(f"Available Margin: {available_margin}, Used Margin: {used_margin}, Capital: {capital}")
        positions = kite.positions()
        current_pnl = sum(
            position['pnl'] for position in positions['net'] if position['tradingsymbol']
        )

        return_percentage = (current_pnl / capital) * 100 if capital != 0 else 0

        orders = kite.orders()
        number_of_orders_punched = len(orders)
        last_order_time = max(
            [order['order_timestamp'] for order in orders], default=None
        )
        last_order_time = last_order_time.strftime("%Y-%m-%d %H:%M:%S") if last_order_time else "No orders"

        has_unfilled_buy_limit_option = any(
            order['order_type'] == 'LIMIT' and
            order['transaction_type'] == 'BUY' and
            order['product'] == 'NRML' and
            order['status'] not in ['COMPLETE', 'TRIGGER PENDING']
            for order in orders
        )

        formatted_capital = format_indian_number(capital)
        formatted_available_margin = format_indian_number(available_margin)
        formatted_used_margin = format_indian_number(used_margin)
        formatted_current_pnl = format_indian_number(current_pnl)

        if number_of_orders_punched > 100:
            subject = f"Alert: {user_id} has placed {number_of_orders_punched} orders"
            body = (f"Client ID: {user_id}\n"
                    f"Number of Orders Placed: {number_of_orders_punched}\n"
                    f"Last Order Time: {last_order_time}\n"
                    f"Available Margin: {formatted_available_margin}\n"
                    f"Used Margin: {formatted_used_margin}\n"
                    f"Current PnL: {formatted_current_pnl}\n")
            # send_email(subject, body)

    except Exception as e:
        print(f"Error fetching data for client {user_id}: {e}")
        formatted_capital = formatted_available_margin = formatted_used_margin = formatted_current_pnl = 0
        number_of_orders_punched = return_percentage = 0
        last_order_time = "Error fetching"
        has_unfilled_buy_limit_option = False

    # Return the dictionary wrapped in a Response
    return Response({
        "client_id": user_id,
        "capital": formatted_capital,
        "available_margin": formatted_available_margin,
        "used_margin": formatted_used_margin,
        "current_pnl": formatted_current_pnl,
        "return (%)": round(return_percentage, 2),
        "number_of_orders_punched": number_of_orders_punched,
        "last_order_time": last_order_time,
        "unfilled_buy_limit_option": has_unfilled_buy_limit_option
    })

@api_view(['GET'])
def fetch_data_for_client2(request):
    user_id = 'ZZ4237'
    login = pd.read_csv('user\\data\\login.csv')
    access_token_value = login.loc[login['login ID'] == user_id, 'access_token'].values
    api_k_value = login.loc[login['login ID'] == user_id, 'api_k'].values
    api_s_value = login.loc[login['login ID'] == user_id, 'api_s'].values
    
    api_k = api_k_value[0]
    api_s = api_s_value[0]
    access_token = access_token_value[0]

    kite = KiteConnect(api_key=api_k)
    kite.set_access_token(access_token)
    print("I am here ")
    
    try:
        margin_data = kite.margins(segment="equity")
        available_margin = margin_data['net']
        used_margin = margin_data['utilised']['exposure'] + margin_data['utilised']['span']
        capital = int(available_margin + used_margin)
        print(f"Available Margin: {available_margin}, Used Margin: {used_margin}, Capital: {capital}")
        positions = kite.positions()
        current_pnl = sum(
            position['pnl'] for position in positions['net'] if position['tradingsymbol']
        )

        return_percentage = (current_pnl / capital) * 100 if capital != 0 else 0

        orders = kite.orders()
        number_of_orders_punched = len(orders)
        last_order_time = max(
            [order['order_timestamp'] for order in orders], default=None
        )
        last_order_time = last_order_time.strftime("%Y-%m-%d %H:%M:%S") if last_order_time else "No orders"

        has_unfilled_buy_limit_option = any(
            order['order_type'] == 'LIMIT' and
            order['transaction_type'] == 'BUY' and
            order['product'] == 'NRML' and
            order['status'] not in ['COMPLETE', 'TRIGGER PENDING']
            for order in orders
        )

        formatted_capital = format_indian_number(capital)
        formatted_available_margin = format_indian_number(available_margin)
        formatted_used_margin = format_indian_number(used_margin)
        formatted_current_pnl = format_indian_number(current_pnl)

        if number_of_orders_punched > 100:
            subject = f"Alert: {user_id} has placed {number_of_orders_punched} orders"
            body = (f"Client ID: {user_id}\n"
                    f"Number of Orders Placed: {number_of_orders_punched}\n"
                    f"Last Order Time: {last_order_time}\n"
                    f"Available Margin: {formatted_available_margin}\n"
                    f"Used Margin: {formatted_used_margin}\n"
                    f"Current PnL: {formatted_current_pnl}\n")
            # send_email(subject, body)

    except Exception as e:
        print(f"Error fetching data for client {user_id}: {e}")
        formatted_capital = formatted_available_margin = formatted_used_margin = formatted_current_pnl = 0
        number_of_orders_punched = return_percentage = 0
        last_order_time = "Error fetching"
        has_unfilled_buy_limit_option = False

    # Return the dictionary wrapped in a Response
    return Response({
        "client_id": user_id,
        "capital": formatted_capital,
        "available_margin": formatted_available_margin,
        "used_margin": formatted_used_margin,
        "current_pnl": formatted_current_pnl,
        "return (%)": round(return_percentage, 2),
        "number_of_orders_punched": number_of_orders_punched,
        "last_order_time": last_order_time,
        "unfilled_buy_limit_option": has_unfilled_buy_limit_option
    })