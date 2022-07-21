from django.apps import AppConfig
import sys
from django.http import HttpResponse



delete_msg_status = 0

#<-----------------------------------------is Message deleting view function starting here --------------------------------------->
def delete_msg_fun(request):
    return  HttpResponse(delete_msg_status)
#<-----------------------------it will use for shoeing a dilog window while msg deleting-------------------------------->



class ChatappConfig(AppConfig):
    name = 'chatapp'
    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        # you must import your modules here 
        # to avoid AppRegistryNotReady exception 
        from .models import Room , Message 
        import time
        import schedule
        import threading
        # startup code here
#<-------------------keep run code infinite to delete msg every day end to check ---------------------------->
        def del_msg():
            time.sleep(1.2)
            global delete_msg_status
            delete_msg_status = 1
            time.sleep(1.7)
            for p in Room.objects.raw('SELECT *  FROM chatapp_Room'):        
                Message.objects.filter(roomname=p).delete()
            delete_msg_status = 0 
        schedule.every().day.at("00:00").do(del_msg)
        # schedule.every(25).seconds.do(del_msg)
        
        def everday_task():
            while True:
                schedule.run_pending()
                time.sleep(60)    
           
        t1 = threading.Thread(target=everday_task)
        t1.start()
        


        



    