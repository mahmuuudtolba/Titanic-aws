#---------------------------------
# Stage 1: The "Builder" Stage
#---------------------------------
# This stage will install all dependencies, download data, and train the model.
# It requires AWS credentials to be passed in securely during the build process.
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies needed for training
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgomp1 \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# Copy only the files needed for installation first, to leverage Docker cache
COPY setup.py .
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -e .

# Now copy the rest of the application code
COPY . .

# ---> This is the critical part <---
# We declare arguments to receive the AWS credentials securely at build time.
# NEVER set a default value for secrets here.
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY

# Set them as environment variables ONLY for the duration of this RUN command
# They will NOT be baked into the final image layer.
RUN --mount=type=secret,id=aws,target=/root/.aws/credentials \
    echo "Running training pipeline from GitHub Actions..." && \
    python pipeline/training_pipeline.py
    
#---------------------------------
# Stage 2: The "Final" Stage
#---------------------------------
# This is the lightweight production image. It does NOT have training libraries
# or AWS credentials. It only runs the Flask app.
FROM python:3.11-slim

WORKDIR /app

# Install only the dependencies needed for the application to run
# (This can be a much smaller requirements_app.txt file)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and the TRAINED MODEL from the builder stage.
COPY application.py .
COPY templates/ templates/
COPY --from=builder /app/artifacts/models/lgbm_model.pkl /app/artifacts/models/lgbm_model.pkl

# Expose the port
EXPOSE 5000

# Command to run ONLY the app
CMD ["python", "application.py"]