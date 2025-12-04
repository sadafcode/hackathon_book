# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app


# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir pip==24.0 && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code

# Create a new, lean stage for the final image
FROM python:3.11-slim

WORKDIR /app

# Copy installed dependencies and binaries from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

# Expose port (Railway will set PORT env var)
EXPOSE 8000

# Run the application
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
