FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

COPY ./app ./app

COPY ./config ./config 

COPY ./tests ./tests

COPY requirements.txt requirements.txt

RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt




#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]