import requests

# Post request
data = {"msg":"Hello this is message one"}
print("Recived status from facade-service post", requests.post("http://localhost:5000/send", json=data))

# Get request 
response = requests.get("http://localhost:5000/get")
print("Recived status from facade-service get", response)
print("Recieved data from facade-service get", response.json())


