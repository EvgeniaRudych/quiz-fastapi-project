FROM python:3.8
WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY ./src /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
