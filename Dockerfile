FROM tiangolo/uwsgi-nginx-flask:latest
COPY ./app /app
ENV PYTHONPATH="$PYTHONPATH:/app"
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt