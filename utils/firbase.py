import firebase_admin
from firebase_admin import db, credentials
import os
from dotenv import load_dotenv
from utils.fieldData import FieldData
import logging


load_dotenv(".env")
logging.basicConfig(filename="log.log")


fieldData=FieldData()

logging.basicConfig(filename="log.log", level=logging.WARNING)

class Firebase(object):
    def __init__(self) -> None:
        self.cred=credentials.Certificate('agrisage-85205-firebase-adminsdk-6ih1w-881ad47372.json')
        firebase_admin.initialize_app(self.cred, {'databaseURL' : os.getenv('FIREBASE_URL')})
        
    def getKeys(self, key:str):
        try:
            keys=db.reference('/').get()
            keys=keys.keys()
        
            if key in keys:
                ifExists=True
            else:
                ifExists=False
            return ifExists
        except Exception as e:
            logging.exception(e)
            return None
    
    def getValue(self, key:str):
        try:
            ifExists=self.getKeys(key=key)
            if ifExists:
                value=db.reference(key).get()
                fieldData.addData(tableName=key, data=value)
                iotData=fieldData.getFieldData(tableName=key)
                
                return iotData
            else:
                iotData=False
            return iotData
        except Exception as e:
            logging.exception(e)
            return None
        
    def setValue(self, key, value):
        try:
            ifExists=self.getKeys(key=key)
            if ifExists:
                db.reference(key).update({'treshold' : value})
        except Exception as e:
            logging.exception(e)

        
    
        
        
            

