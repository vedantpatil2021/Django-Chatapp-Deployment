from django.apps import AppConfig
import sys

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
            for p in Room.objects.raw('SELECT *  FROM chatapp_Room'):        
                Message.objects.filter(roomname=p).delete()

        schedule.every().day.at("00:00").do(del_msg)
        
        def everday_task():
            while True:
                schedule.run_pending()
                time.sleep(60)    
           
        t1 = threading.Thread(target=everday_task)
        t1.start()
        


        



    