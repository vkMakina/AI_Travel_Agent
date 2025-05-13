# Dockerfile – Builds FastAPI + Streamlit in one container

# Base Python image
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy code and install deps
COPY . .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose both ports
EXPOSE 8000 8501

# Command to run both backend and frontend using bash
CMD ["bash", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 8000 & streamlit run frontend/app.py --server.port 8501"]
