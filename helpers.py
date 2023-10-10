import time

def repeator(seconds): 
    def wrapper_decorator(function):   
        def wrapper():
            while True:
                print(f"Function '{str(function.__name__).capitalize()}' wating for {seconds} sec... ")
                time.sleep(seconds)            
                print(f"{str(function.__name__).capitalize()} started...")
                try:
                    function()
                except:
                    pass
                print(f"{str(function.__name__).capitalize()} finished...")
        return wrapper
    return wrapper_decorator