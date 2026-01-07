# Security Rules

Single source of truth for all security guidelines in this skill.

## Contents

- [Credential Handling](#credential-handling)
- [Required .gitignore Entries](#required-gitignore-entries)
- [Safe Token Extraction](#safe-token-extraction)
- [Database Safety](#database-safety)
- [If Credentials Are Accidentally Committed](#if-credentials-are-accidentally-committed)

---

## Credential Handling

### NEVER Do These

1. **NEVER read passwords or tokens** - don't `cat`, `read_file`, `grep -o`, or view credential file contents
2. **NEVER echo/print credentials** - even for "debugging" or "verification"
3. **NEVER log credentials** - no print statements, no logging calls
4. **NEVER commit credentials** - verify `.gitignore` before every `git add`

### ALWAYS Do These

1. **ALWAYS create `.gitignore` first** - before any other file operations
2. **ALWAYS use file operations** - `cp`, `mv`, `chmod` without reading content
3. **ALWAYS verify token file size** - `wc -c < file` not `cat file | wc`
4. **ALWAYS set restrictive permissions** - `chmod 600` on token files

---

## Required .gitignore Entries

Every project MUST include these patterns:

```gitignore
# Environment files
.env
.env.*
*.env

# Streamlit secrets
.streamlit/secrets.toml
secrets.toml

# Snowflake tokens
.snowflake-token
*.token
*.pat

# Cloud credentials
**/credentials.json
**/service_account*.json

# Private keys
private_key*.pem
*.p8
*.p12
```

---

## Safe Token Extraction

When deployment is explicitly requested:

```bash
# SAFE: Extract without displaying content
grep -E "^SNOWFLAKE_PAT=" "${ENV_PATH:-.env}" \
    | head -1 | cut -d'=' -f2- > .snowflake-token
chmod 600 .snowflake-token

# SAFE: Verify size only (not content)
echo "Token file: $(wc -c < .snowflake-token) bytes"
```

---

## Database Safety

### Allowed Operations

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

### Forbidden Operations

```sql
-- NEVER explore user data
SHOW DATABASES;
SELECT * FROM OTHER_DB.SCHEMA.TABLE;
USE DATABASE PRODUCTION_DB;

-- NEVER modify existing data
DROP DATABASE ...;
DROP TABLE ...;
DELETE FROM ...;
UPDATE ... SET ...;
TRUNCATE TABLE ...;
```

**If in doubt, DON'T DO IT. Ask the user first.**

---

## If Credentials Are Accidentally Committed

1. **Rotate credentials immediately** - they are compromised
2. Use `git filter-branch` or BFG Repo-Cleaner to remove from history
3. Force push to all remotes
4. Notify security team if applicable
