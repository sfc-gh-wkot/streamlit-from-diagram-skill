# SPCS (Snowpark Container Services) Setup Guide

## ⚠️ Raw SPCS vs SiS Container

**This guide is for Raw SPCS (CREATE SERVICE).** For SiS Container (CREATE STREAMLIT), use system resources instead:

| Deployment | Compute Pool | Warehouse |
|------------|--------------|-----------|
| **SiS Container** | `SYSTEM_COMPUTE_POOL_CPU` ✅ | `SYSTEM$STREAMLIT_NOTEBOOK_WH` ✅ |
| **Raw SPCS** | Custom pool required | N/A |

## Prerequisites (Raw SPCS Only)

Before deploying a raw SPCS service, ensure:

1. **Account Permissions** - SPCS enabled, CREATE COMPUTE POOL and CREATE SERVICE privileges
2. **Infrastructure** - Image repository and **custom** compute pool created
3. **Local Tools** - Docker Desktop and Snowflake CLI (`snow`) installed

## One-Time Setup (SQL)

```sql
-- 1. Create image repository
CREATE IMAGE REPOSITORY IF NOT EXISTS my_db.my_schema.my_repo;

-- 2. Show repository URL (needed for docker push)
SHOW IMAGE REPOSITORIES;

-- 3. Create compute pool (REQUIRED for raw SPCS - SYSTEM_COMPUTE_POOL_CPU won't work)
-- ⚠️ Note: SYSTEM_COMPUTE_POOL_CPU works for SiS Container (CREATE STREAMLIT)
--          but NOT for raw SPCS (CREATE SERVICE)
CREATE COMPUTE POOL IF NOT EXISTS my_compute_pool
  MIN_NODES = 1
  MAX_NODES = 2
  INSTANCE_FAMILY = CPU_X64_XS
  AUTO_RESUME = TRUE
  AUTO_SUSPEND_SECS = 300;
```

## Instance Families

| Family | CPU | Memory | Use Case |
|--------|-----|--------|----------|
| CPU_X64_XS | 1 | 6 GB | Small Streamlit apps |
| CPU_X64_S | 3 | 13 GB | Medium workloads |
| CPU_X64_M | 6 | 28 GB | Large data processing |

## Dockerfile Best Practices

```dockerfile
FROM python:3.11-slim
RUN pip install uv
WORKDIR /app
COPY requirements-spcs.txt .
RUN uv pip install --system -r requirements-spcs.txt
COPY streamlit_app.py .
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1
CMD ["streamlit", "run", "streamlit_app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
```

## Service Specification (spec.yaml)

```yaml
spec:
  containers:
    - name: streamlit
      image: /MY_DB/MY_SCHEMA/MY_REPO/app_name:latest
      env:
        STREAMLIT_SERVER_PORT: "8501"
        STREAMLIT_SERVER_HEADLESS: "true"
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
```

## Deployment Commands

```bash
# 1. Build for correct architecture (CRITICAL)
docker build --platform linux/amd64 -t app_name:latest .

# 2. Login to Snowflake registry
snow spcs image-registry login --connection my_conn

# 3. Tag and push
docker tag app_name:latest <registry>/app_name:latest
docker push <registry>/app_name:latest

# 4. Create service
snow sql -c my_conn -q "
CREATE OR REPLACE SERVICE my_service
  IN COMPUTE POOL my_compute_pool
  FROM SPECIFICATION $$
$(cat spec.yaml)
$$;
"
```

## Monitoring

```sql
-- Service status
SHOW SERVICES;
DESCRIBE SERVICE my_service;

-- Container logs
SELECT * FROM TABLE(GET_SERVICE_LOGS('my_service', 'streamlit'))
ORDER BY timestamp DESC LIMIT 100;

-- Get endpoint URL
SHOW ENDPOINTS IN SERVICE my_service;
```

## Cleanup

```sql
ALTER SERVICE my_service SUSPEND;
DROP SERVICE my_service;
ALTER COMPUTE POOL my_compute_pool SUSPEND;
DROP COMPUTE POOL my_compute_pool;
```
