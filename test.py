from consul import Consul
import json

def read_from_consul_kv():
    consul = Consul(host='localhost', port=8500)

    index, data = consul.kv.get('config/counting')

    if data:
        json_data = data['Value'].decode('utf-8')
        config = json.loads(json_data)
        print("Read config from Consul KV store:", config)
    else:
        print("Key not found in Consul KV store.")

read_from_consul_kv()
