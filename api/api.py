from fastapi import FastAPI, Request
from pydantic import BaseModel

from measurements import download_speed,upload_speed

# Define a Pydantic model for Speed
class Speed(BaseModel):
    speed: float
# Initialize the app
app = FastAPI()

#def get_client_ip(request: Request):
#    return request.client.host

# GET Download Speed Endpoint
@app.get("/get_download_speed",
         summary="Retrieve Download Speed")
async def get_download_speed():
    down_speed = Speed(speed=download_speed())
    return down_speed

# GET Upload Speed Endpoint
@app.get("/get_upload_speed",
         summary="Retrieve Upload Speed")
async def get_upload_speed():
    upl_speed = Speed(speed=upload_speed())
    return upl_speed