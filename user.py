import requests

# Post requests
# for i in range(10):
#     print("Recived status from facade-service post", requests.post("http://localhost:5000/send", json={"msg":f"message {i}"}))

# Get request
response = requests.get("http://localhost:5000/get")
print("Recived status from facade-service get", response)
print("Recieved data from facade-service get", response.json())
