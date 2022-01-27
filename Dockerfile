FROM python:3.9.7
WORKDIR /Users/ctripp/github-repos/fanalytics
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
EXPOSE 8080
CMD gunicorn --bind 0.0.0.0:8080 --workers 2 application:server