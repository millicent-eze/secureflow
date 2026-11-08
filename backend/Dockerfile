# ==========================================
# Stage 1: Build application dependencies
# ==========================================
FROM python:3.12-slim AS builder

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /app

# Create an isolated Python environment
RUN python -m venv $VIRTUAL_ENV

# Install application dependencies
COPY requirements.txt .

RUN python -m pip install --no-cache-dir --upgrade pip==26.3 \
    && python -m pip install --no-cache-dir -r requirements.txt


# ==========================================
# Stage 2: Production runtime image
# ==========================================
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Create a non-root user
RUN groupadd --system appgroup \
    && useradd --system --gid appgroup --create-home appuser

# Copy installed application dependencies from builder
COPY --from=builder /opt/venv /opt/venv

# Remove pip from the production image.
# It is only required during the build process.
RUN rm -rf \
    /opt/venv/lib/python3.12/site-packages/pip \
    /opt/venv/lib/python3.12/site-packages/pip-*.dist-info \
    /opt/venv/bin/pip \
    /opt/venv/bin/pip3 \
    /opt/venv/bin/pip3.12 \
    /usr/local/lib/python3.12/site-packages/pip \
    /usr/local/lib/python3.12/site-packages/pip-*.dist-info \
    /usr/local/bin/pip \
    /usr/local/bin/pip3 \
    /usr/local/bin/pip3.12

    # Apply available Debian security and package updates
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*
    
# Copy application files
COPY alembic.ini .
COPY alembic ./alembic
COPY app ./app

# Assign application ownership
RUN chown -R appuser:appgroup /app /opt/venv

# Run as a non-root user
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]