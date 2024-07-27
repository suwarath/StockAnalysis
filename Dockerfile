FROM python:3.9.7-slim

RUN pip install -U pip
RUN pip install pipenv

WORKDIR /app
RUN mkdir model_element

COPY ["Pipfile", "Pipfile.lock", "./"]
RUN pipenv install --system --deploy

COPY ["/web_service/get_action.py", "./"]

COPY ["/web_service/model_element/model.py", "/web_service/model_element/preprocess.py", "/web_service/model_element/qtable.bin", "./model_element/"]

EXPOSE 9696

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "get_action:app" ]