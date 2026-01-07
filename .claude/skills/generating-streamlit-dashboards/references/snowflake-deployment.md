# Snowflake Deployment Guide

Complete guide for deploying Streamlit apps to Snowflake environments.

## Contents

- [Security](#security)
- [Deployment Triggers](#deployment-triggers)
- [Pre-Deployment Validation](#pre-deployment-validation)
- [PAT Token Discovery](#pat-token-discovery)
- [Connection Configuration](#connection-configuration)
- [SiS Warehouse Deployment](#sis-warehouse-deployment)
- [SiS Container Deployment](#sis-container-deployment)
- [SPCS Deployment](#spcs-deployment)
- [Naming Convention](#naming-convention)
- [Database Safety Rules](#database-safety-rules)
- [Troubleshooting](#troubleshooting)

---

## Security

**See `references/security-rules.md` for all security guidelines.**

---

## Deployment Triggers

**Deploy only when user EXPLICITLY says:**
- "deploy to snowflake" → All 3 environments
- "deploy to sis warehouse" → SiS Warehouse only
- "deploy to sis container" → SiS Container only
- "deploy to spcs" → SPCS only

**NOT a trigger:** "can be deployed to X, Y, Z" (describes CAPABILITY)

---

## Pre-Deployment Validation

Before starting ANY Snowflake deployment:

```bash
# 1. Verify localhost works
curl -sf http://localhost:8501/_stcore/health && echo "✅ Localhost OK"

# 2. Check snow CLI is installed
snow --version || echo "Please install: pip install snowflake-cli-labs"

# 3. List available connections
snow connection list
```

---

## PAT Token Discovery

**Run ONLY when user requests deployment:**

```bash
# Search common locations
for path in ".env" "../.env" "../../.env" "$HOME/.env" "$HOME/.snowflake/.env"; do
    if [ -f "$path" ] && grep -qE "^SNOWFLAKE_PAT=" "$path" 2>/dev/null; then
        echo "✅ Found PAT at: $path"
        ENV_PATH="$path"
        break
    fi
done

# If not found, ask user
if [ -z "$ENV_PATH" ]; then
    echo "❌ No .env with SNOWFLAKE_PAT found."
    echo "Please create .env with: SNOWFLAKE_PAT=<your-token>"
fi
```

### Extract Token (Safe)

```bash
# Extract without displaying content
grep -E "^SNOWFLAKE_PAT=" "${ENV_PATH:-.env}" \
    | head -1 | cut -d'=' -f2- > .snowflake-token
chmod 600 .snowflake-token

# Verify size only
echo "Token file: $(wc -c < .snowflake-token) bytes"
```

---

## Connection Configuration

### Option 1: Reuse Existing Connection (Preferred)

```bash
snow connection list
snow streamlit deploy --connection EXISTING_CONN
```

### Option 2: Create via config.toml

```bash
mkdir -p ~/.snowflake
cat >> ~/.snowflake/config.toml << EOF

[connections.myconn]
account = "xxx-yyy"
user = "myuser"
authenticator = "PROGRAMMATIC_ACCESS_TOKEN"
token_file_path = "$(pwd)/.snowflake-token"
EOF
```

### Option 3: External Browser Auth

```bash
cat >> ~/.snowflake/config.toml << EOF

[connections.myconn]
account = "xxx-yyy"
user = "myuser"
authenticator = "externalbrowser"
warehouse = "COMPUTE_WH"
database = "MY_DB"
schema = "PUBLIC"
EOF
```

### Test Connection

```bash
snow connection test -c <connection_name>
```

---

## SiS Warehouse Deployment

Uses Conda packages from `snowflake` channel.

### Files Required

- `streamlit_app.py`
- `environment.yml` (NO version specifiers!)
- `snowflake.yml`

### Deploy Command

```bash
# Ensure database exists
snow sql -c <conn> -q "CREATE DATABASE IF NOT EXISTS STREAMLIT_APPS"

# Deploy
snow streamlit deploy app_warehouse --connection <conn> --replace
```

### environment.yml Rules

```yaml
# ❌ WRONG - Version operators not allowed
dependencies:
  - streamlit>=1.35.0
  - pandas==2.0.0

# ✅ CORRECT - Plain package names only
dependencies:
  - streamlit
  - pandas
  - numpy
  - altair
```

---

## SiS Container Deployment

Uses pip packages, runs on compute pool.

**⚠️ Cannot use `snow streamlit deploy` - must use SQL.**

### Files Required

- `streamlit_app.py`
- `requirements.txt`

### Deploy Commands

```bash
# Generate timestamp
TIMESTAMP=$(date +%Y_%m_%d_%H_%M)
APP_NAME="MY_DASHBOARD_${TIMESTAMP}"

# Stage files
snow stage copy streamlit_app.py @STAGE/app/ -c <conn> --overwrite
snow stage copy requirements.txt @STAGE/app/ -c <conn> --overwrite

# Create streamlit (use system resources)
snow sql -c <conn> -q "
    CREATE OR REPLACE STREAMLIT DB.SCHEMA.${APP_NAME}
        FROM '@STAGE/app/'
        MAIN_FILE = 'streamlit_app.py'
        TITLE = '${TIMESTAMP} My Dashboard (Container)'
        QUERY_WAREHOUSE = SYSTEM\$STREAMLIT_NOTEBOOK_WH
        COMPUTE_POOL = SYSTEM_COMPUTE_POOL_CPU;
"
```

### System Resources (Recommended)

| Resource Type | Prefer (System) | Avoid (Custom) |
|---------------|-----------------|----------------|
| Compute Pool | `SYSTEM_COMPUTE_POOL_CPU` | Custom pools (quota limits) |
| Warehouse | `SYSTEM$STREAMLIT_NOTEBOOK_WH` | Custom warehouses |

---

## SPCS Deployment

Full Docker container on Snowpark Container Services.

### Files Required

- `streamlit_app.py`
- `spcs/Dockerfile`
- `spcs/requirements-spcs.txt`
- `spcs/spec.yaml` (reference only)

### Deploy Commands

```bash
TIMESTAMP=$(date +%Y_%m_%d_%H_%M)

# Build Docker image
cd spcs && cp ../streamlit_app.py .
docker build --platform linux/amd64 -t app:${TIMESTAMP} .

# Login and push
snow spcs image-registry login --connection <conn>
docker tag app:${TIMESTAMP} <registry>/app:${TIMESTAMP}
docker push <registry>/app:${TIMESTAMP}

# Create service (inline spec)
snow sql -c <conn> -q "
CREATE SERVICE DB.SCHEMA.MY_SERVICE_${TIMESTAMP}
    IN COMPUTE POOL MY_COMPUTE_POOL
    FROM SPECIFICATION \$\$
spec:
  containers:
    - name: streamlit
      image: /DB/SCHEMA/REPO/app:${TIMESTAMP}
      readinessProbe:
        port: 8501
        path: /_stcore/health
      resources:
        requests:
          memory: 512Mi
          cpu: 0.25
        limits:
          memory: 1Gi
          cpu: 0.5
  endpoints:
    - name: streamlit
      port: 8501
      public: true
\$\$;
"
```

### Wait for Endpoint

```bash
SERVICE="DB.SCHEMA.MY_SERVICE"
echo "⏳ Waiting for endpoint (2-5 minutes)..."

for i in {1..30}; do
    RESULT=$(snow sql -c <conn> -q "SHOW ENDPOINTS IN SERVICE $SERVICE" --format json 2>/dev/null)
    if echo "$RESULT" | grep -q "snowflakecomputing.app"; then
        URL=$(echo "$RESULT" | grep -o '"ingress_url":"[^"]*"' | cut -d'"' -f4)
        echo "✅ Endpoint ready: https://$URL"
        break
    fi
    echo "  Still provisioning... ($i/30)"
    sleep 10
done
```

---

## Naming Convention

**Use underscores, NOT hyphens (Snowflake identifiers don't allow hyphens).**

```bash
TIMESTAMP=$(date +%Y_%m_%d_%H_%M)

# Name: APP_NAME_2026_01_07_14_30
# Title: "2026_01_07_14_30 App Title (Warehouse)"
```

| Variant | Name Pattern | Title Pattern |
|---------|--------------|---------------|
| SiS Warehouse | `APP_NAME_{timestamp}` | `"{timestamp} App Title (Warehouse)"` |
| SiS Container | `APP_NAME_{timestamp}` | `"{timestamp} App Title (Container)"` |
| SPCS | `app_name_{timestamp}` | `"{timestamp} App Title (SPCS)"` |

---

## Database Safety Rules

**DO NO HARM to user databases.**

### ✅ ALLOWED Operations

```sql
-- Creating dashboard-specific objects
CREATE DATABASE IF NOT EXISTS MY_DASHBOARD_DB;
CREATE SCHEMA IF NOT EXISTS MY_DASHBOARD_DB.APP_SCHEMA;
CREATE STAGE IF NOT EXISTS ...;
CREATE STREAMLIT ...;
CREATE SERVICE ...;

-- Reading Snowflake system info
SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY;
SHOW WAREHOUSES;
SHOW COMPUTE POOLS;
```

### ❌ FORBIDDEN Operations

```sql
-- Reading/exploring user data
SHOW DATABASES;                              -- Don't explore
SELECT * FROM OTHER_DB.SCHEMA.TABLE;         -- Don't read user data
USE DATABASE PRODUCTION_DB;                  -- Don't access other databases

-- Modifying anything outside dashboard scope
DROP DATABASE ...;
DROP TABLE ...;
DELETE FROM ...;
UPDATE ... SET ...;
TRUNCATE TABLE ...;
```

**🛡️ If in doubt, DON'T DO IT. Ask the user first.**

---

## Troubleshooting

### Connection Prompt Failure

**Error:** `Warning: Password input may be echoed. Aborted.`

**Fix:** Edit config.toml directly instead of `snow connection add`.

### Version Specifiers in environment.yml

**Error:** `Anaconda dependency names must be lowercase characters, numbers or one of [.-_]`

**Fix:** Remove `>=`, `==`, `<` from environment.yml - use plain names only.

### snowflake.yml runtime Field

**Error:** `Extra inputs are not permitted. You provided field 'entities.app.streamlit.runtime'`

**Fix:** Deploy SiS Container via SQL, not snowflake.yml.

### SPCS "No service hosts found"

**Cause:** Service still starting or endpoint not provisioned.

**Fix:** Wait 2-5 minutes. Check:
```sql
SHOW SERVICES LIKE '%MY_SERVICE%';
SELECT * FROM TABLE(GET_SERVICE_LOGS('MY_SERVICE', 'streamlit'));
SHOW ENDPOINTS IN SERVICE MY_SERVICE;
```

### SPCS "Insufficient CPU resources"

**Fix:** Reduce resource requests or use different compute pool:
```yaml
resources:
  requests:
    memory: 512Mi  # Reduced
    cpu: 0.25      # Reduced
```

See `references/troubleshooting.md` for more detailed solutions.
