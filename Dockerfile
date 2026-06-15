# Start from an official Python base image.
# "slim" is a stripped-down Debian Linux with just enough to run Python.
# Pinning the exact version (3.11) keeps builds reproducible.
FROM python:3.11-slim

# Set the working directory inside the container.
# Every command after this runs from /app, and our app code will live there.
WORKDIR /app

# Set environment variables that make Python behave well in containers:
# - PYTHONDONTWRITEBYTECODE: don't write .pyc files (no need inside a container)
# - PYTHONUNBUFFERED: stream logs immediately instead of buffering them
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy pyproject.toml first, then install dependencies.
# This is the layer-caching trick: as long as pyproject.toml doesn't change,
# Docker reuses the cached "pip install" layer on rebuilds — huge speedup.
# A stub app/__init__.py lets pip read the project metadata without the full source.
COPY pyproject.toml .
RUN mkdir -p app && touch app/__init__.py
RUN pip install --no-cache-dir .

# Now copy the real app code, which overwrites the stub.
# This is the layer that changes most often, so it's last.
COPY ./app ./app

# Document that the container listens on port 8000.
# (This is informational — it doesn't actually publish the port.)
EXPOSE 8000

# The command that runs when the container starts.
# Note --host 0.0.0.0: inside a container, "localhost" only means the container itself,
# so we have to bind to all interfaces for the host machine to reach us.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]