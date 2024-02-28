FROM python:3.11
WORKDIR /usr/src/backend
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 
RUN apt update && apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-venv -y
RUN pip install --upgrade pip  
COPY . .
EXPOSE 9000
RUN chmod +x docker_entry.sh

ENTRYPOINT ["/docker_entry.sh"]