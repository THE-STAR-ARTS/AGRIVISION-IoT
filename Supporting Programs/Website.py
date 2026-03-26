import network
import socket 

name = "Jason"
last_name = "Mguni"
gender = "Male"
height = "150"
phone_number = "0781 927 900"
emergency_number = "0774402304"
hospital = "Zimbabwe International Hospital"
location = "Zimbabwe, Harare" 
previous_illness = "Influenza"
current_illness = "Fever"
chronic_illness = "Diabetes"

# Connect to Wi-Fi (replace with your SSID and password)
ssid = 'Good Samaritan'
password = 'Samaritan123'
ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)
while not ap.active():
    pass
print("Connected")
print(ap.ifconfig())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Medical Data Form</title>
<style>
    body {
        font-family: Arial, sans-serif;
        background-color: teal; /* Light blue */
        margin: 0;
        padding: 20px;
    }
    
    .container {
        max-width: 600px;
        margin: auto;
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }
    
    h1, h2 {
        text-align: center;
        color: #336699; /* Dark blue */
    }
    
    form label {
        display: block;
        margin-top: 10px;
        color: #555;
    }
    
    form input, form select, form textarea {
        width: 100%;
        padding: 10px;
        margin-top: 5px;
        margin-bottom: 15px;
        border: 1px solid #ccc;
        border-radius: 5px;
    }
    
    button {
        display: block;
        width: 100%;
        padding: 10px;
        background-color: #007bff;
        color:   
     white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    
    button:hover {
        background-color:   
     #0056b3;
    }
    .hidden{
        color: black;
    }
    #display-data {
        margin-top: 20px;
        padding: 20px;
        border: 1px solid #ccc;
        border-radius: 5px;
        background-color: coral;
    }
    
    /* Animations */
    h1, h2, p span {
        transition: all 0.3s ease-in-out;
    }
    
    h1:hover, h2:hover, p span:hover {
        color: #007bff;
        transform: scale(1.05);
    }
</style>
</head>
<body>
<div id="display-data" class="hidden">
<h2>Submitted Medical Data</h2>
<p><strong>First Name:</strong> <span id="display-first-name">name_id</span></p>
<p><strong>Last Name:</strong> <span id="display-last-name">last_name_id</span></p>
<p><strong>Gender:</strong> <span id="display-gender">gender_id</span></p>
<p><strong>Height:</strong> <span id="display-height">height_id cm</span></p>
<p><strong>Phone Number:</strong> <span id="display-phone-number">number_id</span></p>
<p><strong>Emergency Phone Number:</strong> <span id="display-emergency-phone-number">emergency_id</span></p>
<p><strong>Hospital Name:</strong> <span id="display-hospital-name">hospital_id</span></p>
<p><strong>Location:</strong> <span id="display-location">location_id</span></p>
<p><strong>Previous Illnesses:</strong> <span id="display-previous-illnesses">prev_ill_id</span></p>
<p><strong>Current Illnesses:</strong> <span id="display-current-illnesses">curr_ill_id</span></p>
<p><strong>Chronic Conditions:</strong> <span id="display-chronic-conditions">chr_id</span></p>
</div>
</div>
</body>
</html>
"""

def WebSocket():
    try:
        conn, addr = s.accept()
        
        # Read and replace placeholders in HTML
        html = html_template
        html = html.replace("name_id", name)
        html = html.replace("last_name_id", last_name)
        html = html.replace("gender_id", gender)
        html = html.replace("height_id", height)
        html = html.replace("number_id", phone_number)
        html = html.replace("emergency_id", emergency_number)
        html = html.replace("hospital_id", hospital)
        html = html.replace("location_id", location)
        html = html.replace("prev_ill_id", previous_illness)
        html = html.replace("curr_ill_id", current_illness)
        html = html.replace("chr_id", chronic_illness)
        
        request = conn.recv(1024)
        request = str(request)
        conn.send(html.encode())
        
        conn.close()
        return html
    
    except OSError as e:
        conn.close()
        print("Connection closed")    

while True:
    WebSocket()