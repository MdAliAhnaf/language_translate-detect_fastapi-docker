# Use the appropriate base image version
FROM tiangolo/uvicorn-gunicorn-fastapi:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file first and install the dependencie
COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt


COPY ./* /app

# Comment out this line as it should not be necessary if your main application code is inside the 'app' directory
# COPY ./app /app/app

# Define the command to run the application when the container starts
CMD [ "uvicorn" , "main:app" , "--host", "0.0.0.0", "--port", "80"]