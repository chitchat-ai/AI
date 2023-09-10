# Use an official Python runtime as a parent image
FROM python:3.11.4

# Set the working directory in the container to /app
WORKDIR /app

RUN pip install -U pytest pytest-docker

RUN pip install poetry==1.5.1

# Cache packages, they don't change often
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Add current directory contents into container by workdir
ADD . .

# Make port 8000 available for links and/or publish
EXPOSE 9000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--reload", "--forwarded-allow-ips='*'", "--proxy-headers"]
