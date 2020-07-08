FROM python:3.7-slim

ENV APP_SETTINGS=K8SDevelopmentConfig

RUN pip install pipenv
RUN apt-get update -y && apt-get install -y curl git

WORKDIR /home/ops-tool
CMD ["python3", "run.py"]

COPY Pipfile* /home/ops-tool/
RUN pipenv install --deploy --system
RUN apt-get remove -y --purge git

COPY . /home/ops-tool
EXPOSE 8003
