FROM python3.11-slim

WORKDIR app

COPY app.py .

RUN pip install flask prometheus_client

EXPOSE 5001

CMD [python, app.py]
