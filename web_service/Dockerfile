FROM python:3.9.7-slim

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app
RUN mkdir model_element

COPY ["Pipfile", "Pipfile.lock", "./"]
RUN pipenv install --system --deploy

COPY ["/get_action.py", "./"]

COPY ["/model_element/model.py", "/model_element/preprocess.py", "/model_element/qtable.bin", "./model_element/"]

EXPOSE 9696

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "get_action:app" ]