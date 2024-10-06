FROM python

# Setup environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Set the working directory
WORKDIR /app

#Install dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt

#Copy the project
COPY . .
