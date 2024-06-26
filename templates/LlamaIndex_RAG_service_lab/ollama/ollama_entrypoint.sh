#!/bin/bash

# # Wait for the ollama application to start
# until curl -s http://localhost:11434 > /dev/null; do
#   echo "Waiting for ollama to start..."
#   sleep 5
# done

# # Run the ollama command
# ollama run llama3

echo "Starting Ollama server..."
ollama serve &


echo "Waiting for Ollama server to be active..."
while [ "$(ollama list | grep 'NAME')" == "" ]; do
  sleep 1
done

ollama pull llama3
