# base image
FROM python:3.10

# sets working directory
WORKDIR /app

# copies 'requirements.txt'
COPY requirements.txt /app/requirements.txt

# upgrades pip & installs Python dependencies specified in 'requirements.txt'
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# exposes port 8100 to allow external access to the application running in the container
EXPOSE 8100

# copies the entire contents of the current directory to the /app directory in the container
COPY ./ /app

# specifies the default command to run when the container starts
CMD ["python", "main.py"]


# $ docker build -t event-planner-api .