import logging
import threading
import time
#to activate the debug logging add the following line


# Create and configure logger
def thread_function(name): # name is the name of the thread
    logging.info("Thread %s: starting", name) 
    time.sleep(2) # wait for 2 seconds
    print("2 seconds passed")
    logging.info("Thread %s: finishing", name)
    logging.debug("Solo per il debug")
    print("Esisto anche io")


format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.DEBUG,
                    datefmt="%H:%M:%S")

logging.info("Main    : before creating thread")
x = threading.Thread(target=thread_function, args=(0,)) # create a thread    
logging.info("Main    : before running thread")
x.start() # start the thread
logging.info("Main    : wait for the thread to finish")
x.join() # wait for the thread to finish
logging.info("Main    : all done")
# %%