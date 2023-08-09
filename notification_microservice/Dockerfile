FROM python:3.8-slim

# working directory in the container
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

# Expose the port that the application listens on.
EXPOSE 80

# Run the application.
CMD ["python", "app.py"]
