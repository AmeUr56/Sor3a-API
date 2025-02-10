import requests
import time

def download_speed(url="http://ipv4.download.thinkbroadband.com/10MB.zip", chunk_size=1024):
    start_time = time.time()

    # Number of chunks
    number_chunks = 0
    
    try:
        # Get Request to receive the data with stream method 
        response = requests.get(url, stream=True)
        for chunk in response.iter_content(chunk_size=chunk_size):
            # Update number of chunks
            number_chunks += 1
            # Stop after 5 Seconds
            if time.time() - start_time > 5:
                break
    except:
        return "Error"
    
    # Takend time
    taken_time = time.time() - start_time
    # Measure Download Speed in Mbps
    speed_mbps = (chunk_size*number_chunks * 8) / (taken_time * 1_000_000)

    return round(speed_mbps,3)

def upload_speed(server="http://speedtest.tele2.net/upload.php", data_size=1_000_000):    
    # Generate 5MB of example data
    data = b'0' * data_size 
    
    start_time = time.time()
    # POST Request to send data to a server
    response = requests.post(server, data=data)
    # Taken Time
    taken_time = time.time() - start_time
    try:
        response.raise_for_status()
    except:
        return "Error"
    # Measure Upload Speed in Mbps
    speed_mbps = (data_size * 8) / (taken_time * 1_000_000) 

    return round(speed_mbps, 3)


#print(f"Download Speed: {download_speed()}")
#print(f"Upload Speed: {upload_speed()}")

