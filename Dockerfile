# Pull base image
FROM python:3.6

# Install psql so that "python manage.py dbshell" works
# RUN apt-get update && apt-get install -y --no-install-recommends apt-utils postgresql-client
# RUN apt-get install -y --no-install-recommends libpq-dev postgresql-client
# RUN apt-get install -y --no-install-recommends postgresql-client
# RUN apk add postgresql-dev gcc python3-dev musl-dev

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Copy project
COPY . /app/