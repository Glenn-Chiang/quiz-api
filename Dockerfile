FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Install web server
RUN pip install gunicorn

COPY . .

# Mark entrypoint file as executable
RUN chmod a+x entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]