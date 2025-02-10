from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from databases import Database
from dotenv import load_dotenv
import os
from datetime import datetime

from measurements import download_speed,upload_speed
from scripts import get_client_ip,db_to_csv,db_to_json

# Define a Pydantic model for Speed
class Speed(BaseModel):
    test_id: int
    speed: float
    
# Initialize the app
app = FastAPI()
load_dotenv()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS"),
    allow_credentials=True,
    allow_methods=["GET"],
)

# Initialize Database
database = Database(os.getenv("DATABASE_URL"))

# Connect with database on startup
@app.on_event("startup")
async def connect_db():
    await database.connect()

# Create database schema on startup
@app.on_event("startup")
async def create_schema():
    query = """
        CREATE TABLE IF NOT EXISTS Test (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip_address TEXT NOT NULL,
            date_time DATETIME NOT NULL,
            download_speed FLOAT,
            upload_speed FLOAT
        )
    """
    await database.execute(query)
    
# Disconnect from the database on shutdown
@app.on_event("shutdown")
async def disconnect_db():
    await database.disconnect()
    
# GET Download Speed Endpoint
@app.get("/get_download_speed",#/{ip_address}",
         summary="Retrieve Download Speed")
async def get_download_speed(request:Request):#,ip_address:str):
    ip_address = get_client_ip(request)
    test_download_speed = download_speed()
    
    query = """
        INSERT INTO Test (ip_address,date_time,download_speed,upload_speed) 
        VALUES (:ip_address,:date_time,:download_speed,:upload_speed)
    """
    values = {"ip_address":ip_address,
              "date_time": datetime.now(),
              "download_speed":test_download_speed,
              "upload_speed":0.000}
    
    test_id = await database.execute(query=query, values=values)
    
    down_speed = Speed(test_id=test_id,speed=test_download_speed)    
    return down_speed

# GET Upload Speed Endpoint
@app.get("/get_upload_speed/{test_id}",
         summary="Retrieve Upload Speed")
async def get_upload_speed(test_id:int):
    test_upload_speed = upload_speed()
    
    query = """
        UPDATE Test 
        SET upload_speed = :upload_speed
        WHERE id = :test_id
    """
    values = {"upload_speed":test_upload_speed,"test_id":test_id}
    
    await database.execute(query=query, values=values)
    
    upl_speed = Speed(test_id=test_id,speed=test_upload_speed)
    return upl_speed

# Fetch all Tests
#@app.get("/tests")
#async def get_tests():
#    query = "SELECT * FROM Test"
#    results = await database.fetch_all(query=query)
#    return results

@app.get("/download_db/{file_type}")
async def download_db(file_type:str):
    match file_type:
        case "db":
            return FileResponse("speed_tests.db", media_type="application/octet-stream", filename="speed_tests.db")
        
        case "csv":
            # Convert DB file to CSV file
            db_to_csv()
        
            return FileResponse("speed_tests.csv", filename="speed_tests.csv")
        
        case "json":
            # Convert DB file to JSON file
            db_to_json()
            
            return  FileResponse("speed_tests.json", filename="speed_tests.json")
