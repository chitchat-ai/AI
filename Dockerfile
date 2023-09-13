# Use an official Python runtime as a parent image
FROM python:3.11.4

# added to more easily and efficiently manage packages
COPY requirements.txt /app/

# Set the working directory in the container to /app
WORKDIR /app

# installs all of the required packages
RUN pip install -r requirements.txt

# Cache packages, they don't change often
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

# Add current directory contents into container by workdir
ADD . .

# Make port 8000 available for links and/or publish
EXPOSE 9000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000", "--reload", "--forwarded-allow-ips='*'", "--proxy-headers"]
