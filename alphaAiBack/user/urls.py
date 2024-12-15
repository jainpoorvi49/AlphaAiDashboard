# user/urls.py
from django.urls import path
from .views import login,create_new_user, get_all_clients_data, fetch_data_for_client1, fetch_data_for_client2, fetch_data_for_client3,fetch_data_for_client4,fetch_data_for_client5,fetch_data_for_client6,fetch_data_for_all_clients

urlpatterns = [
    path('login/',login, name='login'),
    path('add/', create_new_user, name='create_new_user'),
    path('data/', get_all_clients_data , name='get_all_clients_data'),
    path('EC2853/', fetch_data_for_client1, name='EC2853'),
    path('ZZ4237/', fetch_data_for_client2, name='ZZ4237'),
    path('MI5008/', fetch_data_for_client3, name='MI5008'),
    path('WP7621/', fetch_data_for_client4, name='WP7621'),
    path('SOE424/', fetch_data_for_client5, name='SOE424'),
    path('AU4419/', fetch_data_for_client6, name='AU4419'),
    path('clients/', fetch_data_for_all_clients, name='clients'),
]
