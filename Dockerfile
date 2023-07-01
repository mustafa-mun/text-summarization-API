FROM python:3.10
EXPOSE 8080
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]