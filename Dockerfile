FROM python:3.12

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV ADMIN_USERNAME admin
ENV ADMIN_PASSWD admin
ENV DB_HOST db
ENV DB_PORT 3306
ENV DB_USER root
ENV DB_PASSWD password
ENV DB_NAME matrimonio

ENTRYPOINT [ "gunicorn", "app:app", "--bind", "0.0.0.0:80" ]