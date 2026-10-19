FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy configuration and project definition files
COPY pyproject.toml README.md ./

# Install python dependencies (pip install .)
RUN pip install --no-cache-dir .

# Copy source code, dbt project, and entrypoint
COPY src/ ./src/
COPY transform/ ./transform/
COPY entrypoint.sh ./

RUN chmod +x /app/entrypoint.sh

ENV PORT=8000
EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["api"]
