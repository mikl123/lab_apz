import requests

# # Post requests
for i in range(10):
    print("Recived status from facade-service post", requests.post("http://localhost:5000/send", json={"msg":f"message {i}"}))

# Get request message service 
response = requests.get("http://localhost:5004/get")
response = requests.get("http://localhost:5005/get")

# # Get request facade service
response = requests.get("http://localhost:5000/get")
print("Recived status from facade-service get", response)
print("Recieved data from facade-service get", response.json())
