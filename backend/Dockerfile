FROM python:3.11
WORKDIR /usr/src/backend
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 
RUN pip install --upgrade pip  
COPY . .
RUN pip install -r requirements.txt  

EXPOSE 9000
CMD ["python", "manage.py", "runserver", "9000"]
