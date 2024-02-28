FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

ENV POETRY_VIRTUALENVS_IN_PROJECT=true \ POETRY_NO_INTERACTION=1

# Set the working directory inside the container
WORKDIR /app

# Copy the poetry.lock and pyproject.toml files to the container
COPY poetry.lock pyproject.toml /app/


RUN apt-get update \
    && apt-get install --no-install-recommends -y \
    # deps for installing poetry
    curl \
    # deps for building python deps
    build-essential

# install poetry - respects $POETRY_VERSION & $POETRY_HOME
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3
ENV PATH="/opt/poetry/bin:$PATH"
RUN poetry config virtualenvs.create false

# copy project requirement files here to ensure they will be cached.

RUN poetry update
# Install project dependencies
RUN poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application code to the container
COPY . /app

# Define the command to run the FastAPI server
CMD ["./run.sh", "5005"]
