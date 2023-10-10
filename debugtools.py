from datetime import datetime

def timer(function):    
    def wrapper():
        start_time = datetime.now()
        function()
        end_time = datetime.now()
        timing = (end_time - start_time).seconds
        print(f"Job time: {timing} sec. ")  
    return wrapper