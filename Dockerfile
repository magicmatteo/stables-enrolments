FROM tiangolo/uwsgi-nginx-flask:python3.9
ENV STATIC_URL /static
ENV STATIC_PATH /app/mainapp/static
COPY ./requirements.txt /tmp/requirements.txt

RUN rm /app/main.py
RUN rm /app/uwsgi.ini

COPY mainapp /app/mainapp
COPY main.py /app/
COPY uwsgi.ini /app/
WORKDIR /app
# Make /app/* available to be imported by Python globally to better support several use cases like Alembic migrations.
ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r /tmp/requirements.txt