FROM python:3.11-slim

WORKDIR /app
COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv

RUN pipenv install --deploy --ignore-pipfile
COPY . /app/

EXPOSE 8000

# Set perintah untuk menjalankan aplikasi Flask
CMD ["pipenv", "run", "python", "app.py"]
