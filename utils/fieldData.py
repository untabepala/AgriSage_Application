from mysql import connector
from datetime import datetime
from utils.iotDataDict import IoTDataDict
import logging

logging.basicConfig(filename="log.log", 
                    level=logging.WARNING)

class FieldData(object):
    def __init__(self, host="localhost", user="root", password="", databaseName="AgriSage") -> None:
        try:
            fieldDataDB=connector.connect(
                host=host,
                user=user,
                password=password
            )
            
            cursor=fieldDataDB.cursor()
            
            sql=f'''
                CREATE DATABASE IF NOT EXISTS {databaseName}
            '''
            
            cursor.execute(sql)
        except Exception as e:
            logging.exception(e)
        finally:
            cursor.close()
        
    
    def connectDB(self, host="localhost", user="root", password="", databaseName="AgriSage"):
        try:
            fieldDataDB=connector.connect(
                host=host,
                user=user,
                password=password,
                database=databaseName
            )
            
            cursor=fieldDataDB.cursor()
        except Exception as e:
            logging.exception(e)
        return fieldDataDB, cursor

    
    def createFieldDataTable(self, tableName:str):
        _, cursor=self.connectDB()
        try:
            tableName="table_".join(tableName)
            
            sql=f'''
                CREATE TABLE {tableName} (
                    time DATETIME,
                    temperature VARCHAR(10),
                    humidity VARCHAR(10),
                    potassium VARCHAR(10),
                    nitrogen VARCHAR(10),
                    calcium VARCHAR(10),
                    soilMoisture VARCHAR(10),
                    waterLevel VARCHAR(10),
                    phLavel VARCHAR(10)
                )
            '''
            
            cursor.execute(sql)
        except Exception as e:
            logging.exception(e)
        finally:
            cursor.close()
            
    def editFieldDataTable(self, oldTableName:str, newTableName:str):
        _, cursor=self.connectDB()
        try:
            oldTableName="table_".join(oldTableName)
            newTableName="table_".join(newTableName)
            
            sql=f'''
            RENAME TABLE {oldTableName} TO {newTableName}
            '''
            cursor.execute(sql)
        except Exception as e:
            logging.exception(e)
        finally:
            cursor.close()
                   
            
    def deleteFieldDataTable(self, tableName:str):
        _, cursor=self.connectDB()
        try:
            tableName="table_".join(tableName)
            sql=f'''
            DROP TABLE {tableName}
            '''
            cursor.execute(sql)
        except Exception as e:
            logging.exception(e) 
        finally:
            cursor.close()

            
            
    def addData(self, tableName:str, data:dict):
        fieldDataDB, cursor=self.connectDB()
        try:
            tableName="table_".join(tableName)
            time=str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            sql = f''' INSERT INTO {tableName} (time, temperature, humidity, potassium, nitrogen, calcium, soilMoisture, waterLevel, phLavel) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
            values=(
                time,
                str(data['temperature']),
                str(data['humidity']),
                str(data['potassium']),
                str(data['nitrogen']),
                str(data['calcium']),
                str(data['soilMoisture']),
                str(data['waterLavel']),
                str(data['phLavel'])
            )
            
            cursor.execute(sql, values)
            
            fieldDataDB.commit()
        except Exception as e:
            logging.exception(e)
        finally:
            cursor.close()
            
            
    def getFieldData(self, tableName:str):
        _, cursor=self.connectDB()
        date=[]
        potassium=[]
        nitrogen=[]
        calcium=[]
        temperature=[]
        humidity=[]
        soilMoisture=[]
        waterLevel=[]
        
        try:
            tableName="table_".join(tableName)
            sql=f'''
                SELECT * FROM {tableName}
            '''
            cursor.execute(sql)
            rows=cursor.fetchall()
            
            for row in rows:
                date.append(row[0])
                temperature.append(row[1])
                humidity.append(row[2])
                potassium.append(row[3])
                nitrogen.append(row[4])
                calcium.append(row[5])
                soilMoisture.append(row[6])
                waterLevel.append(row[7])
                
            iotData=IoTDataDict(date=date, temperature=temperature, humidity=humidity, potassium=potassium, nitrogen=nitrogen, calcium=calcium, soilMoisture=soilMoisture, waterLevel=waterLevel)
        except Exception as e:
            logging.exception(e)        
        finally:
            cursor.close()
            
        return iotData
            
            