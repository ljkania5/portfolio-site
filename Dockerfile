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

# Copy ONLY requirements.txt first, then install dependencies.
# This is the layer-caching trick: as long as requirements.txt doesn't change,
# Docker reuses the cached "pip install" layer on rebuilds — huge speedup.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of the application code.
# This is the layer that changes most often, so it's last.
COPY ./app ./app

# Document that the container listens on port 8000.
# (This is informational — it doesn't actually publish the port.)
EXPOSE 8000

# The command that runs when the container starts.
# Note --host 0.0.0.0: inside a container, "localhost" only means the container itself,
# so we have to bind to all interfaces for the host machine to reach us.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]