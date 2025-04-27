#!/bin/bash

echo "Pulling the latest Consul Docker image..."
docker pull hashicorp/consul:latest

echo "Running the Consul server container..."
docker run -d \
  -p 8500:8500 \
  -p 8600:8600/udp \
  --name=badger \
  hashicorp/consul agent -server -ui -node=server-1 -bootstrap-expect=1 -client=0.0.0.0

echo "Running the Consul client container..."
docker run -d \
  --name=consule \
  hashicorp/consul agent -node=client-1 -retry-join=172.17.0.2

echo "Consul setup complete!"
