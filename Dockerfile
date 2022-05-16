FROM python:3.9 AS requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* .

RUN poetry export --format requirements.txt --output requirements.txt --without-hashes

# Use requirements.txt created in previous stage to install dependencies
FROM python:3.9

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]