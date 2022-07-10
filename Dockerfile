# syntax=docker/dockerfile:1

FROM python:3-slim-buster

WORKDIR /app

# ENV VIRTUAL_ENV=/opt/venv
# RUN python3 -m venv $VIRTUAL_ENV
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app.py .
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]