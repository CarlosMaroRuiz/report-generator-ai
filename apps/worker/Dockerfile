FROM python:3.12-slim AS base
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl fonts-dejavu-core && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir -e . && pip install --no-cache-dir watchfiles
ENV PYTHONPATH=/app/src
RUN useradd -m w && chown -R w /app
USER w
CMD ["python", "-m", "worker.main"]

FROM base AS dev
CMD ["python", "-m", "worker.main"]

FROM base AS prod
RUN pip uninstall -y watchfiles
CMD ["python", "-m", "worker.main"]