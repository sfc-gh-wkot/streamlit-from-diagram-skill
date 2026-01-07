#!/bin/bash
# Initialize a new Streamlit project for Snowflake deployment
# Usage: ./init-project.sh <project_name> [app_name]

set -e

PROJECT_NAME=${1:-"streamlit-project"}
APP_NAME=${2:-"my_app"}

echo "Creating project: $PROJECT_NAME"
mkdir -p "$PROJECT_NAME/spcs"
cd "$PROJECT_NAME"

# Create pyproject.toml
cat > pyproject.toml << 'EOF'
[project]
name = "streamlit-app"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["streamlit==1.51.0", "pandas", "numpy", "altair"]

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W", "UP"]
EOF

# Create environment.yml
cat > environment.yml << 'EOF'
name: streamlit_env
channels:
  - snowflake
dependencies:
  - streamlit=1.51.0
  - pandas
  - numpy
  - altair
EOF

# Create requirements.txt
cat > requirements.txt << 'EOF'
streamlit==1.51.0
pandas
numpy
altair
EOF

# Create snowflake.yml
cat > snowflake.yml << EOF
definition_version: 2
entities:
  ${APP_NAME}_warehouse:
    type: streamlit
    identifier:
      name: ${APP_NAME^^}
    title: "${APP_NAME} Dashboard"
    query_warehouse: COMPUTE_WH
    main_file: streamlit_app.py
    artifacts:
      - streamlit_app.py
      - environment.yml
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
.venv/
__pycache__/
uv.lock
EOF

# Create spcs files
cat > spcs/Dockerfile << 'EOF'
FROM python:3.11-slim
RUN pip install uv
WORKDIR /app
COPY requirements-spcs.txt .
RUN uv pip install --system -r requirements-spcs.txt
COPY streamlit_app.py .
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
EOF

cp requirements.txt spcs/requirements-spcs.txt

cat > spcs/spec.yaml << EOF
spec:
  containers:
    - name: streamlit
      image: /DB/SCHEMA/REPO/${APP_NAME}:latest
      env:
        STREAMLIT_SERVER_PORT: "8501"
      readinessProbe:
        port: 8501
        path: /_stcore/health
      resources:
        requests:
          memory: 1Gi
          cpu: 0.5
        limits:
          memory: 2Gi
          cpu: 1
  endpoints:
    - name: streamlit
      port: 8501
      public: true
EOF

# Create minimal app
cat > streamlit_app.py << 'EOF'
import altair as alt
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide", page_title="Dashboard")
st.title("📊 Dashboard")

data = pd.DataFrame({"Category": ["A", "B", "C", "D"], "Value": [25, 55, 40, 30]})
chart = alt.Chart(data).mark_bar(color="#4A90D9").encode(
    x="Category:N", y="Value:Q", tooltip=["Category", "Value"]
).properties(height=300).interactive()
st.altair_chart(chart, use_container_width=True)
st.dataframe(data, use_container_width=True)
EOF

echo "✅ Project created: $PROJECT_NAME"
echo "Next: cd $PROJECT_NAME && uv sync && uv run streamlit run streamlit_app.py"
