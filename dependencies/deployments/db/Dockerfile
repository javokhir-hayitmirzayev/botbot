FROM postgres:16-alpine

# Create directory for initialization scripts
RUN mkdir -p /docker-entrypoint-initdb.d

# Copy initialization scripts
COPY ./docker-entrypoint-initdb.d/ /docker-entrypoint-initdb.d/

# Set default environment variables (will be overridden by docker-compose)
ENV POSTGRES_DB=${DB_NAME:-postgres}
ENV POSTGRES_USER=${DB_USER:-postgres}
ENV POSTGRES_PASSWORD=${DB_PASSWORD:-postgres}

# Expose PostgreSQL port
EXPOSE 5432