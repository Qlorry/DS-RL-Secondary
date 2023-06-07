import socket   
from threading import Lock, Thread, Condition
import requests

from SecondaryService.Logging import *

class SecondaryDomainMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SecondaryDomain(metaclass=SecondaryDomainMeta):
    def __init__(self, master, my_port, lagtime):
        self.messages_mtx = Lock()
        self.messages = dict()
        self.lagtime = lagtime

        hostname=socket.gethostname()   
        IPAddr=socket.gethostbyname(hostname)   
        data = {
            "ip": str(IPAddr),
            "port": str(my_port)
        }

        # A POST request to the API
        post_response = requests.post("http://"+master+ "/register", json=data)
        # Print the response
        if not post_response.ok:
            domain_log("Registration failed")
            exit()
        domain_log("Registred on master with name " + str(IPAddr) + str(my_port))
    
    def add_message(self, id, msg):
        if self.lagtime != None:
            time.sleep(self.lagtime)

        with self.messages_mtx:
            self.messages[id] = msg

    def get_messages(self):
        with self.messages_mtx:
            return self.messages
        
        
