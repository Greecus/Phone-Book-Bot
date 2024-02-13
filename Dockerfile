FROM python:3

WORKDIR /bot

RUN pip install --no-cache-dir pipenv

COPY Pipfile ./
COPY Pipfile.lock ./

RUN pipenv install --system --deploy --ignore-pipfile

COPY main.py .
COPY objects.py .

CMD [ "python", "./main.py" ]