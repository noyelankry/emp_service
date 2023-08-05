FROM python:3.8-slim

# working directory in the container
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/

# env variables
ENV FLASK_APP=app.py
ENV DATABASE_URI=sqlite:///mydatabase.db
ENV SECRET_KEY=mysecretkey

# Port
EXPOSE 5000

# command to run application
CMD ["flask", "run", "--host", "0.0.0.0"]
