#syntax=docker/dockerfile:1

FROM python:3.11-bookworm
# Path: /app
WORKDIR /app

# Path: /app/requirements.txt
COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt

# Path: /app
COPY . .

# Run the application
EXPOSE 5000

# Environment variables
ENV FLASK_SECRET=sf34GSEWh54whSE%Hh5S%sy5hsh5sh%RHSh%RH^JDFTUKFy8

CMD ["gunicorn", "-c", "gunicorn.conf.py", "-p", "5000:5000", "app:app"]