# Step 1: Use a Python base image
FROM python:3.13-slim

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Copy the requirements file into the container
COPY requirements.txt /app/

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the entire application into the container
COPY . /app/

# Step 6: Expose the port the app will run on
EXPOSE 8000

# Step 7: Define environment variables (optional but useful for production)
ENV PYTHONUNBUFFERED 1

# Step 8: Run the application (replace 'dev.py' with the script you use to start the app)
CMD ["fastapi", "dev", "tablemate_api/main.py", "--port", "8000", "--host", "0.0.0.0"]
