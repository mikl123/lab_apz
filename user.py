import requests
from consul import Consul
import random

consul = Consul(host='localhost', port=8500)
def get_ip_address(service_name):
    """This functions seeks int consule available adresses for give service_name"""
    try:
        services = consul.health.service(service_name)
        if not services:
            print(f"No services found for '{service_name}'")
            return None
        ip_port_pairs = []
        for service in services[1]:
            port = service["Service"]["Port"]
            if service['Checks'][-1]['Status'] == 'passing':
                ip_port_pairs.append(port)
            
        if len(ip_port_pairs) >= 1:
            selected_port = random.choice(ip_port_pairs)
        print("All ports available for " ,service_name , " " ,  ip_port_pairs)
        return f"http://localhost:{selected_port}"
    except Exception as e:
        print(f"Error getting IP address for service '{service_name}': {str(e)}")
        return None


address = get_ip_address("facade-service")
for i in range(10):
    print("Recived status from facade-service post", requests.post(f"{address}/send", json={"msg":f"message {i}"}))

# Get request message service 

# response = requests.get("http://localhost:5004/get")
# response = requests.get("http://localhost:5005/get")

# # Get request facade service
response = requests.get(f"{address}/get")
print("Recived status from facade-service get", response)
print("Recieved data from facade-service get", response.json())
