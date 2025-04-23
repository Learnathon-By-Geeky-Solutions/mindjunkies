FROM python:3.13-slim-bookworm

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# install uv
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

# copy project files
ADD . /app
WORKDIR /app


RUN uv sync --no-group dev --group prod --frozen

RUN chmod +x /app/entrypoint.sh
