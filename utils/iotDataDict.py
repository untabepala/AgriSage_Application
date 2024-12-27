from typing import TypedDict
import logging

logging.basicConfig(filename="log.log", level=logging.WARNING)

class IoTDataDict(TypedDict):
    date=[]
    potassium=[]
    nitrogen=[]
    calcium=[]
    temperature=[]
    humidity=[]
    soilMoisture=[]
    waterLevel=[]
    phLavel=[]
    
    