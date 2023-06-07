from enum import Enum, unique

SERVICE_NAME = "master-service"

@unique
class ConfigKeys(Enum):
    PORT = "PORT"
    MASTER_ADDR = "MS_ADDR" 
    LAG = "LAG"
