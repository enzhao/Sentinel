# Stage 1: Builder
# This stage installs dependencies into a virtual environment.
FROM python:3.13-slim AS builder

# Set environment variables, including the venv path
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Create venv and install dependencies
RUN python -m venv /opt/venv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---

# Stage 2: Final
# This stage creates the lean production image.
FROM python:3.13-slim

# Set the PATH to use the virtual environment's binaries
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application source code
COPY ./src .

# Expose the port and run the application
EXPOSE 8000
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000", "main:app"]

