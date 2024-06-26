# FROM ollama/ollama

# # Install curl & rm the apt cache for a smaller image
# RUN apt-get update && apt-get install -y \
#     curl \
#     && rm -rf /var/lib/apt/lists/*

# # Copy the start script into the container
# COPY start_ollama.sh /start_ollama.sh

# # Make the script executable
# RUN chmod +x /start_ollama.sh

# # Set the entrypoint to the script
# ENTRYPOINT ["/bin/bash", "/start_ollama.sh"]

FROM ollama/ollama

WORKDIR /app

COPY ollama_entrypoint.sh /tmp/ollama_entrypoint.sh

WORKDIR /tmp

RUN chmod +x ollama_entrypoint.sh \ 
    && ./ollama_entrypoint.sh

EXPOSE 11434