# SPCS Streamlit Container
# Build: docker build --platform linux/amd64 -t app:latest .
#
# Uses Python 3.13 and latest Streamlit from PyPI
# Reference: https://pypi.org/project/streamlit/

FROM python:3.13-slim

# Install uv for fast dependency management
RUN pip install uv

# Set working directory
WORKDIR /app

# Copy requirements first (layer caching)
COPY requirements-spcs.txt .

# Install dependencies using uv
RUN uv pip install --system -r requirements-spcs.txt

# Copy application code
COPY streamlit_app.py .

# Expose Streamlit port
EXPOSE 8501

# Health check for SPCS readiness probe
HEALTHCHECK --interval=30s --timeout=10s CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "streamlit_app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
