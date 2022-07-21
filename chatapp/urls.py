from django.contrib import admin
from django.urls import path,include
from chatapp import views,apps

urlpatterns = [
    path('',views.home,name='home'),
    path('room/<str:room>/<str:phone>',views.room,name='room'),
    path('send',views.send_msg,name='send_msg'),
    path('get_messages/<str:room>',views.get_messages,name='get_messages'),
    path('create_room',views.create_room,name='create_room'),
    path('delete_room/<str:room>',views.delete_room,name='delete_room'),
    path('block_user',views.block_unblock().block_user,name='block_user'),
    path('unblock_user',views.block_unblock().unblock_user,name='unblock_user'),
    path('isblocked',views.isblocked,name='isblocked'),
    path('delete_msg_fun',apps.delete_msg_fun,name='delete_msg_fun'),
]
