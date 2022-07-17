from email.policy import HTTP
from django import http
from django.shortcuts import render,redirect
from django.http import HttpResponse , JsonResponse
from chatapp.models import Room , Message
import threading
import time
import re
from datetime import datetime


 #<------------Auto delete msg every day-end to check is located in apps.py ------------------->
         
#  username and Password for django super user
# Username :- nikhil pass:- nikhil@123





# Create your views here.
#<-------------------------------------------------Home View Start Here -------------------------------------------------------->
def home(request):
    if request.method =="POST":
        #fetch data from form
        room_name = request.POST.get("room_name")
        username = request.POST.get("username")
        phone = request.POST.get("phone")
        #check if it is exixt in database
        if Room.objects.filter(roomname=room_name).exists():
            if block_unblock().is_bloked(phone,room_name):
                data = Room.objects.get(roomname=room_name)
                return HttpResponse("blocked")
            else:
                return HttpResponse('/room/'+room_name+'/'+phone+'?username='+username+'') 
        else:
            return HttpResponse("Room not exists")
    return render(request,'home.html')

#<------------------------------------ Main IS Blocked -------------------------->

def isblocked(request):
    roomname = request.GET.get("roomname")
    phone = request.GET.get("phone")    
    if block_unblock().is_bloked(phone,roomname):
        return HttpResponse('blocked')
    else:
        return HttpResponse('notblocked')


#<----------------------------------------------------Room View Here--------------------------------------------------------------->

def room(request,room,phone):
    username = request.GET.get('username')
    room_info = Room.objects.get(roomname=room)
    context = {
        'username':username,
        'phone' : phone,
        'room': room,
        'room_info':room_info
    }
    return render(request,'room.html',context)


#<-----------------------------------------------Create Room View Start Here-------------------------------------------------------------->

def create_room(request):
     #fetch data from form
    if request.method =='POST':
        roomname = request.POST.get("roomname")
        username = request.POST.get("username")
        phone = request.POST.get("phone")
        if Room.objects.filter(roomname=roomname).exists():
            return HttpResponse('<h1>Same Room Name Alredy Exist</h1>')
        else:
            new_room=Room.objects.create(roomname=roomname,adminname=username,phone=phone)
            new_room.save()
            return redirect('/room/'+roomname+'/'+phone+'?username='+username+'')
    return render(request,'create_room.html')


#<------------------------------------------------Delete Room View Start Here---------------------------------------------------------------->

def delete_room(request,room):
     # If Method isfetch data from form
    if request.method =='POST':
        roomname = request.POST.get("roomname")
        phone = request.POST.get("phone")
        Room.objects.get(roomname=roomname,phone=phone).delete()
        if Message.objects.filter(roomname=roomname).exists():
            Message.objects.get(roomname=roomname).delete()
            return HttpResponse('yes')

    #If Method Not Post then Show Whole Room Info.

    try:
        room_info = Room.objects.get(roomname=room)
        context = {
            'room_info':room_info
        }
        return render(request,'delete_room.html',context)
    except:
        room_info = "Not Found"
        context = {
            'room_info':room_info
        }
        return render(request,'delete_room.html',context)
        

#<-----------------------------------------#Class Block And Unblock Start Here function is start here----------------------------------------->

class block_unblock():
    def __init__(self):
        self.roomname = None
        self.phone    = None
        self.temp     = None
        self.data     = None
        
    #<-----------------------------------------#set data  And get_context function is start here----------------------------------------->
        
    def set_data(self,request):
        self.roomname = request.POST.get("roomname")
        self.phone = request.POST.get("phone")
        self.temp = Room.objects.get(roomname=self.roomname)
        self.data  = self.temp.blockuser
        
    def is_bloked(self,phone,room_name):
        data = Room.objects.get(roomname=room_name)
        temp_lst = list(data.blockuser.split('*'))
            #spilt and check if the no is alredy exist
        if phone in temp_lst:
            return True
        else:
            return False     
        
    def get_context(self,request):
        roomname = request.GET.get('roomname')
        phone = request.GET.get('phone')
        context = {
            'roomname':roomname,
            'phone' : phone
        }
        return context

    #<-----------------------------------------#block_user function is start here----------------------------------------->

    def block_user(self,request):
        # If Method Then fetch data from form
        if request.method =='POST':
            self.set_data(request)
            if self.phone == self.temp.phone:
                return HttpResponse('Room Owner Cannot Be Blocked')
            temp_lst = list(self.data.split('*'))
            #spilt and check if the no is alredy exist
            if self.phone in temp_lst:
                return HttpResponse('User is Alredy Blocked')
            else:
                #Add The Phone No in Blocked List
                new_block_user="*"+self.phone
                self.data=self.data+new_block_user
                # save and Return Conformation Data
                Room.objects.filter(roomname=self.roomname).update(blockuser=self.data)
                return HttpResponse('User Blocked Succesfully')
        
        #If Method Not Post then Show Block user template.
        return render(request,'block_user.html',context = self.get_context(request))
    
    
    #<-----------------------------------------#UN-block_user function is start here----------------------------------------->
 
 
 
    def unblock_user(self,request):
        # If Method isfetch data from form
        if request.method =='POST':
            self.set_data(request)
        # <--------------machanism to avoid redundancy of "*" in database ------------->
            counter=0
            for i in self.data: 
                if i == '*':
                    counter=counter+1
                    continue
                break
            new_data=self.data[counter:]
            updated_list=''
            temp_lst = list(new_data.split('*'))
        # <--------------END OF machanism to avoid redundancy of "*" in database ------------->
            if self.phone in temp_lst:
                temp_lst.remove(self.phone)
                for i in temp_lst:
                    updated_list=('*'+i)+updated_list
                # save and Return Conformation Data
                Room.objects.filter(roomname=self.roomname).update(blockuser=updated_list)
                new_data = ''
                self.data=''
                return HttpResponse('Un-Blocked')
            else:
                return HttpResponse('Not Found')

        #If Method Not Post then Show Block user template.
        return render(request,'unblock_user.html',context = self.get_context(request))

# <--------------------------------------------Send meassage View Here------------------------------------------------------------------>

def send_msg(request):
    # gether all data
    message =  request.POST.get("message")
    username = request.POST.get("username")
    room_id =  request.POST.get("room_id")
    phone =  request.POST.get("phone")
    # create data saving instance
    new_msg=Message.objects.create(value=message,user=username,roomname=room_id,phone=phone)
    # save and Return Conformation Data
    new_msg.save()
    return HttpResponse('Message Sent Succesfully...')


#  <---------------------------------------------Get meassage Using Room Name Start View Here------------------------------------------>

def get_messages(request,room):
    room_details = Room.objects.get(roomname=room)
    messages = Message.objects.filter(roomname=room)
    return JsonResponse({'messages':list(messages.values())})