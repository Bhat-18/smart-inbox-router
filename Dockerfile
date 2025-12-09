# 1. Use a lightweight, official Python image (Linux-based)
FROM python:3.9-slim

# 2. Set the working directory inside the container to /app
WORKDIR /app

# 3. Copy just the requirements file first (this speeds up re-builds)
COPY requirements.txt .

# 4. Install the libraries inside the container
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of your source code into the container
COPY . .

# 6. The command to run when the container starts
CMD ["python", "src/main.py"]