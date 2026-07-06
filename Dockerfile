# 1. Use an official, lightweight Python environment
FROM python:3.11-slim

# 2. Set the working folder inside the container
WORKDIR /app

# 3. Install the official Google Gen AI SDK
RUN pip install --no-cache-dir google-genai

# 4. Copy our app.py file from your Mac into the container
COPY app.py .

# 5. Tell the container to run our script when it boots up
CMD ["python", "app.py"]