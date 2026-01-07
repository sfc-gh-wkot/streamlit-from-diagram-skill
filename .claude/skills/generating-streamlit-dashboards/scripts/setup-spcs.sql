-- SPCS Infrastructure Setup (Raw SPCS / CREATE SERVICE only)
-- Replace: MY_DB, MY_SCHEMA, MY_REPO, MY_POOL
--
-- ⚠️ NOTE: This setup is for RAW SPCS (CREATE SERVICE) only.
-- For SiS Container (CREATE STREAMLIT), use system resources:
--   COMPUTE_POOL = SYSTEM_COMPUTE_POOL_CPU
--   QUERY_WAREHOUSE = SYSTEM$STREAMLIT_NOTEBOOK_WH

-- 1. Create image repository
CREATE IMAGE REPOSITORY IF NOT EXISTS MY_DB.MY_SCHEMA.MY_REPO;
SHOW IMAGE REPOSITORIES;

-- 2. Create compute pool (REQUIRED for raw SPCS - SYSTEM_COMPUTE_POOL_CPU won't work for CREATE SERVICE)
CREATE COMPUTE POOL IF NOT EXISTS MY_POOL
  MIN_NODES = 1
  MAX_NODES = 2
  INSTANCE_FAMILY = CPU_X64_XS
  AUTO_RESUME = TRUE
  AUTO_SUSPEND_SECS = 300;

-- 3. Create service (after pushing image)
CREATE SERVICE my_streamlit_service
  IN COMPUTE POOL MY_POOL
  FROM SPECIFICATION $$
spec:
  containers:
    - name: streamlit
      image: /MY_DB/MY_SCHEMA/MY_REPO/app_name:latest
      env:
        STREAMLIT_SERVER_PORT: "8501"
      readinessProbe:
        port: 8501
        path: /_stcore/health
      resources:
        requests:
          memory: 512Mi   # Reduced to avoid capacity issues
          cpu: 0.25
        limits:
          memory: 1Gi
          cpu: 0.5
  endpoints:
    - name: streamlit
      port: 8501
      public: true
$$;

-- 4. Check status
SHOW SERVICES;
SHOW ENDPOINTS IN SERVICE my_streamlit_service;
SELECT * FROM TABLE(GET_SERVICE_LOGS('my_streamlit_service', 'streamlit')) LIMIT 50;

-- 5. Cleanup
-- DROP SERVICE my_streamlit_service;
-- ALTER COMPUTE POOL MY_POOL SUSPEND;
-- DROP COMPUTE POOL MY_POOL;
