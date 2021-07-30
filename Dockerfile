FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt
ADD . /app/
CMD gunicorn -b 0.0.0.0:8000 movies_project.wsgi
