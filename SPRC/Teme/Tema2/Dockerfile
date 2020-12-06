FROM python:latest
COPY requirements.txt /tmp
RUN pip install -U setuptools
RUN pip install -r /tmp/requirements.txt
COPY /src /app
WORKDIR /app

EXPOSE 5001
CMD ["python", "main.py"]
