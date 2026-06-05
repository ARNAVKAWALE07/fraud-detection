#python enve
FROM python:3.10-slim

#working dict
WORKDIR /app

#copy and install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#copy app code
COPY app/ .

#expose port
EXPOSE 8080

#cmd to run container 
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port","8080"]
