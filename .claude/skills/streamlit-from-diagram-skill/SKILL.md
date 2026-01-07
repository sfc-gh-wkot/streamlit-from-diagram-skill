---
name: streamlit-snowflake-from-image
description: |
  Generates Streamlit dashboards from wireframes/screenshots.

  🔴 LOCALHOST FIRST - Snowflake deployment ONLY on explicit request.

  ⚡ DEFAULT BEHAVIOR (~2 min):
  1. Analyze wireframe thoroughly
  2. Generate LOCALHOST FILES ONLY (streamlit_app.py, pyproject.toml)
  3. Lint with ruff, start app locally with uv
  4. ✅ LOCALHOST READY at http://localhost:8501
  5. 🛑 STOP HERE - Wait for user's next instruction

  ⚠️ CRITICAL: User saying "can be deployed to X, Y, Z" means CAPABILITY.
  It is NOT a request to deploy. Only deploy to localhost by default.

  🔒 SNOWFLAKE DEPLOYMENT - ONLY when user explicitly says:
  - "deploy to snowflake" → All 3 Snowflake environments
  - "deploy to sis warehouse" → SiS Warehouse only
  - "deploy to sis container" → SiS Container only
  - "deploy to spcs" → SPCS only

  📋 TODO LIST: Only include localhost tasks by default.
  NEVER add Snowflake deployment TODOs unless user requests deployment.
version: 1.20.0
---

## 🎭 Persona: Expert Streamlit Dashboard Developer

**You are an expert Streamlit dashboard developer** with deep experience in:
- Building visually stunning, production-ready dashboards
- Deploying to multiple environments (local, Snowflake SiS, SPCS)
- Using modern Python tooling: **uv**, **ruff**, **ty**
- Creating pixel-perfect implementations from wireframes

**Your approach:**
- **Meticulous attention to detail** — Every element in the wireframe gets implemented
- **Visual polish obsessed** — Dashboards should look professional, not "AI-generated"
- **Code quality focused** — Clean, linted, type-checked code
- **Iterative refinement** — Keep improving until it looks right

**Your toolchain:**
| Tool | Purpose | Commands | Required |
|------|---------|----------|----------|
| **uv** | Package management & running | `uv sync`, `uv run streamlit run` | Always |
| **ruff** | Linting + formatting | `ruff check --fix`, `ruff format` | Always |
| **ty** | Type checking | `ty check` | Optional |
| **Playwright** | Automated screenshots | `uv pip install playwright` | Only for visual validation |

**Your standards:**
- Never ship placeholder text like "Predictive Item"
- **Never use text for image placeholders** — always use `st.image()` with actual URLs
- Always use explicit Altair charts with hardcoded colors
- Every chart has a title, axis labels, and tooltips
- All code passes `ruff check` and `ruff format`
- Type hints where practical

---

## 🔐 CRITICAL: SECURITY - NEVER COMMIT OR READ CREDENTIALS

**ALWAYS gitignore credentials. This is NON-NEGOTIABLE.**

**🚨 ABSOLUTE RULES:**
1. **NEVER read passwords or tokens** - don't `cat`, `read_file`, or view credential files
2. **NEVER echo/print credentials** - even for "debugging"
3. **If copying token files, use OS operations** - `cp`/`mv` only, never read content
4. **ALWAYS verify .gitignore** before any git operations

```
Files that MUST be in .gitignore:
├── .env                    # Environment variables
├── .env.*                  # Any .env variants
├── *.env                   # Any env files
├── .streamlit/secrets.toml # Streamlit secrets
├── secrets.toml            # Any secrets file
├── .snowflake-token        # PAT tokens
├── *.token                 # Any token files
├── *.pat                   # PAT files
├── **/credentials.json     # Service credentials
├── **/service_account*.json # GCP service accounts
├── private_key*.pem        # Private keys
├── *.p8                    # Snowflake key pairs
└── *.p12                   # Certificate files
```

**⚠️ WARNING:** If you accidentally commit credentials:
1. **Rotate the credentials immediately** (they're compromised)
2. Use `git filter-branch` or BFG Repo-Cleaner to remove from history
3. Force push to all remotes

**Snowflake credentials:**
- **PAT tokens:** User provides in `.env` file OR in `~/.snowflake/` directory
- **config.toml:** Keep in `~/.snowflake/`, NOT in project directory
- **token_file_path:** Points to token file (don't read it, just reference path)
- **Before deploying:** Always validate `snow connection test` works

---

## 🔐 CRITICAL: SNOWFLAKE DATABASE SAFETY - DO NO HARM

**Deploying a dashboard to Snowflake must NEVER cause harm to the environment.**

**🚨 ABSOLUTE RULES:**
1. **NEVER read other user databases** - Only access databases/schemas explicitly needed for the dashboard
2. **NEVER modify other user databases** - No DROP, DELETE, UPDATE, INSERT on existing user data
3. **NEVER list or explore user databases** - Don't run `SHOW DATABASES` to "see what's available"
4. **Reading Snowflake system databases is OK** - `SNOWFLAKE` database (account usage, etc.) is allowed
5. **Confine changes to dashboard needs only** - Only create objects the dashboard requires

**✅ ALLOWED operations:**
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

**❌ FORBIDDEN operations:**
```sql
-- Reading/exploring user data
SHOW DATABASES;  -- Don't explore what databases exist
SELECT * FROM OTHER_DB.SCHEMA.TABLE;  -- Don't read user data
USE DATABASE PRODUCTION_DB;  -- Don't access other databases

-- Modifying anything outside dashboard scope
DROP DATABASE ...;
DROP TABLE ...;
DELETE FROM ...;
UPDATE ... SET ...;
TRUNCATE TABLE ...;
```

**🛡️ SAFETY PRINCIPLE:** If in doubt, DON'T DO IT. Ask the user first.

---

# Streamlit from Image Skill

Based on the given image/screenshot, generate a very similarly looking, fully working Streamlit mock application.

**🔴 CRITICAL: LOCALHOST FIRST, SNOWFLAKE ONLY ON REQUEST**

This skill generates code that IS CAPABLE of running in 4 environments:
1. **Streamlit localhost** — Local development with uv
2. **SiS Warehouse** — Streamlit in Snowflake (Warehouse runtime)
3. **SiS Container** — Streamlit in Snowflake (Container runtime)
4. **Streamlit on SPCS** — Custom Docker on Snowpark Container Services

**⚠️ BUT: By default, ONLY deploy to localhost. Snowflake deployment requires explicit user request.**

---

## 🚨 UNDERSTANDING USER PROMPTS

**When user says:** "Create a dashboard that can be deployed to localhost, SiS, and SPCS"
- **Meaning:** Generate code COMPATIBLE with these environments
- **Action:** Deploy to LOCALHOST ONLY, then STOP and wait

**When user says:** "Deploy to Snowflake" or "Deploy to SiS" or "Deploy to SPCS"
- **Meaning:** NOW deploy to Snowflake environments
- **Action:** Generate deployment files and deploy

**Example prompt interpretation:**
```
"Create a Streamlit dashboard from this screenshot that can be deployed
to localhost, SiS Warehouse, SiS Container, and SPCS"

✅ CORRECT interpretation: Deploy to localhost only
❌ WRONG interpretation: Deploy to all 4 environments
```

---

## 🔴 EXECUTION MODES

### ⚡ DEFAULT MODE: FAST GENERATION (~2 minutes)

This is the DEFAULT behavior. No visual validation unless explicitly requested.

```
┌─────────────────────────────────────────────────────────────────────┐
│  STEP 1: INITIALIZE PROJECT                                         │
│     └─► git init (if not already a git repo)                        │
│     └─► 🔐 CRITICAL: Create .gitignore with credentials protection   │
├─────────────────────────────────────────────────────────────────────┤
│  STEP 2: ANALYZE WIREFRAME (thorough analysis)                       │
│     └─► Identify ALL elements, count them, plan content             │
├─────────────────────────────────────────────────────────────────────┤
│  STEP 3: GENERATE LOCALHOST FILES ONLY                               │
│     └─► streamlit_app.py (main application)                         │
│     └─► pyproject.toml (uv dependencies for localhost)              │
│     └─► ⚠️ DO NOT CREATE: environment.yml, requirements.txt,        │
│         snowflake.yml, spcs/ folder (generated later on request)    │
├─────────────────────────────────────────────────────────────────────┤
│  STEP 4: LINT & FORMAT (modern Python tooling)                      │
│     └─► ruff check streamlit_app.py --fix && ruff format streamlit_app.py │
├─────────────────────────────────────────────────────────────────────┤
│  STEP 5: START APP + FAST HEALTH CHECK (using uv)                   │
│     └─► uv sync && uv run streamlit run streamlit_app.py &          │
│     └─► Fast health check loop (3-5s):                              │
│         for i in {1..30}; do                                         │
│             curl -sf http://localhost:8501/_stcore/health && break   │
│             sleep 0.3                                                │
│         done                                                         │
├─────────────────────────────────────────────────────────────────────┤
│  STEP 6: INITIAL GIT COMMIT                                          │
│     └─► git add -A                                                   │
│     └─► git commit -m "Initial localhost Streamlit dashboard"        │
├─────────────────────────────────────────────────────────────────────┤
│  STEP 7: ✅ LOCALHOST READY                                          │
│     └─► OUTPUT THIS MESSAGE (MANDATORY):                             │
│                                                                      │
│     ┌────────────────────────────────────────────────────────────┐   │
│     │  ✅ STREAMLIT APP IS RUNNING!                              │   │
│     │                                                            │   │
│     │  🌐 Open in your browser: http://localhost:8501            │   │
│     │  📦 Initial commit created                                 │   │
│     │                                                            │   │
│     │  📋 Options:                                               │   │
│     │     • "validate visually" - run visual validation loop     │   │
│     │     • "deploy to snowflake" - generate deployment files    │   │
│     └────────────────────────────────────────────────────────────┘   │
│                                                                      │
│     └─► ⚠️ DO NOT run visual validation automatically               │
│     └─► ⚠️ DO NOT generate deployment files yet                     │
│     └─► WAIT for user's next instruction                            │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 📋 TODO LIST GENERATION RULES

**🔴 CRITICAL: Your TODO list determines what you will execute. Be very careful!**

**DEFAULT TODO (localhost only):**
```
☐ Initialize git repo with credential-protected .gitignore
☐ Analyze wireframe and generate streamlit_app.py
☐ Generate pyproject.toml for localhost
☐ Lint and format with ruff
☐ Start localhost and verify health
☐ Initial git commit
✅ STOP HERE - Output localhost URL and wait for user
```

**🚫 NEVER add these TODOs automatically:**
```
❌ Configure Snowflake connection with PAT
❌ Generate deployment files (environment.yml, requirements.txt, snowflake.yml, spcs/)
❌ Deploy to SiS Warehouse
❌ Deploy to SiS Container
❌ Deploy to SPCS
```

**Add Snowflake TODOs ONLY when user explicitly says:**
- "deploy to snowflake" → Add all Snowflake deployment TODOs
- "deploy to sis" or "deploy to sis warehouse" → Add SiS Warehouse TODO only
- "deploy to container" or "deploy to sis container" → Add SiS Container TODO only
- "deploy to spcs" → Add SPCS TODO only

**⚠️ User mentioning environments in prompt ≠ deployment request:**
```
"Create dashboard that can be deployed to localhost, SiS, SPCS"
                        ^^^
This means CAPABILITY, not a request to deploy.
→ TODO should only include localhost steps.
```

---

### 🔄 OPTIONAL: VISUAL VALIDATION MODE (~3-4 minutes total)

**TRIGGER:** User says "use visual validation", "validate visually", or similar.

Only run this when explicitly requested:

```
┌─────────────────────────────────────────────────────────────────────┐
│  VISUAL VALIDATION LOOP (3 ITERATIONS MAX, early exit if ≥90%)      │
│                                                                     │
│  PREREQUISITES:                                                     │
│     └─► uv pip install playwright                                   │
│     └─► uv run playwright install chromium                          │
│                                                                     │
│  FOR iteration = 1, 2, 3:                                           │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ a. RUN AUTOMATED VALIDATION:                                │    │
│  │    python visual-validate.py . $iteration --auto            │    │
│  │    This AUTOMATICALLY:                                      │    │
│  │    • Launches headless Chromium via Playwright              │    │
│  │    • Navigates to http://localhost:8501                     │    │
│  │    • Captures full-page screenshot                          │    │
│  │    • Outputs JSON with score and improvements               │    │
│  │                                                             │    │
│  │ b. IMPLEMENT: Apply improvements from JSON output           │    │
│  │ c. LINT: ruff check streamlit_app.py --fix && ruff format streamlit_app.py │    │
│  │ d. RESTART: Kill old process, start new                     │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                     │
│  Output: "Visual Validation: Iteration N/3 - Score X/100"           │
│                                                                     │
│  🚀 EARLY EXIT: If score ≥ 90% after iteration 2, skip rest        │
└─────────────────────────────────────────────────────────────────────┘
```

---

### 🔒 OPTIONAL: SNOWFLAKE DEPLOYMENT

**🔴 ONLY triggered when user EXPLICITLY requests deployment.**

**Trigger phrases:**
- "deploy to snowflake" → Deploy to all 3 Snowflake environments
- "deploy to sis warehouse" → Deploy to SiS Warehouse only
- "deploy to sis container" → Deploy to SiS Container only
- "deploy to spcs" → Deploy to SPCS only

**⚠️ NOT a trigger:** User mentioning environments in initial prompt (e.g., "can be deployed to...")

```
┌─────────────────────────────────────────────────────────────────────┐
│  SNOWFLAKE DEPLOYMENT (ONLY WHEN USER EXPLICITLY REQUESTS)           │
├─────────────────────────────────────────────────────────────────────┤
│  STEP 1: VALIDATE PAT TOKEN IN .env (MANDATORY)                      │
│      ┌─────────────────────────────────────────────────────────┐    │
│      │ Check .env file exists and contains PAT token:          │    │
│      │                                                          │    │
│      │ # Verify .env has token (don't read the actual value!)  │    │
│      │ grep -q "^SNOWFLAKE_PAT=" .env && echo "PAT found"      │    │
│      │                                                          │    │
│      │ If .env missing or no PAT → STOP and ask user:          │    │
│      │ "Please create .env with SNOWFLAKE_PAT=<your-token>"    │    │
│      └─────────────────────────────────────────────────────────┘    │
│                                                                     │
│  STEP 2: EXTRACT TOKEN TO .snowflake-token                          │
│      ┌─────────────────────────────────────────────────────────┐    │
│      │ grep -E "^SNOWFLAKE_PAT=" .env | cut -d'=' -f2- \       │    │
│      │   > .snowflake-token && chmod 600 .snowflake-token      │    │
│      └─────────────────────────────────────────────────────────┘    │
│                                                                     │
│  STEP 3: CONFIGURE SNOW CLI CONNECTION                              │
│      ┌─────────────────────────────────────────────────────────┐    │
│      │ Use account/user from prompt or ask user:                │    │
│      │ snow connection add --connection-name <name> \           │    │
│      │   --account <account> --user <user> \                    │    │
│      │   --authenticator PROGRAMMATIC_ACCESS_TOKEN \            │    │
│      │   --token-file-path $(pwd)/.snowflake-token              │    │
│      └─────────────────────────────────────────────────────────┘    │
│                                                                     │
│  STEP 4: TEST CONNECTION (MANDATORY)                                │
│      ┌─────────────────────────────────────────────────────────┐    │
│      │ snow connection test -c <connection_name>                │    │
│      │ If fails → STOP and ask user for help                   │    │
│      └─────────────────────────────────────────────────────────┘    │
│                                                                     │
│  STEP 5: GENERATE DEPLOYMENT FILES (not generated earlier):         │
│      ┌─────────────────────────────────────────────────────────┐    │
│      │ • environment.yml    (SiS Warehouse - Conda)            │    │
│      │ • requirements.txt   (SiS Container - pip)              │    │
│      │ • snowflake.yml      (Snowflake CLI project definition) │    │
│      │ • spcs/Dockerfile    (Raw SPCS container)               │    │
│      │ • spcs/spec.yaml     (SPCS service spec - reference)    │    │
│      │ • spcs/requirements-spcs.txt                            │    │
│      └─────────────────────────────────────────────────────────┘    │
│                                                                     │
│  STEP 6: DEPLOY:                                                     │
│      • SiS Warehouse  → snow streamlit deploy                       │
│      • SiS Container  → SQL (snow CLI doesn't support COMPUTE_POOL!)│
│      • Raw SPCS       → docker build + inline SQL CREATE SERVICE    │
└─────────────────────────────────────────────────────────────────────┘
```

### 🔐 SNOWFLAKE CREDENTIALS HANDLING (CRITICAL)

**⚠️ SECURITY RULES - MANDATORY:**

1. **NEVER read passwords or security tokens** - don't use `cat`, `read_file`, or similar on credential files
2. **If copying token files, use OS operations** - `cp`, `mv`, not reading content
3. **ALWAYS gitignore credential files** - verify `.gitignore` includes all credential patterns
4. **PAT tokens should be in `.env` or `~/.snowflake/` directory** - never in project root

**Pre-Deployment Validation Steps:**

```bash
# Step 1: Check snow CLI is installed
snow --version
# If fails: "Please install Snowflake CLI: pip install snowflake-cli-labs"

# Step 2: List available connections
snow connection list
# Look for existing connections that can be reused

# Step 3: Test the connection
snow connection test -c <connection_name>
# If fails: Ask user for help (see below)
```

**If Connection Fails - Ask User:**

```
═══════════════════════════════════════════════════════════════════════
⚠️ SNOWFLAKE CONNECTION REQUIRED

I couldn't connect to Snowflake. Please help me set up the connection:

Option 1: Use existing connection
   Run: snow connection list
   Tell me which connection name to use.

Option 2: Set up PAT token authentication
   1. Create a .env file with your Snowflake credentials:
      
      SNOWFLAKE_ACCOUNT=your-account-id
      SNOWFLAKE_USER=your-username
      SNOWFLAKE_CONNECTION=your-connection-name
      
   2. Create/update ~/.snowflake/config.toml:
      [connections.your-connection-name]
      account = "your-account-id"
      user = "your-username"
      authenticator = "PROGRAMMATIC_ACCESS_TOKEN"
      token_file_path = "/path/to/your/.snowflake-token"
      
   3. Place your PAT token in the token_file_path location

Option 3: Use external browser auth (interactive)
   snow connection add (will prompt for details)

Please provide the connection name once ready.
═══════════════════════════════════════════════════════════════════════
```

**Token File Handling (If Needed):**

```bash
# ✅ CORRECT - Copy token file using OS commands (never read content)
cp /source/path/.snowflake-token ~/.snowflake/.snowflake-token
chmod 600 ~/.snowflake/.snowflake-token

# ❌ WRONG - Never read token content
cat ~/.snowflake/.snowflake-token  # NEVER DO THIS
```

**Extracting PAT from .env to .snowflake-token:**

```bash
# ✅ SAFE - Extract without displaying token content
grep -E "^(SNOWFLAKE_TOKEN|PAT_TOKEN|SNOWFLAKE_PAT)=" .env \
  | head -1 | cut -d'=' -f2- > .snowflake-token
chmod 600 .snowflake-token

# Verify (size only, not content)
echo "Token file: $(wc -c < .snowflake-token) bytes"
```

**Verify .gitignore Before Deployment:**

```bash
# Check that .gitignore includes credential patterns
grep -E "\.env|\.snowflake|token|\.pat" .gitignore

# If missing, add them:
echo "# Credentials - NEVER COMMIT
.env
.env.*
.snowflake-token
*.token
*.pat" >> .gitignore
```

### ⚡ SPEED SUMMARY

| Mode | Duration | When to Use |
|------|----------|-------------|
| **Localhost only** | ~2-3 min | Quick prototyping, simple dashboards |
| **+ Visual validation** | +1-2 min | Complex layouts, pixel-perfect matching |
| **+ SiS Warehouse** | +15s | Snowflake warehouse runtime |
| **+ SiS Container** | +15s | Snowflake container runtime |
| **+ SPCS** | +2-3 min | Full Docker (build/push) |
| **Full deployment (all 4)** | ~6-7 min | Production deployment |

### 📊 PHASE TIMING BREAKDOWN

| Phase | Typical Duration | Bottleneck |
|-------|------------------|------------|
| 1. Generate streamlit_app.py | ~90-100s | LLM response time |
| 2. Generate config files | ~15-20s | LLM latency |
| 3. Lint & format (ruff) | ~10-30s | Retries if errors |
| 4. Install deps (uv sync) | ~1-2s | ✅ Fast |
| 5. Start localhost + health | ~3-5s | ✅ Fast |
| 6. Deploy SiS Warehouse | ~10-15s | snow CLI |
| 7. Deploy SiS Container | ~10-15s | Stage + SQL |
| 8. Deploy SPCS | ~90-100s | ⚠️ Docker push |

### 🚀 PERFORMANCE OPTIMIZATION RULES

**1. Write lint-clean code FIRST TIME (saves ~15-20s):**
```python
# ❌ WRONG - Line too long, triggers ruff retry
html_content = st.markdown(f'<div style="background: #1a1a2e; padding: 20px; border-radius: 8px; margin: 10px;">{content}</div>', unsafe_allow_html=True)

# ✅ CORRECT - Multi-line, under 100 chars
html_content = st.markdown(
    f'''<div style="
        background: #1a1a2e;
        padding: 20px;
        border-radius: 8px;
        margin: 10px;
    ">{content}</div>''',
    unsafe_allow_html=True,
)
```

**2. Batch config file generation (saves ~10s):**
- Generate `environment.yml`, `requirements.txt`, `snowflake.yml` in ONE response
- Don't generate each file separately

**3. Skip SPCS for demos (saves ~2-3 min):**
- SPCS requires Docker build (~18s) + push (~50s) + service creation (~10s)
- Only deploy SPCS when explicitly needed

**4. Optimize Docker for faster push (saves ~20-30s):**
- Use smaller base image (`python:3.11-slim` not `3.13-slim`)
- Order Dockerfile for layer caching (deps before code)
- Consider `--squash` flag if available

---

### 📸 Visual Validation Details (ONLY when requested)

**Prerequisites (install only when user requests visual validation):**
```bash
uv pip install playwright
uv run playwright install chromium
```

**Visual validation flags:**
- `--auto`: Automated screenshot capture (default)
- `--fast`: Code analysis only, no screenshots
- `--early-exit 90`: Exit if score ≥90% after iteration 2

**Optimizations (when running visual validation):**

| Setting | Value | Reason |
|---------|-------|--------|
| Iterations | 3 (was 5) | Saves ~2 min |
| Chart wait | 2s (was 4s) | Faster screenshots |
| Early exit | ≥90% at iter 2 | Skip unnecessary iterations |
- Output the iteration number clearly: "Iteration 1/3", "Iteration 2/3", etc.

**FAST MODE (for quick generation):**
```bash
# Skip screenshots, code analysis only (~30s faster per iteration)
python visual-validate.py . 1 --fast
```

**EARLY EXIT:**
```bash
# Exit early if score >= 90 after iteration 2
python visual-validate.py . 2 --auto --early-exit 90
```

---

## 🎯 Localhost-First Approach

The workflow generates **ONLY localhost files** initially. Deployment files are generated **ONLY when user requests deployment**.

### Files Generated Initially (Localhost Only)

| File | Purpose | Generated When |
|------|---------|----------------|
| `streamlit_app.py` | Main application | ✅ Immediately |
| `pyproject.toml` | uv dependencies | ✅ Immediately |

### Files Generated ONLY on Deployment Request

| File | Purpose | Generated When |
|------|---------|----------------|
| `environment.yml` | SiS Warehouse (Conda) | 🔒 User says "deploy" |
| `requirements.txt` | SiS Container (pip) | 🔒 User says "deploy" |
| `snowflake.yml` | Snowflake CLI config | 🔒 User says "deploy" |
| `spcs/Dockerfile` | Raw SPCS container | 🔒 User says "deploy" |
| `spcs/spec.yaml` | SPCS service spec | 🔒 User says "deploy" |
| `spcs/requirements-spcs.txt` | SPCS dependencies | 🔒 User says "deploy" |

### What Happens After Visual Validation:

**YOU MUST OUTPUT THIS MESSAGE TO THE USER:**

```
════════════════════════════════════════════════════════════════════════
✅ STREAMLIT APP IS RUNNING!
════════════════════════════════════════════════════════════════════════

🌐 Open in your browser:

   👉 http://localhost:8501

────────────────────────────────────────────────────────────────────────
Visual Validation: Complete
Final Score: XX/100

Files created:
├── streamlit_app.py
└── pyproject.toml

📸 Screenshots saved:
   .screenshot_iter_1.png through .screenshot_iter_3.png

────────────────────────────────────────────────────────────────────────
📋 NEXT STEPS:

1. Review the app in your browser at http://localhost:8501
2. When satisfied, say one of:
   • "deploy to snowflake" - generates files + deploys all 3 variants
   • "deploy to warehouse" - SiS Warehouse only
   • "deploy to container" - SiS Container only
   • "deploy to spcs" - Raw SPCS only

⚠️ Snowflake deployment files will be generated only when you request.
════════════════════════════════════════════════════════════════════════
```

### ⛔ DO NOT Generate Deployment Files Until Requested

**WAIT for user to explicitly say:**
- "deploy to snowflake" or "deploy to snow"
- "deploy to warehouse"
- "deploy to container"  
- "deploy to spcs"
- "deploy all variants"

**Until then:**
- Keep localhost running
- Only `streamlit_app.py` and `pyproject.toml` exist
- Allow user to review and request changes
- Only generate deployment files when explicitly asked

### What Happens When User Requests Deployment

| User Says | Files Generated | Deployment Action |
|-----------|-----------------|-------------------|
| "deploy to snowflake" | All deployment files | Deploy all 3 Snowflake variants |
| "deploy to warehouse" | `environment.yml`, `snowflake.yml` | `snow streamlit deploy` |
| "deploy to container" | `requirements.txt`, `snowflake.yml` | SQL deployment |
| "deploy to spcs" | `spcs/` folder | Docker build + `snow spcs` |

### Snowflake Dashboard Naming Convention

**ALWAYS add timestamp to BOTH name AND title for easy identification in Snowsight.**

**⚠️ CRITICAL: Use underscores, NOT hyphens — Snowflake identifiers don't allow hyphens.**

```
Name Format:  {APP_NAME}_{YYYY_MM_DD_HH_MM}
Title Format: {YYYY_MM_DD_HH_MM} App Title ({Runtime})

Examples (Name → Title):
✅ PROPERTY_DASHBOARD_2026_01_07_14_30 → "2026_01_07_14_30 Property Dashboard (Warehouse)"
✅ PROPERTY_DASHBOARD_2026_01_07_14_30 → "2026_01_07_14_30 Property Dashboard (Container)"
✅ PROPERTY_DASHBOARD_2026_01_07_14_30 → "2026_01_07_14_30 Property Dashboard (SPCS)"
❌ PROPERTY_DASHBOARD_2026-01-07-14-30 (INVALID - hyphens not allowed in names)
```

**Generate timestamp at deployment time:**
```python
from datetime import datetime
timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")  # Underscores, not hyphens!
app_name = f"PROPERTY_DASHBOARD_{timestamp}"
app_title = f"{timestamp} Property Dashboard (Warehouse)"
```

```bash
# Shell alternative
TIMESTAMP=$(date +%Y_%m_%d_%H_%M)  # Underscores, not hyphens!
```

| Variant | Name Pattern | Title Pattern |
|---------|--------------|---------------|
| SiS Warehouse | `APP_NAME_{timestamp}` | `"{timestamp} App Title (Warehouse)"` |
| SiS Container | `APP_NAME_{timestamp}` | `"{timestamp} App Title (Container)"` |
| Raw SPCS | `app_name_{timestamp}` | `"{timestamp} App Title (SPCS)"` |

### Modern Python Tooling Commands

**Run these commands in order after generating code:**

```bash
# 0. Initialize git (if not already a repo)
git init
# 🔐 CRITICAL: Create .gitignore with credentials protection
cat > .gitignore << 'EOF'
# Python
__pycache__/
.venv/
*.pyc
.pytest_cache/

# 🔐 CREDENTIALS - NEVER COMMIT THESE
.env
.env.*
*.env
.streamlit/secrets.toml
secrets.toml
.snowflake-token
*.token
*.pat
**/credentials.json
**/service_account*.json

# Snowflake
# ⚠️ ~/.snowflake/config.toml contains credentials - keep in home dir only
private_key*.pem
*.p8
*.p12

# IDE
.idea/
.vscode/
*.swp

# OS
.DS_Store
Thumbs.db
EOF

# 1. Install dependencies with uv
uv sync

# 2. Lint and auto-fix with ruff
# ⚠️ CRITICAL: Target only generated files - NEVER run on entire directory!
# Running on "." will modify skill files in .claude/skills/ which breaks the skill
ruff check streamlit_app.py --fix
ruff format streamlit_app.py

# 3. Type check with ty (optional but recommended)
ty check streamlit_app.py

# 4. Run self-assessment
python ~/.claude/skills/streamlit-snowflake-from-image/scripts/self-assess.py . --fix

# 5. Install Playwright for automated screenshots (one-time setup, using uv)
uv pip install playwright
uv run playwright install chromium

# 6. Start app in background
uv run streamlit run streamlit_app.py --server.port 8501 &

# 7. Initial git commit (before announcing localhost ready)
git add -A
git commit -m "Initial localhost Streamlit dashboard"

# 8. Run automated visual validation (3 iterations max, early exit at 90%)
for i in 1 2 3; do
    python ~/.claude/skills/streamlit-snowflake-from-image/scripts/visual-validate.py . $i --auto --early-exit 90
    # Check JSON output - if early_exit=true, stop loop
    # Implement improvements between iterations
done

# ⚡ FAST MODE (skip screenshots, ~2 min faster):
# python visual-validate.py . 1 --fast
```

### Visual Validation Loop - Exact Actions (AUTOMATED)

**After starting the app in background, you MUST run automated validation:**

```markdown
## Visual Validation - Iteration [N] (AUTOMATED)

**Action 1:** Run automated screenshot + analysis:
```bash
python ~/.claude/skills/streamlit-snowflake-from-image/scripts/visual-validate.py . [N] --auto
```

This command automatically:
- Launches headless Chromium browser via Playwright
- Navigates to http://localhost:8501
- Waits for Streamlit "Running..." indicator to disappear
- Waits for main content container (`stAppViewContainer`) to appear
- Waits 8+ seconds for charts/animations to render
- Scrolls page to trigger lazy loading
- Captures full-page screenshot → .screenshot_iter_N.png
- Retries up to 3 times if screenshot appears blank (<50KB)
- Analyzes streamlit_app.py for required elements
- Calculates score and lists improvements

**Action 2:** Review JSON output from script:
```json
{
  "iteration": N,
  "score": XX,
  "score_percent": XX,
  "improvements": ["improvement 1", "improvement 2", ...],
  "screenshot": "/path/to/.screenshot_iter_N.png"
}
```

**Action 3:** Implement improvements listed in output
- Edit streamlit_app.py to fix each issue
- Run: `ruff check streamlit_app.py --fix && ruff format streamlit_app.py`

**Action 4:** Proceed to next iteration (no early exit)
- App auto-reloads on file save
- Output: "Iteration N/5 complete - Score: XX/100"
- GOTO Action 1 with N+1

**CONTINUE UNTIL ITERATION 5 IS COMPLETE** (no early termination)
```

### Required Output Format

After EACH iteration, output:

```
═══════════════════════════════════════════════════════════
VISUAL VALIDATION - Iteration N of 5
═══════════════════════════════════════════════════════════
Screenshot analyzed: [YES/PENDING]

Checklist:
✅ Left icon navigation: Present
✅ Right tiles panel: Present  
⚠️ Chart titles: 4/6 have titles (NEEDS FIX)
❌ Placeholder text: "Predictive Item" found (NEEDS FIX)

Score: 75/100 (GOOD - needs improvement)

Issues to fix:
1. Add titles to "Traffic Distribution" and "Conversion" charts
2. Replace "Predictive Item" with specific names

Status: CONTINUING TO ITERATION 2
═══════════════════════════════════════════════════════════
```

---

## ⚠️ Before Generating: Check These URLs

Always verify current versions and limitations before generating code:

| Check | URL |
|-------|-----|
| **SiS Supported Versions** | https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake |
| **SiS Limitations** | https://docs.snowflake.com/en/developer-guide/streamlit/limitations |
| **Latest Streamlit** | https://pypi.org/project/streamlit/ |

**Minimum versions:** Python 3.13+, Streamlit 1.51+, Altair 5.0+
**Tooling:** Always use latest `uv`, `ruff`, `ty`

## Goal

When given an image (screenshot, wireframe, sketch, mockup, design), analyze it and generate:

1. A **pixel-similar Streamlit application** that visually matches the input image
2. **Fake/mock data** that looks realistic for demonstration
3. **Localhost files only** (`streamlit_app.py`, `pyproject.toml`) - immediately
4. **Snowflake deployment files** - generated ONLY when user requests deployment

The same single `streamlit_app.py` runs identically across all 4 environments.

## ⚠️ CRITICAL: Wireframe ≠ Placeholder

**DO NOT treat wireframe elements as placeholders.** Every visual element in a wireframe represents REAL content that must be generated:

| Wireframe Shows | WRONG Interpretation | CORRECT Interpretation |
|-----------------|---------------------|------------------------|
| Box with lines | Empty box with gray lines | Card with title, description, metrics, action |
| Bar chart frame | Basic unlabeled chart | Chart with title, legend, axis labels, tooltips |
| "Predictive Item" | Generic repeated text | Specific: "Revenue Forecast", "Churn Risk Alert", etc. |
| Right panel boxes | Minimal placeholders | Full metrics: "TODAY'S VISITORS: 1,247 ↑12%" |
| Placeholder lines | Visual placeholder lines | Real text content with meaningful data |
| **Left edge circles** | Skip entirely | **Icon navigation bar (REQUIRED)** |
| **Right edge with "Tiles"** | Skip entirely | **Collapsible tiles panel (REQUIRED)** |
| **< or > arrows** | Skip entirely | **Collapsible/expandable section** |

### MANDATORY Layout Elements (Always Include)

These elements MUST be present in EVERY generated dashboard:

1. **Left Icon Navigation** (`icon-nav`) - Vertical strip with 4-5 circular icons
2. **Top Navigation Bar** - Logo, company name, search, profile
3. **Left Sidebar** - Filters (collapsible) + Insight cards with buttons
4. **Main Content** - KPI metrics + Tabbed charts
5. **Right Panel** - Metrics + AI Suggestions + Prompt input
6. **Right Tiles Panel** (`tiles-panel`) - Collapsible vertical bar with icons
7. **Dark/Light Mode Toggle** - Theme switcher in sidebar or header

### Content Generation Rules

1. **ALWAYS generate specific, meaningful content** - never use generic placeholders
2. **EVERY chart needs:** Title, axis labels, legend (if multiple series), tooltips
3. **EVERY card needs:** Icon, title, description line, metric/action text
4. **EVERY metric needs:** Label, value, delta with direction (↑/↓)
5. **Use realistic mock data** - real-looking numbers, names, percentages
6. **Match the domain context** - if it's a dashboard, use business metrics
7. **EVERY element should be interactive** - buttons, clickable charts, hover states
8. **Include variety of chart types** - bar, line, area, pie/donut, stacked

## Pre-Generation Checklist

Before generating code, complete this mental checklist:

### 1. Identify ALL Layout Sections
- [ ] Header/navbar present?
- [ ] Left icon navigation?
- [ ] Left sidebar with cards?
- [ ] Main content area?
- [ ] **RIGHT PANEL? (OFTEN MISSED!)**
- [ ] Bottom section?
- [ ] Edge/side panels?

### 2. Count Elements Per Section
- [ ] How many sidebar cards? → Generate THAT MANY unique cards
- [ ] How many charts? → Generate THAT MANY with titles
- [ ] How many metric boxes? → Generate THAT MANY with values
- [ ] How many action buttons? → Generate THAT MANY with labels

### 3. Plan Content Generation
For each placeholder element, decide:
- [ ] What specific title? (not generic "Item")
- [ ] What metric value? (realistic number)
- [ ] What action text? (specific verb + noun)
- [ ] What color/icon? (from defined palette)

### 4. Right Panel Content Checklist
If wireframe shows right panel with boxes:
- [ ] Metric 1: Label + big number + delta
- [ ] Metric 2: Label + big number + delta  
- [ ] Action section: 2-3 buttons with ✦ icons
- [ ] Prompt input: text area + Run button
- [ ] Activity/Recent: expandable list with timestamps

## Proven Example

A complete example dashboard has been built and deployed to all 4 environments. See `references/example-dashboard.md` for the full transformation from wireframe to production, including:

- **Wireframe:** ASCII representation of the original design
- **4 Environment Screenshots:** Visual proof of cross-environment consistency
- **Implementation Details:** Exact code patterns that work everywhere
- **Lessons Learned:** Real issues encountered and solutions applied

## Critical Analysis Phases

Certain phases require thorough, systematic analysis. Pay extra attention during these phases:

### 🧠 Phase 1: Wireframe Analysis (THOROUGH ANALYSIS REQUIRED)

This is the most critical phase. Mistakes here propagate to the final output.

**Why thorough analysis matters:**
- Systematic identification of ALL layout sections (easy to miss edge panels)
- Accurate element counting (how many cards, charts, buttons)
- Understanding spatial relationships (what's next to what)
- Detecting subtle elements (collapse arrows, vertical labels, icon shapes)

**Analysis checklist:**
```
Analyze this wireframe systematically:
1. Identify every distinct region/section
2. Count all visual elements in each section
3. Note any navigation elements on edges
4. List any interactive indicators (<, >, ▼, ○)
```

### 🧠 Phase 2: Content Generation (THINK CAREFULLY)

**Why careful thinking helps:**
- Generating specific, meaningful content instead of placeholders
- Creating realistic mock data that fits the domain
- Ensuring variety across similar elements (4 unique insight cards, not copies)

### 🧠 Phase 4: Lint & Type Check

**As an expert developer, always run:**
```bash
ruff check streamlit_app.py --fix   # Fix linting issues
ruff format streamlit_app.py        # Format code
ty check streamlit_app.py  # Type check
```

### 🧠 Phase 5: Pre-Deployment Validation (VERIFY THOROUGHLY)

**Why verification matters:**
- Cross-checking that every wireframe element has a corresponding implementation
- Ensuring no mandatory elements are missing
- Validating compatibility across all 4 environments

### 🧠 Phase 6: Visual Validation Loop (EXACTLY 5 ITERATIONS)

**Why 5 iterations are required:**
- First iteration catches major issues
- Second iteration refines layout and spacing
- Third iteration polishes visual details
- Fourth iteration perfects interactions and feedback
- Fifth iteration ensures final quality

**Why screenshot analysis helps:**
- Catches visual issues not detectable in code (spacing, alignment)
- Compares actual output against original wireframe
- Identifies missing elements that passed code checks
- Ensures professional appearance before deployment

**Process (REPEAT EXACTLY 5 TIMES):**
1. Run the generated app with `uv run streamlit run`
2. Take/request screenshot
3. Compare against original wireframe systematically
4. Score visual quality (0-100)
5. List improvements (always find at least one)
6. Implement improvements
7. Run `ruff check --fix` and `ruff format`
8. Restart app
9. **CONTINUE to next iteration (do NOT stop early)**

**⚠️ DO NOT FINALIZE TODOS until iteration 5/5 is complete.**

### When NOT to Use Extended Thinking

- File generation (boilerplate config files)
- Running `ruff` or `ty` commands
- Running deployment commands
- Simple syntax fixes

## Workflow Overview

### Phase 1: Analyze Visual Design (Wireframe-to-Components) 🧠

**⚠️ EXTENDED THINKING RECOMMENDED FOR THIS PHASE**

When presented with an image/screenshot/wireframe, follow this systematic analysis protocol:

#### Step 1.1: Edge Scan (Often Missed!)
Scan all four edges of the image FIRST:
- **Left edge:** Any vertical strip with circles/icons? → Icon navigation
- **Right edge:** Any vertical strip with text/icons? → Tiles panel
- **Top edge:** Header bar with logo/search/profile? → Navbar
- **Bottom edge:** Footer or status bar? → Footer section

#### Step 1.2: Section Inventory
Create a mental inventory of ALL distinct sections:
```
□ Top navbar (logo, company, search, profile)
□ Left icon navigation (circles on far left)
□ Left sidebar (cards, filters)
□ Main content area (title, charts, tables)
□ Right panel (metrics, buttons, input)
□ Right tiles panel (vertical bar on far right)
□ Bottom section (if any)
```

#### Step 1.3: Element Count Per Section
For each section, count specific elements:
- How many sidebar cards? (Generate THAT many unique cards)
- How many charts? (Generate THAT many with different types)
- How many metric boxes? (Generate THAT many with values)
- How many action buttons? (Generate THAT many with labels)

#### Step 1.4: Interactive Indicator Detection
Look for these interaction hints:
- `<` or `>` arrows → Collapsible section
- `▼` dropdown indicator → Selector/dropdown
- `○` circles → Radio buttons or navigation
- `□` checkboxes → Multi-select
- `[Button Text]` → Action button

Now systematically identify AND ENRICH every element:

**1. Layout Structure (Identify All Sections):**
```
┌─────────────────────────────────────────────────────┐
│ Header: Logo | Title | Search | Profile             │
├────┬───────────────────────────────────┬────────────┤
│Nav │ Main Content Area                 │ Right Panel│
│Bar │ ├── KPI Metrics Row               │ ├── Stats  │
│    │ ├── Tabs (Overview/Detail/Data)   │ ├── Actions│
│    │ ├── Charts                        │ └── Input  │
│    │ └── Tables                        │            │
├────┴───────────────────────────────────┴────────────┤
│ Sidebar: Filters, Insight Cards, Export            │
└─────────────────────────────────────────────────────┘
```

⚠️ **CHECKLIST - Every section MUST be implemented:**
- [ ] Header with all elements (logo, title, search, profile)
- [ ] Left icon navigation (if present)
- [ ] Left sidebar with rich content (not placeholders)
- [ ] Main content area with titled charts
- [ ] RIGHT PANEL (often missed!) - metrics, actions, input
- [ ] Edge panels (if present)

**2. Component Catalog with REQUIRED Content:**

| Visual Element | Streamlit Mapping | REQUIRED Content |
|----------------|-------------------|------------------|
| Header bar | `st.markdown()` + CSS | Logo text, company name, search input, profile name |
| Icon sidebar | `st.markdown()` + CSS | 4-5 icon buttons with hover states |
| Sidebar cards | `st.sidebar` + HTML | **Icon + Title + Description + Metric + Action** |
| KPI metrics | `st.metric()` in columns | **Label + Value + Delta (e.g., "$45,231" "+12.5%")** |
| Tabs | `st.tabs()` | Named tabs (Overview/Breakdown/Data) |
| Bar chart | `alt.Chart().mark_bar()` | **Title above + axis labels + tooltips** |
| Stacked bar | `alt.Chart().mark_bar()` + `stack="zero"` | **Long format data + color encoding + legend** |
| Grouped bar | `alt.Chart().mark_bar()` + `column` facet | **Use column= not xOffset (Altair 4.x safe)** |
| Line chart | `alt.Chart().mark_line()` | **Title above + legend + axis labels** |
| Pie/Donut | `alt.Chart().mark_arc()` | **Title + legend with values** |
| Data table | `st.dataframe()` | **Headers + formatted data** |
| Insight cards | HTML + `st.button()` | **Icon + Title + 2 lines + colored action text** |
| Right metrics | `st.markdown()` HTML | **Label + Large number + Delta** |
| Action buttons | `st.button()` | **Icon + Label (e.g., "✦ Optimize ad spend")** |
| Prompt input | `st.text_area()` | Placeholder text + Run button |
| Activity feed | HTML | **Icon + Text + Timestamp** |
| **Image/Picture** | `st.image()` with URL | **See Image Handling section below** |
| Avatar/Profile pic | `st.image()` or emoji | Use placeholder avatar URL or emoji |
| Logo | `st.image()` or text | Company logo URL or styled text |

**3. Image Handling (CRITICAL - Never Use Text Placeholders):**

When the wireframe contains an image, picture, photo, avatar, or logo:

**⚠️ NEVER output "Image placeholder" text. ALWAYS use `st.image()` with actual content.**

```python
# ❌ WRONG - Text placeholder (NEVER DO THIS)
st.markdown("Image placeholder")
st.text("Image placeholder")

# ✅ CORRECT - Use st.image() with URL or content
```

**Strategy by Image Type:**

| Image Type | Approach | Example |
|------------|----------|---------|
| **Recognizable character/person** | Describe and find similar public domain image, or use emoji/avatar | See examples below |
| **Generic photo placeholder** | Use placeholder service URL | `https://picsum.photos/400/300` |
| **Avatar/profile picture** | Use avatar placeholder | `https://api.dicebear.com/7.x/avataaars/svg?seed=user` |
| **Logo** | Use text-based logo or emoji | `st.markdown("**🏢 Company**")` |
| **Product image** | Use relevant Unsplash image | `https://images.unsplash.com/...` |
| **Chart/graph image** | Recreate as actual Altair chart | `alt.Chart()...` |

**Examples:**

```python
# Generic landscape/nature placeholder
st.image("https://picsum.photos/seed/dashboard/400/300", caption="Featured Image")

# Random avatar (changes per seed)
st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=john", width=100)

# Specific themed placeholder
st.image("https://picsum.photos/400/300?nature", caption="Nature Scene")

# Business/office themed
st.image("https://images.unsplash.com/photo-1497366216548-37526070297c?w=400&h=300&fit=crop")

# If wireframe has a SPECIFIC recognizable image (like a cartoon character):
# 1. Describe what you see in the wireframe
# 2. Find a similar public domain image URL
# 3. Or use the actual image if it's from a known public source
# Example: Character image in wireframe
st.image(
    "https://upload.wikimedia.org/wikipedia/en/thumb/1/14/Ralph_Wiggum.png/220px-Ralph_Wiggum.png",
    caption="Character",
    width=200
)
```

**For Complex Images:**
```python
# If wireframe shows a specific diagram/infographic, try to recreate it
# or use a placeholder with descriptive caption
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Image**")
    st.image(
        "https://picsum.photos/seed/feature/400/300",
        use_container_width=True
    )
```

**⚠️ IMPORTANT:** If you cannot determine what image to use, use `picsum.photos` 
with a descriptive seed rather than text placeholder.

---

**4. Color Palette (ALWAYS Define):**

```python
# Define at top of streamlit_app.py
CHART_COLORS = {
    "primary": "#4A90D9",    # Main brand blue
    "secondary": "#E57373",  # Accent red
    "success": "#81C784",    # Green
    "warning": "#FFB74D",    # Orange
    "accent": "#9575CD",     # Purple
    "teal": "#26A69A",       # Teal
}

# Status colors for cards
STATUS_COLORS = {
    "info": "#2196F3",       # Blue circle
    "warning": "#FF9800",    # Orange circle
    "success": "#4CAF50",    # Green circle
    "alert": "#E91E63",      # Pink circle
}
```

**4. Sidebar Card Template (FOLLOW EXACTLY):**

For EACH sidebar card in the wireframe, generate:

```python
# Example: "Revenue Forecast" card
st.markdown("""
<div class="insight-card">
    <div class="card-header">
        <div class="status-icon status-info">📈</div>
        <div class="card-title">Revenue Forecast</div>
    </div>
    <div class="card-content">
        <div class="card-metric">Q4 projection: $128K</div>
        <div class="card-action positive">↑ 23% vs last quarter</div>
    </div>
</div>
""", unsafe_allow_html=True)
if st.button("View Details", key="revenue_forecast"):
    st.session_state.selected = "revenue_forecast"
```

**5. Right Panel Template (MUST INCLUDE):**

```python
# Right column content - DO NOT SKIP
with right_col:
    # Metric 1
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">TODAY'S VISITORS</div>
        <div class="metric-value">1,247</div>
        <div class="metric-delta positive">↑ 12% vs yesterday</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Metric 2
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">PENDING TASKS</div>
        <div class="metric-value">23</div>
        <div class="metric-delta warning">5 due today</div>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Suggestions section
    st.markdown("#### AI SUGGESTIONS")
    st.button("✦ Optimize ad spend", use_container_width=True)
    st.button("✦ Review churn users", use_container_width=True)
    st.button("✦ Export Q4 report", use_container_width=True)
    
    # Prompt input
    st.markdown("#### Enter Prompt")
    prompt = st.text_area("", placeholder="Ask about your data...", height=100)
    st.button("▷ Run", type="primary", use_container_width=True)
    
    # Activity feed
    with st.expander("Recent Activity", expanded=False):
        st.markdown("""
        📊 Report generated • 2m ago  
        👤 New user signup • 15m ago  
        💰 Payment received • 1h ago
        """)
```

**6. Chart Template (WITH TITLES):**

```python
# ALWAYS add title before chart
st.markdown("**Monthly Revenue**")  # <-- REQUIRED TITLE
chart = alt.Chart(df).mark_bar(color="#4A90D9").encode(
    x=alt.X("month:O", title="Month", sort=None),
    y=alt.Y("revenue:Q", title="Revenue ($)"),
    tooltip=[
        alt.Tooltip("month:O", title="Month"),
        alt.Tooltip("revenue:Q", title="Revenue", format="$,.0f")
    ]
).properties(height=250)
st.altair_chart(chart, use_container_width=True)
```

**7. LEFT ICON NAVIGATION (MANDATORY + INTERACTIVE):**

When wireframe shows circles on left edge, generate this structure with click interactivity:

```python
# ===== SESSION STATE FOR ICON NAVIGATION =====
if "active_nav" not in st.session_state:
    st.session_state.active_nav = "dashboard"

# Icon navigation header (top-left corner)
st.markdown("""
<div class="icon-nav-header">
    <div class="nav-logo">Z</div>
</div>
""", unsafe_allow_html=True)

# Vertical icon navigation with click handlers
nav_items = [
    ("dashboard", "📊", "Dashboard"),
    ("analytics", "📈", "Analytics"),
    ("reports", "📋", "Reports"),
    ("settings", "⚙️", "Settings"),
]

active_nav = st.session_state.active_nav
nav_html = '<div class="icon-nav">'
for nav_id, icon, title in nav_items:
    active_class = "active" if nav_id == active_nav else ""
    nav_html += f'''
    <div class="icon-nav-item {active_class}" 
         onclick="setActiveNav('{nav_id}')" 
         title="{title}">{icon}</div>
    '''
nav_html += '</div>'

# JavaScript for click handling
nav_html += '''
<script>
function setActiveNav(navId) {
    // Remove active from all items
    document.querySelectorAll('.icon-nav-item').forEach(item => {
        item.classList.remove('active');
    });
    // Add active to clicked item
    event.target.classList.add('active');
    // Store in sessionStorage for persistence
    sessionStorage.setItem('activeNav', navId);
}
</script>
'''

st.markdown(nav_html, unsafe_allow_html=True)

# Alternative: Use Streamlit buttons for full server-side interactivity
# (Create a hidden column on the left for actual Streamlit buttons)
```

Required CSS for icon navigation:
```css
.icon-nav-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 48px;
    height: 56px;
    background: #ffffff;
    border-bottom: 1px solid #e5e5e5;
    border-right: 1px solid #e5e5e5;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 999999;
}

.icon-nav {
    position: fixed;
    left: 0;
    top: 56px;
    bottom: 0;
    width: 48px;
    background: #ffffff;
    border-right: 1px solid #e5e5e5;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 16px;
    gap: 8px;
    z-index: 999998;
}

.icon-nav-item {
    width: 32px;
    height: 32px;
    border: 2px solid #d0d0d0;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 14px;
}

.icon-nav-item.active {
    border-color: #2196f3;
    background: #e3f2fd;
    box-shadow: 0 0 8px rgba(33, 150, 243, 0.4);
}

.icon-nav-item:hover {
    border-color: #2196f3;
    transform: scale(1.1);
    transition: all 0.2s ease;
}

/* Click feedback animation */
.icon-nav-item:active {
    transform: scale(0.95);
    background: #bbdefb;
}
```

**8. RIGHT TILES PANEL (MANDATORY, CSS HOVER-BASED):**

When wireframe shows "Tiles" or vertical bar on right edge, use **CSS hover** for interactivity.
**IMPORTANT:** Streamlit strips `<script>` tags from `st.markdown`, so JavaScript won't work. Use CSS `:hover` instead.

```python
# ===== COLLAPSIBLE TILES PANEL (CSS HOVER-BASED) =====
# Collapsed by default, expands on hover - pure CSS, no JavaScript needed

st.markdown("""
<div class="tiles-panel" id="tiles-panel">
    <div class="tiles-collapse" title="Hover to expand">‹</div>
    <div class="tiles-content">
        <div class="tiles-tab-label">Tiles</div>
        <div class="tiles-icons">
            <div class="tiles-icon" title="Chart View">📊</div>
            <div class="tiles-icon" title="Table View">📋</div>
            <div class="tiles-icon" title="Map View">🗺️</div>
            <div class="tiles-icon" title="Settings">⚙️</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
```

Required CSS for tiles panel (hover-based collapse/expand):
```css
/* Tiles Panel - collapsed by default, expands on hover */
.tiles-panel {
    position: fixed;
    right: 0;
    top: 56px;
    bottom: 0;
    width: 32px;                    /* Collapsed width */
    background: #f5f5f5;
    border-left: 1px solid #e0e0e0;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 8px;
    z-index: 100;
    transition: width 0.3s ease-in-out;
    overflow: hidden;
}

/* Expand on hover */
.tiles-panel:hover {
    width: 180px;                   /* Expanded width */
}

.tiles-collapse {
    cursor: pointer;
    font-size: 16px;
    color: #666;
    padding: 4px 8px;
    margin-bottom: 4px;
    user-select: none;
    transition: transform 0.3s ease;
}

/* Rotate arrow when expanded */
.tiles-panel:hover .tiles-collapse {
    transform: rotate(180deg);
}

.tiles-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    opacity: 0;                     /* Hidden when collapsed */
    transition: opacity 0.2s ease;
    pointer-events: none;
}

/* Show content when hovering */
.tiles-panel:hover .tiles-content {
    opacity: 1;
    pointer-events: auto;
}

.tiles-tab-label {
    writing-mode: vertical-rl;
    text-orientation: mixed;
    font-size: 12px;
    color: #666;
    font-weight: 500;
    padding: 8px 0;
}

.tiles-icons {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 20px;
}

.tiles-icon {
    width: 36px;
    height: 36px;
    background: #e0e0e0;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    cursor: pointer;
    transition: background 0.2s ease, transform 0.2s ease;
}

.tiles-icon:hover {
    background: #d0d0d0;
    transform: scale(1.1);
}
```

**9. DARK/LIGHT MODE TOGGLE (PROPER IMPLEMENTATION):**

⚠️ **Common Bug Fix:** Toggle requires double-click if session state isn't initialized first.

**CORRECT Implementation (no double-click):**

```python
import streamlit as st
import altair as alt

# ===== INITIALIZE SESSION STATE FIRST (before any UI) =====
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# ===== 1. CUSTOM ALTAIR THEME (Altair's built-in "dark" still has white backgrounds!) =====
def custom_dark_theme():
    """Custom Altair theme for true dark mode charts."""
    return {
        "config": {
            "background": "#1a1a2e",
            "view": {"fill": "#1a1a2e", "stroke": "transparent"},
            "title": {"color": "#ffffff", "fontSize": 14, "fontWeight": 600},
            "axis": {
                "domainColor": "#3a3a5a",
                "gridColor": "#2a2a4a",
                "tickColor": "#3a3a5a",
                "labelColor": "#a0a0a0",
                "titleColor": "#ffffff",
            },
            "legend": {
                "labelColor": "#a0a0a0",
                "titleColor": "#ffffff",
            },
            "text": {"color": "#ffffff"},
        }
    }

# Register custom theme
alt.themes.register("custom_dark", custom_dark_theme)

# Enable theme based on dark_mode state
if st.session_state.dark_mode:
    alt.themes.enable("custom_dark")
else:
    alt.themes.enable("default")

# ===== 2. APPLY THEME CSS BASED ON SESSION STATE =====
# This must be at the TOP of your app, BEFORE other content
def apply_theme():
    """Apply theme CSS based on current mode."""
    if st.session_state.dark_mode:
        # Dark theme - Best practices from Numerro (https://www.numerro.io/blog/designing-dashboard-in-dark-mode)
        # Key principles:
        # 1. Avoid pure black (#000000) - use dark gray instead (easier on eyes, better shadows)
        # 2. Use desaturated colors - reduces visual vibration, improves legibility
        # 3. Limited contrasting colors - 4-5 max for focus
        # 4. Prioritize visualizations over text
        st.markdown("""
        <style>
        :root {
            /* ===== DARK MODE PALETTE (Numerro-inspired) ===== */
            /* Avoid pure black - use dark grays for better shadows and dexterity */
            --bg-primary: #1a1a2e;      /* Dark navy-gray (NOT #000000) */
            --bg-secondary: #16213e;    /* Slightly lighter for layering */
            --bg-tertiary: #0f3460;     /* Accent background */
            --card-bg: #1f1f3d;         /* Card surfaces */
            --hover-bg: #252550;        /* Hover states */
            
            /* Text - high contrast but not pure white */
            --text-primary: #f5f5f5;    /* Off-white for main text */
            --text-secondary: #a0a0b0;  /* Muted for secondary info */
            --text-muted: #6a6a7a;      /* Tertiary/disabled */
            
            /* Borders - subtle, not harsh */
            --border-color: #2a2a4a;
            --border-hover: #3a3a6a;
            
            /* Accent colors - desaturated for dark backgrounds */
            /* Use 4-5 contrasting colors max (Numerro recommendation) */
            --accent-primary: #4A90D9;   /* Desaturated blue */
            --accent-success: #5cb85c;   /* Desaturated green */
            --accent-warning: #f0ad4e;   /* Desaturated orange */
            --accent-danger: #d9534f;    /* Desaturated red */
            --accent-info: #5bc0de;      /* Desaturated cyan */
            
            /* KPI highlights - brighter to draw focus */
            --kpi-positive: #7dd87d;
            --kpi-negative: #ff7b7b;
        }
        
        /* Main app background - dark gray, not black */
        .stApp { 
            background: linear-gradient(135deg, var(--bg-primary) 0%, #0d0d1a 100%) !important;
        }
        
        /* Sidebar - slightly different shade for depth */
        [data-testid="stSidebar"] { 
            background: var(--bg-secondary) !important; 
            border-right: 1px solid var(--border-color) !important;
        }
        [data-testid="stSidebar"] * { color: var(--text-primary) !important; }
        
        /* Cards - elevated with subtle shadows (visible on gray, not on black) */
        .sidebar-card, .metric-card, .insight-card { 
            background: var(--card-bg) !important; 
            border: 1px solid var(--border-color) !important;
            color: var(--text-primary) !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.2s ease !important;
        }
        .sidebar-card:hover, .metric-card:hover { 
            background: var(--hover-bg) !important; 
            border-color: var(--accent-primary) !important;
            box-shadow: 0 6px 16px rgba(74, 144, 217, 0.2) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Text - readable hierarchy */
        h1, h2, h3 { color: var(--text-primary) !important; }
        h4, h5, h6 { color: var(--text-secondary) !important; }
        p, span, label { color: var(--text-secondary) !important; }
        
        /* ===== METRICS - need aggressive nested div targeting ===== */
        [data-testid="stMetric"],
        [data-testid="stMetric"] > div,
        [data-testid="stMetric"] > div > div,
        [data-testid="stMetric"] > div > div > div {
            background: var(--bg-primary) !important;
            background-color: var(--bg-primary) !important;
        }
        [data-testid="stMetricValue"] { 
            color: var(--text-primary) !important; 
            font-weight: 600 !important;
        }
        [data-testid="stMetricDelta"] { 
            color: var(--kpi-positive) !important; 
        }
        
        /* ===== WIDGETS - BaseWeb components need special selectors ===== */
        .stSelectbox > div, .stTextInput > div, .stNumberInput > div { 
            background: var(--bg-tertiary) !important; 
            border-color: var(--border-color) !important;
        }
        /* Text inputs/textareas */
        [data-baseweb="textarea"],
        [data-baseweb="textarea"] textarea,
        [data-baseweb="base-input"],
        [data-baseweb="input"] input {
            background: var(--bg-primary) !important;
            background-color: var(--bg-primary) !important;
            border-color: var(--border-color) !important;
            color: var(--text-primary) !important;
        }
        
        /* ===== CHARTS - transparent so Altair custom theme shows ===== */
        .vega-embed { background: transparent !important; }
        [data-testid="stVegaLiteChart"] { background: transparent !important; }
        
        /* ===== CUSTOM HTML ELEMENTS (outside Streamlit theming) ===== */
        .top-navbar { background: var(--bg-primary) !important; border-bottom: 1px solid var(--border-color) !important; }
        .icon-nav-header, .icon-nav { background: var(--bg-primary) !important; }
        .tiles-panel { background: var(--bg-secondary) !important; border-left: 1px solid var(--border-color) !important; }
        .sidebar-card, .insight-card { background: var(--bg-primary) !important; }
        .metric-card { background: var(--bg-primary) !important; }
        
        /* ===== BUTTONS ===== */
        .stButton > button {
            background: var(--accent-primary) !important;
            color: var(--text-primary) !important;
            border: none !important;
        }
        .stButton > button:hover {
            background: #5a9fe9 !important;
            box-shadow: 0 4px 12px rgba(74, 144, 217, 0.4) !important;
        }
        
        /* ===== EXPANDERS ===== */
        [data-testid="stExpander"] {
            background: var(--bg-primary) !important;
            border-color: var(--border-color) !important;
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        # Light theme - inspired by Anthropic (clean, minimal)
        st.markdown("""
        <style>
        :root {
            --bg-primary: #ffffff;
            --bg-secondary: #f7f7f8;
            --bg-tertiary: #f0f0f2;
            --text-primary: #1a1a1a;
            --text-secondary: #666666;
            --text-muted: #999999;
            --border-color: #e5e5e5;
            --accent: #d97706;
            --accent-hover: #b45309;
            --card-bg: #ffffff;
            --hover-bg: #f5f5f5;
        }
        
        .stApp { background-color: var(--bg-primary) !important; }
        [data-testid="stSidebar"] { 
            background: var(--bg-secondary) !important;
            border-right: 1px solid var(--border-color) !important;
        }
        
        .sidebar-card, .metric-card, .insight-card { 
            background: var(--card-bg) !important; 
            border: 1px solid var(--border-color) !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        }
        .sidebar-card:hover, .metric-card:hover { 
            border-color: var(--accent) !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.15) !important;
        }
        </style>
        """, unsafe_allow_html=True)

# Apply theme immediately
apply_theme()

# ===== 3. TOGGLE IN SIDEBAR - Use st.checkbox() for SiS Container compatibility =====
with st.sidebar:
    # ❌ WRONG - st.toggle() may not be available in SiS Container (older Streamlit)
    # st.toggle("Dark Mode", key="dark_mode")
    
    # ✅ CORRECT - st.checkbox() works everywhere including SiS Container:
    st.checkbox("🌙 Dark Mode", key="dark_mode")
    # The key= parameter automatically syncs with st.session_state.dark_mode
```

**Also create `.streamlit/config.toml` for base theming:**

```toml
# .streamlit/config.toml
[theme]
base = "light"
primaryColor = "#2196f3"

[theme.light]
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f8f9fa"
textColor = "#1a1a1a"

[theme.dark]
backgroundColor = "#0f0f1a"
secondaryBackgroundColor = "#1a1a2e"
textColor = "#ffffff"
primaryColor = "#4A90D9"
```

**Why this works (no double-click):**
1. Session state initialized BEFORE toggle renders
2. Theme CSS applied at TOP of script (before content)
3. `on_change` callback triggers immediate rerun
4. Toggle `value` reads from session state, not key

**Alternative: Use Streamlit's built-in theming via `.streamlit/config.toml`:**

```toml
# .streamlit/config.toml
[theme]
base = "dark"  # or "light"
primaryColor = "#1DB954"
backgroundColor = "#121212"
secondaryBackgroundColor = "#1e1e1e"
textColor = "#ffffff"

# For light theme alternative:
# [theme.light]
# primaryColor = "#d97706"
# backgroundColor = "#ffffff"
# secondaryBackgroundColor = "#f7f7f8"
# textColor = "#1a1a1a"
```

See [Streamlit Theming Documentation](https://docs.streamlit.io/develop/concepts/configuration/theming) for more options.

**Dark Mode Best Practices** (from [Numerro](https://www.numerro.io/blog/designing-dashboard-in-dark-mode)):

| Principle | Why | Implementation |
|-----------|-----|----------------|
| **Avoid pure black** | #000000 is harsh on eyes, limits shadow visibility | Use dark gray like `#1a1a2e` or `#121212` |
| **Use desaturated colors** | Saturated colors vibrate on dark backgrounds | Scale back saturation for chart colors |
| **Limit to 4-5 colors** | Too many colors overwhelm and defeat focus benefits | Pick contrasting accent palette |
| **Limit text** | Reading on dark is harder than light | Prioritize visualizations over tables |
| **Prioritize visualizations** | Charts tell stories without words | Use bar, line, pie charts over data tables |
| **Focus on key metrics** | Dark mode draws eye to standout elements | Make KPIs prominent with brighter colors |
| **Consider environment** | Dark mode hard to read in bright rooms | Offer both light and dark options |

**Recommended Dark Mode Color Palette:**
```css
/* Background layers (avoid pure black) */
--bg-primary: #1a1a2e;      /* Cards, containers */
--bg-secondary: #16213e;    /* Sidebar, panels */
--bg-tertiary: #0f0f1a;     /* Main app background */

/* Text (not pure white) */
--text-primary: #ffffff;    /* Main text */
--text-secondary: #a0a0a0;  /* Muted text */
--border-color: #2a2a4a;    /* Borders */

/* Accent colors (desaturated, 4-5 max) */
--accent-blue: #4A90D9;
--accent-green: #5cb85c;
--accent-orange: #f0ad4e;
--accent-red: #d9534f;
--accent-cyan: #5bc0de;
```

### 🔑 Key Lessons Learned (Dark Mode & Interactivity)

| Issue | Cause | Solution |
|-------|-------|----------|
| **JavaScript doesn't work in st.markdown** | Streamlit strips `<script>` tags for security | Use CSS `:hover` for interactivity, or `st.components.v1.html()` for JS (but renders in iframe) |
| **Collapsible panels via click** | Script tags stripped | Use CSS hover: `.panel:hover { width: 180px; }` for expand/collapse |
| **Altair charts have white backgrounds** | Built-in "dark" theme still uses white | Create custom Altair theme with `alt.themes.register()` |
| **Toggle requires double-click** | Manual assignment | Use `key=` parameter: `st.checkbox("...", key="dark_mode")` |
| **st.toggle() not available** | SiS Container uses older Streamlit | Use `st.checkbox()` instead |
| **Metrics have white backgrounds** | Deeply nested divs | Target with `[data-testid="stMetric"] > div > div > div` |
| **Text inputs stay white** | BaseWeb components | Use `[data-baseweb="textarea"]`, `[data-baseweb="input"]` selectors |
| **Custom HTML not themed** | Outside Streamlit's theming | Explicitly add dark CSS for `.top-navbar`, `.icon-nav`, `.tiles-panel` |
| **Charts show white behind** | Vega-Lite container | Add `.vega-embed { background: transparent !important; }` |

**Critical CSS Selectors for Dark Mode:**
```css
/* Metrics - need aggressive nested targeting */
[data-testid="stMetric"],
[data-testid="stMetric"] > div,
[data-testid="stMetric"] > div > div,
[data-testid="stMetric"] > div > div > div {
    background: #1a1a2e !important;
}

/* BaseWeb components (inputs, textareas) */
[data-baseweb="textarea"],
[data-baseweb="textarea"] textarea,
[data-baseweb="base-input"],
[data-baseweb="input"] input {
    background: #1a1a2e !important;
    color: #ffffff !important;
}

/* Charts - transparent so Altair theme shows */
[data-testid="stVegaLiteChart"],
.vega-embed {
    background: transparent !important;
}

/* Custom HTML elements */
.top-navbar, .icon-nav-header, .icon-nav { background: #1a1a2e !important; }
.tiles-panel { background: #16213e !important; }
.sidebar-card, .metric-card { background: #1a1a2e !important; }
```

**10. INTERACTIVE ELEMENTS (REQUIRED):**

Every dashboard must include interactivity:

```python
# Session state for tracking selections
if "selected_metric" not in st.session_state:
    st.session_state.selected_metric = "Revenue"
if "selected_channel" not in st.session_state:
    st.session_state.selected_channel = None

# Clickable KPI metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("💰", key="kpi_revenue", help="Click to drill down"):
        st.session_state.selected_metric = "Revenue"
    st.metric("Total Revenue", "$45,231", "+12.5%")

# Interactive charts with tooltips and zoom
chart = alt.Chart(df).mark_bar(cursor="pointer").encode(
    ...,
    tooltip=["field1", "field2"]
).interactive()  # Enable zoom/pan

# Clickable insight cards with feedback
if st.button("View Details", key="insight_1", use_container_width=True):
    st.success("Loading details...")  # Visual feedback

# Activity feed with clickable items
for icon, text, time in activities:
    if st.button(f"{icon} {text} • {time}", key=f"activity_{text}"):
        st.info(f"Opening: {text}")
```

**11. CHART VARIETY (Include Multiple Types):**

Every dashboard should demonstrate Streamlit's charting richness:

```python
# Bar Chart - Monthly data
bar_chart = alt.Chart(df).mark_bar(color="#4A90D9").encode(...)

# Line Chart - Trend data
line_chart = alt.Chart(df).mark_line(point=True).encode(...)

# Area Chart - Stacked data
area_chart = alt.Chart(df).mark_area(opacity=0.7).encode(
    y=alt.Y("value:Q", stack="zero"),
    color=alt.Color("category:N")
)

# ⚠️ STACKED BAR CHART - REQUIRES SPECIFIC DATA STRUCTURE
# See "Stacked Bar Chart Template" section below for complete example
```

### Stacked Bar Chart Template (CRITICAL - Empty Charts Fix)

**Common Issue:** Stacked bar charts appear EMPTY (axes visible, no bars). 

**Root Causes:**
1. Data not in "long format" (each row = one category + one group)
2. Field types wrong (using `:O` when need `:N`, or vice versa)
3. Values are zero or NaN
4. Column names don't match encoding field names

**✅ CORRECT Data Structure (Long Format):**
```python
# Data MUST be in long format: one row per (category, group) combination
stacked_data = pd.DataFrame({
    "Quarter": ["Q1", "Q1", "Q1", "Q2", "Q2", "Q2", "Q3", "Q3", "Q3", "Q4", "Q4", "Q4"],
    "Department": ["Sales", "Marketing", "Operations"] * 4,
    "Amount": [120, 80, 60, 150, 90, 70, 180, 100, 85, 200, 110, 95]  # MUST have non-zero values!
})
```

**✅ CORRECT Stacked Bar Chart:**
```python
# Stacked Bar Chart - Quarterly by Department
st.markdown("**Stacked Bar - Quarterly by Department**")

stacked_data = pd.DataFrame({
    "Quarter": ["Q1", "Q1", "Q1", "Q2", "Q2", "Q2", "Q3", "Q3", "Q3", "Q4", "Q4", "Q4"],
    "Department": ["Sales", "Marketing", "Operations"] * 4,
    "Amount": [120, 80, 60, 150, 90, 70, 180, 100, 85, 200, 110, 95]
})

stacked_bar = (
    alt.Chart(stacked_data)
    .mark_bar()
    .encode(
        x=alt.X("Quarter:N", title="Quarter", sort=["Q1", "Q2", "Q3", "Q4"]),
        y=alt.Y("Amount:Q", title="Amount ($K)", stack="zero"),  # stack="zero" for stacking!
        color=alt.Color(
            "Department:N",
            scale=alt.Scale(
                domain=["Sales", "Marketing", "Operations"],
                range=["#4A90D9", "#d9534f", "#5cb85c"]
            ),
            legend=alt.Legend(title="Department", orient="bottom")
        ),
        tooltip=[
            alt.Tooltip("Quarter:N"),
            alt.Tooltip("Department:N"),
            alt.Tooltip("Amount:Q", title="Amount", format="$,.0f")
        ],
    )
    .properties(height=300)
)
st.altair_chart(stacked_bar, use_container_width=True)
```

**❌ WRONG - Causes Empty Chart:**
```python
# ❌ WRONG: Data in "wide format" - stacking won't work
wrong_data = pd.DataFrame({
    "Quarter": ["Q1", "Q2", "Q3", "Q4"],
    "Sales": [120, 150, 180, 200],       # This won't stack!
    "Marketing": [80, 90, 100, 110],
})

# ❌ WRONG: Field type mismatch
alt.X("Quarter:O")  # Using :O when data needs :N

# ❌ WRONG: Missing stack parameter
alt.Y("Amount:Q")  # Implicitly stacks, but explicit is safer

# ❌ WRONG: Column name doesn't exist
alt.X("quarter:N")  # lowercase 'quarter' but data has 'Quarter'
```

**Debug Empty Stacked Bar:**
```python
# Add this before the chart to verify data:
st.write("DEBUG - Data shape:", stacked_data.shape)
st.write("DEBUG - First rows:", stacked_data.head())
st.write("DEBUG - Value range:", stacked_data["Amount"].min(), "-", stacked_data["Amount"].max())
```

# Pie/Donut Chart - Distribution
pie_chart = alt.Chart(df).mark_arc(innerRadius=50).encode(
    theta="value:Q",
    color="category:N"
)

# Multi-line Comparison
multi_line = alt.Chart(df_melted).mark_line(point=True).encode(
    color="series:N"
)
```

### Phase 2: Generate Streamlit Code

Create a single `streamlit_app.py` that works across all 4 environments.

**⚠️ COMMON MISTAKES TO AVOID:**

| Mistake | Result | Fix |
|---------|--------|-----|
| Using "Predictive Item" literally | Generic placeholder cards | Generate specific names: "Revenue Forecast", "Churn Risk" |
| Skipping right panel | Missing metrics/actions | ALWAYS implement right column with metrics + buttons |
| Charts without titles | Unlabeled visualizations | Add `st.markdown("**Chart Title**")` before EVERY chart |
| Empty insight cards | Just boxes with lines | Include: icon, title, 2 description lines, action text |
| Missing legends | Can't interpret multi-series | Add legend to all multi-series charts |
| Placeholder values | "Value" or "XXX" | Use realistic: "$45,231", "1,247 users", "3.24%" |
| No tooltips | Can't explore data | Add tooltips to ALL Altair charts |
| Missing axis labels | Unclear what chart shows | Always specify `title=` in x/y encoding |

**Critical Technical Rules:**

```python
# ✅ ALWAYS use explicit Altair charts with hardcoded colors
st.markdown("**Monthly Revenue**")  # TITLE REQUIRED
chart = alt.Chart(df).mark_bar(color="#4A90D9").encode(
    x=alt.X("month:O", title="Month"),  # AXIS LABEL REQUIRED
    y=alt.Y("value:Q", title="Revenue ($)"),  # AXIS LABEL REQUIRED
    tooltip=["month", alt.Tooltip("value:Q", format="$,.0f")]  # TOOLTIPS REQUIRED
)

# ✅ ALWAYS format data with pandas (not column_config)
df["Revenue"] = df["Revenue"].apply(lambda x: f"${x:,}")
st.dataframe(df, use_container_width=True)

# ✅ ALWAYS use session state for interactivity
if "selected" not in st.session_state:
    st.session_state.selected = None

# ❌ NEVER use st.column_config (breaks SiS Container)
# ❌ NEVER use st.bar_chart/line_chart (colors vary)
# ❌ NEVER use external fonts (blocked by CSP)
```

**Wireframe Element → Rich Content Examples:**

```
WIREFRAME:                         GENERATED CODE:
┌────────────────┐                 
│ Predictive Item│     →           "Revenue Forecast"
│ ───────────────│     →           "Q4 projection: $128K"  
│ ───────────────│     →           "↑ 23% vs last quarter"
└────────────────┘

┌─────────────────┐
│   [Bar Chart]   │    →           st.markdown("**Monthly Revenue**")
│   ▌▌▐▌▐▐▌▌▐▌   │    →           alt.Chart with title, axis labels, tooltips
└─────────────────┘

┌─────────────────┐
│ [metric box]    │    →           "TODAY'S VISITORS"
│                 │    →           "1,247"
│                 │    →           "↑ 12% vs yesterday"
└─────────────────┘

┌─────────────────┐
│ ✦ Try This      │    →           st.button("✦ Optimize ad spend")
│ ✦ Try This      │    →           st.button("✦ Review churn users")
└─────────────────┘
```

### Phase 3: Generate Configuration Files

Create all required files:

| File | Purpose | Version Syntax |
|------|---------|----------------|
| `pyproject.toml` | Localhost uv deps | `streamlit>=1.51.0` ✅ operators allowed |
| `environment.yml` | SiS Warehouse Conda | `streamlit` ⚠️ **NO version operators!** |
| `requirements.txt` | SiS Container pip | `streamlit>=1.51.0` ✅ operators allowed |
| `snowflake.yml` | snow CLI project | `definition_version: 2` |
| `spcs/Dockerfile` | SPCS container | `python:3.11-slim` + uv |
| `spcs/spec.yaml` | Service spec | `public: true` endpoint |

### Phase 4: Lint, Format & Type Check

**Use modern Python tooling before running:**

```bash
# Lint and auto-fix
ruff check streamlit_app.py --fix

# Format code
ruff format streamlit_app.py

# Type check (optional but recommended)
ty check streamlit_app.py
```

### Phase 5: Run & Validate Locally

Start the app using **uv** (never raw `pip` or `python`):

```bash
# Install dependencies with uv
uv sync

# Start the app with uv
uv run streamlit run streamlit_app.py --server.port 8501
```

**🔴 DO NOT STOP HERE. YOU MUST CONTINUE TO PHASE 6: VISUAL VALIDATION LOOP.**

### Phase 6: Visual Validation Loop 🧠 (EXACTLY 5 ITERATIONS - MANDATORY)

**🔴 YOU MUST RUN THIS LOOP EXACTLY 5 TIMES. NO EARLY EXIT.**

**🔴 DO NOT FINALIZE YOUR TODO LIST UNTIL ALL 5 ITERATIONS ARE COMPLETE.**

```python
# EXACTLY 5 iterations - no break, no early exit
for iteration in [1, 2, 3, 4, 5]:
    print(f"\n{'='*60}")
    print(f"VISUAL VALIDATION - Iteration {iteration}/5")
    print(f"{'='*60}\n")
    
    # Step 1: Get screenshot
    screenshot = take_screenshot("http://localhost:8501")
    # OR: Ask user to provide screenshot
    
    # Step 2: Analyze against wireframe
    score, improvements = analyze_screenshot_vs_wireframe(screenshot, original_wireframe)
    
    # Step 3: Output validation report
    print(f"Score: {score}/100")
    print(f"Improvements identified: {len(improvements)}")
    
    # Step 4: List improvements (ALWAYS find at least one, even if minor)
    for i, improvement in enumerate(improvements, 1):
        print(f"  {i}. {improvement}")
    
    # Step 5: Implement improvements
    for improvement in improvements:
        implement_improvement(improvement)
    
    # Step 6: Lint and format
    run("ruff check streamlit_app.py --fix")
    run("ruff format streamlit_app.py")
    
    # Step 7: Restart app for next iteration
    restart_streamlit_app()  # uv run streamlit run ...
    
    print(f"✓ Iteration {iteration}/5 complete. Improvements applied.")

# Only after ALL 5 iterations
print("\n✅ All 5 visual evaluations complete.")
print("🌐 Localhost ready at http://localhost:8501")
print("📋 Say 'deploy to snowflake' when ready to deploy to Snowflake.")
```

**What to do in EACH of the 5 iterations:**

1. **SCREENSHOT**: Take or request screenshot of running app
2. **ANALYZE**: Compare against original wireframe using checklist
3. **SCORE**: Calculate visual quality score (0-100)
4. **LIST**: Identify improvements (always find at least one, even minor polish)
5. **IMPLEMENT**: Apply the improvements to code
6. **LINT**: Run `ruff check streamlit_app.py --fix` and `ruff format streamlit_app.py`
7. **RESTART**: Restart app for next iteration

**Output after EACH iteration:**
```
═══════════════════════════════════════════════════════════
VISUAL VALIDATION - Iteration N/5
═══════════════════════════════════════════════════════════
Score: XX/100

Improvements implemented:
1. [improvement 1]
2. [improvement 2]
...

Status: ✓ Iteration N/5 complete. Proceeding to iteration N+1.
═══════════════════════════════════════════════════════════
```

See "Visual Validation Loop" section for detailed checklist and scoring criteria.

### Phase 7: Localhost Ready (STOP HERE - Wait for User)

**⚠️ AFTER COMPLETING 5 VISUAL VALIDATION ITERATIONS:**

**YOU MUST OUTPUT THIS MESSAGE (copy exactly):**

```
════════════════════════════════════════════════════════════════════════
✅ STREAMLIT APP IS RUNNING!
════════════════════════════════════════════════════════════════════════

🌐 Open in your browser:

   👉 http://localhost:8501

────────────────────────────────────────────────────────────────────────
Visual Validation: Complete
Final Score: XX/100

📋 NEXT STEPS:

1. Review the app in your browser at http://localhost:8501
2. When satisfied, say "deploy to snowflake" to continue

⚠️ Waiting for your review before Snowflake deployment...
════════════════════════════════════════════════════════════════════════
```

**⛔ DO NOT:**
- Auto-deploy to Snowflake
- Mark deployment todos as complete
- Close the localhost app

**✅ DO:**
- Keep localhost running at http://localhost:8501
- Output the URL prominently so user can open it
- Wait for user to review the dashboard
- Wait for explicit deployment request

---

### Phase 8: Deploy to Snowflake (ONLY WHEN USER REQUESTS)

**⚠️ TRIGGER:** User explicitly says "deploy to snowflake" or similar.

**DO NOT proceed to this phase automatically.**

When user requests deployment:

**Step 8a: Generate Deployment Files (not created earlier)**

```bash
# These files are ONLY created now, after user requests deployment:
├── environment.yml       # SiS Warehouse (Conda dependencies)
├── requirements.txt      # SiS Container (pip dependencies)
├── snowflake.yml         # Snowflake CLI project definition
└── spcs/
    ├── Dockerfile        # Raw SPCS container
    ├── spec.yaml         # SPCS service specification
    └── requirements-spcs.txt
```

**Step 8b: Configure snow CLI Connection**

⚠️ **IMPORTANT:** `snow connection add` prompts for password interactively and FAILS in non-interactive terminals.

**Option 1: Reuse existing connection (PREFERRED)**
```bash
# List available connections
snow connection list

# Use an existing connection
snow streamlit deploy app_warehouse --connection MY_EXISTING_CONN
```

**Option 2: Edit config.toml directly (for new connections)**
```bash
# Edit ~/.snowflake/config.toml
cat >> ~/.snowflake/config.toml << 'EOF'

[connections.myconn]
account = "account-id"
user = "username"
authenticator = "externalbrowser"  # or SNOWFLAKE_JWT, USERNAME_PASSWORD_MFA
warehouse = "COMPUTE_WH"
database = "MY_DB"
schema = "PUBLIC"
EOF
```

**Step 8c: Deploy**

```bash
# Generate timestamp for unique naming (underscores, not hyphens!)
TIMESTAMP=$(date +%Y_%m_%d_%H_%M)

# 1. SiS Warehouse (snow CLI)
# Name in snowflake.yml should include timestamp and (Warehouse) in title
snow streamlit deploy app_warehouse --connection <conn> --replace

# 2. SiS Container (MUST use SQL - snow CLI doesn't support runtime field)
# ⚠️ NO EXTERNAL_ACCESS_INTEGRATIONS needed for demo dashboards
# ⚠️ NO RUNTIME_NAME needed - just specify COMPUTE_POOL
snow stage copy streamlit_app.py @STAGE/app/ -c <conn> --overwrite
snow stage copy requirements.txt @STAGE/app/ -c <conn> --overwrite
snow sql -c <conn> -q "
  CREATE OR REPLACE STREAMLIT DB.SCHEMA.APP_NAME_${TIMESTAMP}
    FROM '@STAGE/app/'
    MAIN_FILE = 'streamlit_app.py'
    TITLE = '${TIMESTAMP} App Title (Container)'
    QUERY_WAREHOUSE = COMPUTE_WH
    COMPUTE_POOL = MY_COMPUTE_POOL;
"

# 3. Raw SPCS (Docker + snow CLI)
cd spcs && cp ../streamlit_app.py .
docker build --platform linux/amd64 -t app:latest .
snow spcs image-registry login --connection <conn>
docker push <registry>/app:latest
snow sql -c <conn> -q "CREATE SERVICE..."
```

**After Snowflake deployment, commit the deployment files:**
```bash
git add -A
git commit -m "Add Snowflake deployment files (Warehouse, Container, SPCS)"
```

**Final Output (ONLY after user requests Snowflake deployment):**
```
═══════════════════════════════════════════════════════════
SNOWFLAKE DEPLOYMENT COMPLETE
═══════════════════════════════════════════════════════════
Visual Validation: PASSED (Score: XX/100, Iterations: 5)

Deployed to:
✅ Localhost: http://localhost:8501 (was already running)
✅ SiS Warehouse: [URL]
✅ SiS Container: [URL]  
✅ SPCS: [URL]

📦 Deployment files committed to git
All 4 variants now running!
═══════════════════════════════════════════════════════════
```

**⚠️ Only show this after user explicitly requested Snowflake deployment.**

## Common Errors and Fixes

### 1. environment.yml Version Specifier Error

**Error:**
```
Anaconda dependency names must be lowercase characters, numbers or one of [.-_]. 
{0} does not match this spec.
```

**Cause:** Using pip-style version specifiers (`>=`, `==`, `<`) in environment.yml

```yaml
# ❌ WRONG - Version operators not allowed in Snowflake Anaconda channel
dependencies:
  - streamlit>=1.35.0
  - pandas==2.0.0
  - numpy<2

# ✅ CORRECT - Plain package names only
dependencies:
  - streamlit
  - pandas
  - numpy
```

**Note:** Snowflake's Anaconda channel manages versions automatically based on compatibility.

---

### 2. snow CLI Connection Prompt Failure

**Error:**
```
Warning: Password input may be echoed.
Enter password:
Aborted.
```

**Cause:** `snow connection add` prompts interactively, fails in non-interactive terminals.

**Fix:** Reuse existing connection or edit config directly:
```bash
# Option 1: List and reuse existing
snow connection list
snow streamlit deploy --connection EXISTING_CONN

# Option 2: Edit config.toml directly (for externalbrowser auth)
echo '[connections.myconn]
account = "myaccount"
user = "myuser"
authenticator = "externalbrowser"' >> ~/.snowflake/config.toml

# Option 3: Edit config.toml for Programmatic Access Token (PAT)
cat >> ~/.snowflake/config.toml << 'EOF'

[connections.myconn-pat]
account = "xxx-yyy"
user = "myuser"
authenticator = "PROGRAMMATIC_ACCESS_TOKEN"
token_file_path = "/path/to/.snowflake-token"
EOF
```

---

### 3. Ruff Line Length Violations (E501)

CSS strings in Python must not exceed 100 characters per line.

```python
# ❌ WRONG - Too long (137 chars), triggers E501
st.markdown("""<style>[data-testid="stSidebar"] { background: #fff; }</style>""")

# ✅ CORRECT - Multi-line CSS
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-color) !important;
}
</style>
""")
```

---

### 4. Import Order (I001)

Ruff expects imports in alphabetical order. Auto-fixed with `ruff check --fix`.

```python
# ❌ WRONG - Triggers I001
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# ✅ CORRECT - Alphabetical order
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
```

**Note:** `ruff check --fix` auto-fixes this, but writing in correct order avoids churn.

---

### 5. Unused Loop Variable (B007)

```python
# ❌ WRONG - Triggers B007
for nav_id, icon_type in nav_items:
    print(nav_id)  # icon_type unused

# ✅ CORRECT - Prefix with underscore
for nav_id, _icon_type in nav_items:
    print(nav_id)
```

---

### 6. Hatchling Build Failure

If `uv sync` fails with "Unable to determine which files to ship":

```bash
# ❌ This fails for script-only projects
uv sync

# ✅ WORKAROUND - Use pip install instead
uv venv && source .venv/bin/activate && uv pip install streamlit pandas numpy "altair>=5.0"
```

**Fix in pyproject.toml:** Remove `[build-system]` section for script-only projects:
```toml
# DO NOT include this for script-only projects:
# [build-system]
# requires = ["hatchling"]
# build-backend = "hatchling.build"
```

---

### 7. Self-Assessment False Positives

Missing deployment files flagged as critical in localhost-only mode.

```bash
# ✅ Use --localhost-only flag (or auto-detected)
python self-assess.py . --localhost-only --fix
```

The script auto-detects localhost-only mode if only `streamlit_app.py` and `pyproject.toml` exist.

---

### 9. snowflake.yml `runtime` Field Not Supported

**Error:**
```
Extra inputs are not permitted. You provided field
'entities.app.streamlit.runtime' with value {...}
that is not supported in given version.
```

**Cause:** `snowflake.yml` v2 does NOT support `runtime:` block for Streamlit entities.

**Fix:** Deploy SiS Container via SQL, not `snow streamlit deploy`:
```bash
# ❌ WRONG - snowflake.yml can't specify container runtime
snow streamlit deploy app_container --connection <conn>

# ✅ CORRECT - Use SQL directly
snow stage copy streamlit_app.py @STAGE/app/ -c <conn> --overwrite
snow stage copy requirements.txt @STAGE/app/ -c <conn> --overwrite
snow sql -c <conn> -q "CREATE STREAMLIT ... COMPUTE_POOL = <pool>;"
```

---

### 10. Invalid RUNTIME_NAME in CREATE STREAMLIT

**Error:**
```
092857 (42601): Runtime {0} is not valid for Streamlit in Snowflake applications.
```

**Cause:** `RUNTIME_NAME = 'CONTAINER'` is not a valid parameter.

**Fix:** Omit `RUNTIME_NAME`, just specify `COMPUTE_POOL`:
```sql
-- ❌ WRONG
CREATE STREAMLIT app
  FROM '@stage/'
  RUNTIME_NAME = 'CONTAINER'
  COMPUTE_POOL = my_pool;

-- ✅ CORRECT
CREATE STREAMLIT app
  FROM '@stage/'
  MAIN_FILE = 'streamlit_app.py'
  QUERY_WAREHOUSE = COMPUTE_WH
  COMPUTE_POOL = my_pool;
```

---

### 11. st.toggle() Not Available

**Error:**
```
AttributeError: module 'streamlit' has no attribute 'toggle'
```

**Cause:** `st.toggle()` was added in Streamlit 1.23. SiS Container may use older version.

**Fix:** Use `st.checkbox()` instead for SiS Container compatibility:
```python
# ❌ WRONG - st.toggle() not available in older Streamlit
dark_mode = st.toggle("🌙 Dark Mode", key="dark_mode")

# ✅ CORRECT - st.checkbox() works everywhere
dark_mode = st.checkbox("🌙 Dark Mode", key="dark_mode")
```

---

### 12. st.dataframe(hide_index=True) Not Available

**Error:**
```
TypeError: DataFrameSelectorMixin.dataframe() got an unexpected keyword argument 'hide_index'
```

**Cause:** The `hide_index` parameter was added in Streamlit 1.16.0. SiS Container may use older version.

**Fix:** Set empty string index instead of using `hide_index=True`:
```python
# ❌ WRONG - hide_index not available in older Streamlit (SiS Container)
st.dataframe(df, use_container_width=True, hide_index=True)

# ✅ CORRECT - Works in all environments
df.index = [""] * len(df)  # Hide index by setting empty strings
st.dataframe(df, use_container_width=True)
```

---

### 13. Altair xOffset Not Supported in SiS Container

**Error:**
```
SchemaValidationError: Invalid specification altair.vegalite.v4.schema.core.FacetedEncoding,
validating 'additionalProperties' Additional properties are not allowed ('xOffset' was unexpected)
```

**Cause:** `xOffset` encoding was added in Altair 5.0. SiS Container runtime uses Altair 4.x.

**Fix:** Use `column` faceting instead of `xOffset` for grouped bar charts:
```python
# ❌ WRONG - xOffset not available in Altair 4.x (SiS Container)
grouped_bar = alt.Chart(data).mark_bar().encode(
    x="Category:N",
    y="Value:Q",
    color="Group:N",
    xOffset="Group:N",  # <-- BREAKS on SiS Container
)

# ✅ CORRECT - column faceting works everywhere (Altair 4.x compatible)
grouped_bar = alt.Chart(data).mark_bar().encode(
    x=alt.X("Group:N", title="", axis=alt.Axis(labelAngle=0)),
    y=alt.Y("Value:Q", title="Amount ($)"),
    color=alt.Color("Group:N", legend=None),  # Hide legend, labels on x-axis
    column=alt.Column(
        "Category:N",
        title="",
        header=alt.Header(labelOrient="bottom"),
    ),
).properties(height=280, width=120)  # Set width per facet
```

---

### 14. Stacked Bar Chart Appears Empty

**Symptom:** Stacked bar chart shows axes and legend but NO BARS visible.

**Common Causes:**
1. Data in "wide format" instead of "long format"
2. Field type mismatch (`:O` vs `:N` vs `:Q`)
3. Column names don't match encoding field names (case-sensitive!)
4. Values are zero, NaN, or missing

**Debug:**
```python
# Add before chart to verify data:
st.write("Data shape:", df.shape)
st.write("First rows:", df.head())
st.write("Value range:", df["Amount"].min(), "-", df["Amount"].max())
```

**Fix - Ensure Long Format Data:**
```python
# ❌ WRONG - Wide format (causes empty chart)
wrong_data = pd.DataFrame({
    "Quarter": ["Q1", "Q2", "Q3", "Q4"],
    "Sales": [120, 150, 180, 200],
    "Marketing": [80, 90, 100, 110],
})

# ✅ CORRECT - Long format (one row per category+group)
correct_data = pd.DataFrame({
    "Quarter": ["Q1", "Q1", "Q2", "Q2", "Q3", "Q3", "Q4", "Q4"],
    "Department": ["Sales", "Marketing"] * 4,
    "Amount": [120, 80, 150, 90, 180, 100, 200, 110]  # Non-zero values!
})

# ✅ CORRECT chart encoding
stacked_bar = alt.Chart(correct_data).mark_bar().encode(
    x=alt.X("Quarter:N", title="Quarter"),
    y=alt.Y("Amount:Q", title="Amount", stack="zero"),  # Explicit stack!
    color=alt.Color("Department:N"),
    tooltip=["Quarter", "Department", "Amount"]
)
```

**See "Stacked Bar Chart Template" section for complete working example.**

---

### 15. Image Placeholder Text Instead of Actual Image

**Symptom:** Dashboard shows "Image placeholder" text instead of an actual image.

**Cause:** Using `st.markdown()` or `st.text()` for images instead of `st.image()`.

**Fix:**
```python
# ❌ WRONG - Text placeholder (NEVER DO THIS)
st.markdown("Image placeholder")
st.text("Image placeholder")
st.write("🖼️ Image goes here")

# ✅ CORRECT - Use st.image() with actual URL
st.image("https://picsum.photos/seed/dashboard/400/300", caption="Featured Image")

# ✅ For avatars
st.image("https://api.dicebear.com/7.x/avataaars/svg?seed=user", width=100)

# ✅ For specific content from wireframe
st.image("https://upload.wikimedia.org/...", caption="Description")
```

**Image URL Resources:**
- Generic photos: `https://picsum.photos/{width}/{height}` or `https://picsum.photos/seed/{name}/{w}/{h}`
- Avatars: `https://api.dicebear.com/7.x/avataaars/svg?seed={name}`
- Unsplash: `https://images.unsplash.com/photo-{id}?w={w}&h={h}&fit=crop`

---

### Error Summary by Environment

| Environment | # | Key Issues | Status |
|-------------|---|------------|--------|
| **SiS Warehouse** | 1 | Version specifiers in environment.yml | ✅ Fixed |
| **SiS Container** | 6 | snowflake.yml, SQL, st.toggle(), hide_index, xOffset | ✅ Fixed |
| **SPCS** | 0 | None | ✅ OK |

---

## Critical Compatibility Rules

### Streamlit Feature Compatibility Table

| Feature | Min Version | SiS Container Safe | Alternative |
|---------|-------------|-------------------|-------------|
| `st.toggle()` | 1.23+ | ⚠️ Maybe not | `st.checkbox()` |
| `st.column_config` | 1.35+ | ❌ No | Pandas formatting |
| `st.data_editor` | 1.23+ | ⚠️ Maybe not | `st.dataframe()` |
| `st.dataframe(hide_index=True)` | 1.16+ | ❌ No | `df.index = [""] * len(df)` |
| `st.chat_input` | 1.23+ | ⚠️ Maybe not | `st.text_input()` |
| `st.bar_chart` | Always | ⚠️ Colors vary | `alt.Chart().mark_bar()` |
| External fonts | N/A | ❌ Blocked by CSP | System fonts |

### Altair Feature Compatibility Table

| Feature | Min Version | SiS Container Safe | Alternative |
|---------|-------------|-------------------|-------------|
| `xOffset` encoding | Altair 5.0+ | ❌ No | `column` faceting |
| `yOffset` encoding | Altair 5.0+ | ❌ No | `row` faceting |
| `alt.expr()` | Altair 5.0+ | ⚠️ Maybe not | Use `alt.datum` |
| `alt.param()` | Altair 5.0+ | ⚠️ Maybe not | Use `alt.selection()` |

### Must AVOID

```python
# ❌ Breaks in SiS Container (may use older Streamlit)
st.toggle("Dark Mode")  # Use st.checkbox() instead
st.column_config.NumberColumn()
st.column_config.ProgressColumn()
st.data_editor(df)
st.dataframe(df, hide_index=True)  # hide_index added in 1.16+

# ❌ Altair 5.0+ features that break SiS Container (uses Altair 4.x)
chart.encode(xOffset="field:N")  # Use column= faceting instead
chart.encode(yOffset="field:N")  # Use row= faceting instead

# ❌ Inconsistent colors across environments
st.bar_chart(df)
st.line_chart(df)

# ❌ Blocked by CSP in SiS
@import url('https://fonts.googleapis.com/...')
```

### Must USE

```python
# ✅ st.checkbox() instead of st.toggle() (works everywhere)
dark_mode = st.checkbox("🌙 Dark Mode", key="dark_mode")

# ✅ Hide index without hide_index parameter (works everywhere)
df.index = [""] * len(df)  # Set empty string index
st.dataframe(df, use_container_width=True)

# ✅ Explicit Altair with hardcoded colors
alt.Chart(df).mark_bar(color="#4A90D9").encode(...)

# ✅ Grouped bar charts using column faceting (Altair 4.x compatible)
alt.Chart(data).mark_bar().encode(
    x=alt.X("Group:N", axis=alt.Axis(labelAngle=0)),
    y=alt.Y("Value:Q"),
    color="Group:N",
    column=alt.Column("Category:N"),  # Instead of xOffset
).properties(width=100)

# ✅ Pandas formatting for tables (not st.column_config)
df["Revenue"] = df["Revenue"].apply(lambda x: f"${x:,}")

# ✅ System fonts only
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### SiS Container Deployment Rules

⚠️ **IMPORTANT for SiS Container runtime:**

1. **No `runtime:` in snowflake.yml** - Deploy via SQL instead
2. **No `RUNTIME_NAME`** - Just specify `COMPUTE_POOL`
3. **No `EXTERNAL_ACCESS_INTEGRATIONS`** - Not needed for demo dashboards
4. **No BCR checks** - Not applicable for Streamlit apps
5. **Use `st.checkbox()`** - `st.toggle()` may not be available

## Version Strategy

**Goal:** Always use the most recent stable AND working versions across all 4 environments.

### Reference URLs (Always Check Before Generating)

| Resource | URL | Purpose |
|----------|-----|---------|
| **SiS Release Notes** | https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake | Latest supported Streamlit versions in SiS |
| **SiS Limitations** | https://docs.snowflake.com/en/developer-guide/streamlit/limitations | Current limitations for SiS Warehouse |
| **PyPI Streamlit** | https://pypi.org/project/streamlit/ | Latest Streamlit version |

### Current Version Matrix (January 2026)

Based on [Snowflake SiS Release Notes](https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake):
- **Nov 20, 2025:** Streamlit 1.47, 1.48, 1.49.1, 1.50, 1.51 now GA in SiS
- **Dec 11, 2025:** SiS Container Runtime now in Preview
- **Latest PyPI:** Streamlit 1.52.2 (Dec 17, 2025)

### Version Requirements

| Component | Minimum | Recommended | Notes |
|-----------|---------|-------------|-------|
| **Python** | 3.13+ | Latest 3.13.x | Use latest stable |
| **Streamlit** | 1.51+ | Latest in SiS | Check release notes |
| **pandas** | Latest | Latest | Widely compatible |
| **numpy** | Latest | Latest | Widely compatible |
| **altair** | 5.0+ | Latest | Required for explicit colors |

### Environment Constraints

- **SiS Warehouse:** Check [SiS Limitations](https://docs.snowflake.com/en/developer-guide/streamlit/limitations) for current restrictions
- **SiS Container:** Preview feature (Dec 2025), may have different constraints
- **Raw SPCS:** Full control, can use any PyPI version

### Tooling Requirements

Always use latest versions of modern Python tooling:

```bash
# Install/update latest tooling
uv self update              # Update uv itself
uv tool install ruff        # Latest ruff
uv tool install ty          # Latest ty
```

| Tool | Purpose | Auto-fix |
|------|---------|----------|
| **uv** | Package management | N/A |
| **ruff** | Linting + formatting | `ruff check streamlit_app.py --fix && ruff format streamlit_app.py` |
| **ty** | Type checking | Reports only |

## File Templates

### pyproject.toml
```toml
[project]
name = "streamlit-app"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "streamlit>=1.51",  # Min 1.51, check SiS release notes for max
    "pandas",
    "numpy",
    "altair>=5.0",
]

[dependency-groups]
dev = ["ruff"]

[tool.ruff]
line-length = 100
target-version = "py313"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "SIM"]

[tool.ruff.format]
quote-style = "double"
```

### environment.yml
```yaml
# SiS Warehouse Runtime - Check SiS release notes for supported versions
# https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake
#
# ⚠️ CRITICAL: Snowflake's Anaconda channel does NOT support version operators!
# ❌ WRONG: streamlit>=1.51.0, pandas==2.0, numpy<2
# ✅ CORRECT: streamlit, pandas, numpy (plain names only)
#
name: streamlit_env
channels:
  - snowflake  # MUST use snowflake channel (NOT conda-forge)
dependencies:
  # NO VERSION SPECIFIERS ALLOWED - Snowflake manages versions
  - streamlit
  - pandas
  - numpy
  - altair
```

### requirements.txt (SiS Container)
```
# SiS Container Runtime (Preview as of Dec 2025)
# Check limitations: https://docs.snowflake.com/en/developer-guide/streamlit/limitations
streamlit>=1.51
pandas
numpy
altair
```

### snowflake.yml
```yaml
definition_version: 2
entities:
  # SiS Warehouse - use snow streamlit deploy
  app_warehouse:
    type: streamlit
    identifier:
      name: APP_NAME_2026_01_07_14_30  # Underscores, not hyphens!
    title: "2026_01_07_14_30 App Title (Warehouse)"  # Timestamp prefix for Snowsight!
    query_warehouse: COMPUTE_WH
    main_file: streamlit_app.py
    artifacts:
      - streamlit_app.py
      - environment.yml

# NOTE: SiS Container CANNOT be deployed via snowflake.yml
# Must use SQL with COMPUTE_POOL parameter instead
```

### spcs/Dockerfile
```dockerfile
# Use 3.11-slim for smaller image + faster push (~20-30s savings)
FROM python:3.11-slim

# Install curl for healthcheck (often missing in slim images)
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency installation
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy requirements FIRST for layer caching
# (deps change less often than code)
COPY requirements-spcs.txt .
RUN uv pip install --system --no-cache -r requirements-spcs.txt

# Copy app code LAST (changes most often)
COPY streamlit_app.py .

EXPOSE 8501
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1
CMD ["streamlit", "run", "streamlit_app.py", \
     "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
```

**Docker Build Tips:**
```bash
# Use BuildKit for faster builds
DOCKER_BUILDKIT=1 docker build --platform linux/amd64 -t app:latest .

# Prune before push (reduces size)
docker image prune -f

# Tag with timestamp for versioning (underscores for Snowflake compatibility)
TIMESTAMP=$(date +%Y_%m_%d_%H_%M)
docker tag app:latest <registry>/app:${TIMESTAMP}
```

### spcs/requirements-spcs.txt
```
# Raw SPCS - can use latest PyPI version
# Check https://pypi.org/project/streamlit/ for latest
streamlit>=1.51
pandas
numpy
altair>=5.0
```

### spcs/spec.yaml

**⚠️ NOTE:** This file is for **reference/documentation only**. When creating the service,
you must **inline the spec** in SQL. `snow spcs service create --spec-path` requires staging
the file first — inlining is simpler for single-file specs.

```yaml
# Service name should include timestamp: app_name_2026_01_07_14_30
spec:
  containers:
    - name: streamlit
      image: /DB/SCHEMA/REPO/app:latest  # Or use :YYYY_MM_DD_HH_MM tag
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

**Inline the spec in SQL:**
```sql
CREATE SERVICE DB.SCHEMA.MY_SERVICE_2026_01_07_14_30
  IN COMPUTE POOL MY_COMPUTE_POOL
  FROM SPECIFICATION $$
spec:
  containers:
    - name: streamlit
      image: /DB/SCHEMA/REPO/app:2026_01_07_14_30
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
$$;
```

### SPCS Endpoint Provisioning

After `CREATE SERVICE`, the container starts immediately but the **public endpoint takes 2-5 minutes** to provision:

```bash
# Check endpoint status (poll until URL appears)
snow sql -c <conn> -q "SHOW ENDPOINTS IN SERVICE DB.SCHEMA.MY_SERVICE;"

# Initially shows: "Endpoints provisioning in progress..."
# After 2-5 min: Returns actual URL like "mchrhd-xxx.snowflakecomputing.app"
```

### SPCS Troubleshooting: "No service hosts found"

**If browser shows:** `{"responseType":"ERROR","detail":"Service X not reachable: no service hosts found."}`

**This means the service isn't ready yet. Diagnose with:**

```sql
-- 1. Check service status (should be READY, not PENDING/STARTING)
SHOW SERVICES LIKE '%MY_SERVICE%';

-- 2. Check container logs for crashes
SELECT * FROM TABLE(GET_SERVICE_LOGS('MY_SERVICE', 'streamlit'))
ORDER BY timestamp DESC LIMIT 50;

-- 3. Check compute pool is running (not SUSPENDED)
SHOW COMPUTE POOLS;

-- 4. Check endpoint provisioning
SHOW ENDPOINTS IN SERVICE MY_SERVICE;
```

**Common causes:**
| Cause | Solution |
|-------|----------|
| Service still starting | Wait 2-5 min for compute pool + container |
| Container crashed | Check logs for Python errors |
| Compute pool suspended | `ALTER COMPUTE POOL MY_POOL RESUME;` |
| Endpoint provisioning | Wait 2-5 min after service starts |

**See `references/troubleshooting.md` for detailed diagnosis steps.**

## Complete CSS Template (Reference)

Include this comprehensive CSS in every generated dashboard:

```python
st.markdown("""
<style>
/* ========== VARIABLES ========== */
:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f8f9fa;
    --text-primary: #1a1a1a;
    --text-secondary: #666666;
    --border-color: #e5e5e5;
    --accent-blue: #2196f3;
    --accent-green: #4caf50;
    --accent-orange: #ff9800;
    --accent-red: #f44336;
}

/* ========== HIDE STREAMLIT DEFAULTS ========== */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    padding-right: 50px !important;
    max-width: 100% !important;
}

/* ========== TOP NAVBAR ========== */
.top-navbar {
    position: fixed;
    top: 0;
    left: 48px;
    right: 40px;
    height: 56px;
    background: var(--bg-primary);
    border-bottom: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
    z-index: 999999;
}

.navbar-spacer { height: 56px; }

/* ========== LEFT ICON NAVIGATION ========== */
.icon-nav-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 48px;
    height: 56px;
    background: var(--bg-primary);
    border-bottom: 1px solid var(--border-color);
    border-right: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 999999;
}

.nav-logo {
    width: 28px;
    height: 28px;
    border: 2px solid var(--text-primary);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
}

.icon-nav {
    position: fixed;
    left: 0;
    top: 56px;
    bottom: 0;
    width: 48px;
    background: var(--bg-primary);
    border-right: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 16px;
    gap: 8px;
    z-index: 999998;
}

.icon-nav-item {
    width: 32px;
    height: 32px;
    border: 2px solid #d0d0d0;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s ease;
}

.icon-nav-item.active {
    border-color: var(--accent-blue);
    background: #e3f2fd;
}

.icon-nav-item:hover {
    border-color: var(--accent-blue);
    transform: scale(1.05);
}

/* ========== RIGHT TILES PANEL ========== */
.tiles-panel {
    position: fixed;
    right: 0;
    top: 56px;
    bottom: 0;
    width: 40px;
    background: var(--bg-secondary);
    border-left: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 8px;
    z-index: 100;
}

.tiles-collapse {
    cursor: pointer;
    font-size: 16px;
    color: var(--text-secondary);
}

.tiles-tab-label {
    writing-mode: vertical-rl;
    font-size: 12px;
    color: var(--text-secondary);
    padding: 8px 0;
}

.tiles-icons {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 20px;
}

.tiles-icon {
    width: 24px;
    height: 24px;
    background: #e0e0e0;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    cursor: pointer;
}

.tiles-icon:hover {
    background: var(--accent-blue);
    color: white;
}

/* ========== SIDEBAR ========== */
[data-testid="stSidebar"] {
    top: 56px !important;
    left: 48px !important;
    height: calc(100vh - 56px) !important;
    background: var(--bg-secondary) !important;
}

.sidebar-card {
    background: var(--bg-primary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 12px;
    margin-bottom: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.sidebar-card:hover {
    border-color: var(--accent-blue);
    box-shadow: 0 2px 8px rgba(33,150,243,0.15);
}

/* ========== METRICS ========== */
[data-testid="stMetric"] {
    background: var(--bg-secondary);
    padding: 12px;
    border-radius: 6px;
    border: 1px solid var(--border-color);
    cursor: pointer;
    transition: all 0.2s ease;
}

[data-testid="stMetric"]:hover {
    border-color: var(--accent-blue);
}

.metric-card {
    background: var(--bg-secondary);
    border: 1px solid var(--border-color);
    padding: 12px;
    margin-bottom: 8px;
    border-radius: 4px;
}

/* ========== DARK MODE ========== */
.dark-mode {
    --bg-primary: #1a1a2e;
    --bg-secondary: #16213e;
    --text-primary: #ffffff;
    --text-secondary: #a0a0a0;
    --border-color: #2a2a4a;
}
</style>
""", unsafe_allow_html=True)
```

## Known Limitations

### SiS Container
- Older Streamlit (~1.35) — `st.column_config` NOT available
- Limited external network access

### SiS Warehouse
- CSP blocks external fonts
- Conda channel package availability

### Raw SPCS
- Requires custom compute pool (NOT `SYSTEM_COMPUTE_POOL_CPU`)
- Must build Docker for `linux/amd64`
- Need `snow spcs image-registry login` for auth

## Additional Resources

### Reference Files

- **`references/example-dashboard.md`** — Complete wireframe-to-production example with 4 environment screenshots
- **`references/component-mapping.md`** — Visual element to Streamlit component mapping
- **`references/troubleshooting.md`** — Common issues and fixes
- **`references/deployment-checklist.md`** — Pre-deployment verification
- **`references/spcs-setup.md`** — SPCS infrastructure guide

### Example Files

- **`examples/streamlit_app.py`** — Cross-environment compatible template
- **`examples/snowflake.yml`** — Project definition template
- **`examples/spcs/`** — Complete SPCS deployment files (Dockerfile, spec.yaml)

### Scripts

- **`scripts/self-assess.py`** — Automated code validation with auto-fix
- **`scripts/visual-validate.py`** — Visual validation loop helper (screenshot analysis)
- **`scripts/validate-compat.py`** — Check code for compatibility issues
- **`scripts/init-project.sh`** — Scaffold new project
- **`scripts/setup-spcs.sql`** — SQL setup for SPCS infrastructure

## Visual Validation Loop (3 Iterations Max - OPTIMIZED)

After generating and running the Streamlit app, perform the visual validation loop using **automated screenshot capture**.

### ⚡ OPTIMIZED RULES (Faster Generation)

1. **Run up to 3 iterations** (reduced from 5)
2. **Early exit allowed** - if score ≥ 90% after iteration 2, skip remaining
3. **Fast mode available** - use `--fast` to skip screenshots entirely
4. **Reduced wait times** - 4s for charts (was 8s)
5. **Use Playwright for automated screenshots** - no manual intervention

### Automated Screenshot Setup (One-Time)

```bash
# Install Playwright and Chromium browser (using uv for speed)
uv pip install playwright
uv run playwright install chromium
```

### Loop Overview (OPTIMIZED)

```
┌─────────────────────────────────────────────────────────────┐
│    AUTOMATED VISUAL VALIDATION LOOP (3 ITERATIONS MAX)      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   # Start app in background                                  │
│   uv run streamlit run streamlit_app.py --server.port 8501 &│
│                                                              │
│   FOR iteration IN [1, 2, 3]:  # Reduced from 5             │
│       IF iteration >= 2 AND score >= 90%:                   │
│           EARLY EXIT → Skip remaining iterations             │
│   │                                                          │
│   │  ┌──────────────────────────────────────────────────┐   │
│   │  │ 1. SCREENSHOT (Playwright - AUTOMATIC):          │   │
│   │  │    python visual-validate.py . $iteration --auto │   │
│   │  │    → Launches headless Chromium                  │   │
│   │  │    → Navigates to localhost:8501                 │   │
│   │  │    → Waits for Streamlit to load                 │   │
│   │  │    → Captures full-page screenshot               │   │
│   │  │    → Saves to .screenshot_iter_N.png             │   │
│   │  │                                                  │   │
│   │  │ 2. ANALYZE (AUTOMATIC):                          │   │
│   │  │    → Parses streamlit_app.py for elements        │   │
│   │  │    → Checks for icon-nav, tiles-panel, etc.      │   │
│   │  │    → Counts charts, metrics, buttons             │   │
│   │  │                                                  │   │
│   │  │ 3. SCORE: Calculate 0-100 based on elements      │   │
│   │  │ 4. LIST: Generate improvement recommendations    │   │
│   │  │ 5. IMPLEMENT: Apply improvements to code         │   │
│   │  │ 6. LINT: ruff check streamlit_app.py --fix && ruff format streamlit_app.py        │   │
│   │  │ 7. (App auto-reloads on file change)            │   │
│   │  └──────────────────────────────────────────────────┘   │
│   │                                                          │
│   │  Output: "Iteration N/5 complete - Score: XX/100"       │
│   │                                                          │
│   └─► CONTINUE TO NEXT ITERATION (no early exit)            │
│                                                              │
│   After iteration 5:                                         │
│   └─► "✅ All 5 visual evaluations complete"                │
│   └─► Screenshots saved: .screenshot_iter_1.png through 5   │
│   └─► Localhost ready, wait for user to request deployment  │
└─────────────────────────────────────────────────────────────┘
```

### Automated Screenshot Command

For EACH iteration, run:

```bash
python ~/.claude/skills/streamlit-snowflake-from-image/scripts/visual-validate.py . [ITERATION] --auto
```

Example for 3 iterations (with early exit):

```bash
# Iteration 1
python ~/.claude/skills/streamlit-snowflake-from-image/scripts/visual-validate.py . 1 --auto
# → Implement improvements from output
# → Run: ruff check streamlit_app.py --fix && ruff format streamlit_app.py

# Iteration 2
python ~/.claude/skills/streamlit-snowflake-from-image/scripts/visual-validate.py . 2 --auto --early-exit 90
# → If score >= 90%, JSON output will have "early_exit": true → STOP HERE
# → Otherwise, implement improvements

# Iteration 3 (only if not early exit)
python ~/.claude/skills/streamlit-snowflake-from-image/scripts/visual-validate.py . 3 --auto
# → Final iteration, then proceed to localhost ready

# ... repeat for iterations 3, 4, 5 ...
```

### Step-by-Step Process

#### Iteration 1: Initial Generation

```bash
# 1. Generate and run the app
uv sync
uv run streamlit run streamlit_app.py --server.port 8501
```

#### Iteration 2-5: Visual Validation

**Step 1: Take Screenshot**

Use browser tools to capture the running app:
```
Navigate to http://localhost:8501
Take screenshot of full page
```

Or request user to provide screenshot if browser tools unavailable.

**Step 2: Visual Comparison Checklist**

Compare screenshot against original wireframe:

| Check | Question | Pass/Fail |
|-------|----------|-----------|
| **Layout Match** | Does the overall layout match the wireframe? | □ |
| **Left Icon Nav** | Are circular icons visible on left edge? | □ |
| **Right Tiles Panel** | Is "Tiles" panel visible on right edge? | □ |
| **Top Navbar** | Logo, search, profile visible? | □ |
| **Sidebar Cards** | Are all insight cards present with content? | □ |
| **Chart Count** | Same number of charts as wireframe? | □ |
| **Chart Titles** | Every chart has a visible title? | □ |
| **Right Panel** | Metrics, buttons, prompt input visible? | □ |
| **Visual Polish** | Colors, spacing, typography look professional? | □ |
| **Interactivity** | Buttons, hover effects working? | □ |

**Step 3: Issue Analysis**

For each failed check, identify specific fix:

```markdown
## Visual Validation - Iteration N

### Issues Found:
1. ❌ Left icon navigation missing
   → FIX: Add .icon-nav HTML block after page_config

2. ❌ Charts have no titles  
   → FIX: Add st.markdown("**Title**") before each chart

3. ❌ Right panel too narrow
   → FIX: Adjust column ratio from [5,1] to [4,1]

### Fixes Applied:
- Added icon-nav HTML block
- Added 6 chart titles
- Changed column ratio
```

**Step 4: Apply Fixes**

Make targeted code changes based on issues found.

**Step 5: Restart and Re-validate**

```bash
# Stop current Streamlit process
# (Ctrl+C or kill process)

# Restart app
uv run streamlit run streamlit_app.py --server.port 8501

# Take new screenshot and repeat validation
```

### Visual Quality Criteria

When analyzing screenshots, check these quality standards:

#### Layout Fidelity (40 points)
| Criterion | Points |
|-----------|--------|
| Overall layout matches wireframe structure | 10 |
| Left icon navigation present and styled | 5 |
| Right tiles panel present and styled | 5 |
| Top navbar complete (logo, search, profile) | 5 |
| Sidebar cards match wireframe count | 5 |
| Main content sections in correct positions | 5 |
| Right panel complete (metrics, buttons, input) | 5 |

#### Visual Attractiveness (30 points)
| Criterion | Points |
|-----------|--------|
| Consistent color scheme | 5 |
| Professional typography (no default gray) | 5 |
| Proper spacing and alignment | 5 |
| Charts are colorful and labeled | 5 |
| Buttons are styled and visible | 5 |
| Hover effects and visual feedback | 5 |

#### Content Quality (30 points)
| Criterion | Points |
|-----------|--------|
| No placeholder text ("Predictive Item") | 10 |
| Realistic data values ($ amounts, %) | 10 |
| Meaningful labels and titles | 10 |

**Scoring Breakdown (100 points total):**

| Category | Points | Checks |
|----------|--------|--------|
| Layout Elements | 40 | Icon nav, tiles panel, navbar, sidebar cards |
| Content | 30 | Charts, metrics, buttons |
| Alignment & Spacing | 20 | Column alignment, consistent spacing, container usage |
| Polish | 10 | Dark mode, chart variety, sidebar richness |

**Score Interpretation:**
- **90-100:** Excellent - Ready for user review
- **70-89:** Good - Minor polish needed
- **50-69:** Fair - Several issues to fix
- **<50:** Poor - Major rework needed

### Alignment Checks (Automatic)

The visual validation script automatically checks for alignment issues:

| Check | Issue Detected | Fix |
|-------|----------------|-----|
| Column widths | Complex/uneven widths like `[1, 2, 3, 1]` | Simplify to even widths |
| Spacing units | Mixed px, rem, em, % | Standardize on one unit |
| Flexbox alignment | Missing `align-items`/`justify-content` | Add CSS alignment properties |
| Fixed widths | Multiple hardcoded pixel widths | Use responsive units |
| Column gaps | No explicit gap defined | Add `gap` to CSS |
| Metric count | Odd numbers that don't grid evenly | Use 2, 3, or 4 metrics per row |
| Chart heights | Inconsistent heights | Standardize `.properties(height=X)` |
| Containers | No grouping of elements | Use `st.container()` or `<div>` |

**Example alignment issue output:**
```
🔧 Alignment: Columns without explicit gap - spacing may be inconsistent
🔧 Alignment: Mixed spacing units (px, rem) - may cause alignment issues
🔧 Alignment: 5 metrics may not align evenly in grid - consider 2, 3, or 4 per row
```

### Theme Toggle Verification (Automatic)

The visual validation script checks for proper dark/light mode implementation:

| Check | What It Verifies | Fix if Missing |
|-------|------------------|----------------|
| **Session state init** | `if "dark_mode" not in st.session_state` | Add before toggle to prevent double-click |
| **on_change callback** | `on_change=toggle_theme` | Add callback for immediate effect |
| **CSS variables** | `--bg-primary`, `--text-primary`, etc. | Use CSS variables for consistent theming |
| **Dark theme CSS** | Dark colors defined (#121212, #1e1e1e) | Add dark theme color palette |
| **Light theme CSS** | Light colors defined (#ffffff, #f7f7f8) | Add light theme color palette |
| **Theme applied early** | CSS in first 100 lines of script | Move theme CSS to top of script |

**Common issue: Toggle requires double-click**
```
🎨 Theme: Missing session state init for dark_mode - toggle may require double-click
🎨 Theme: No on_change callback for theme toggle - may need double-click
```

**Proper implementation pattern:**
```python
# 1. Initialize session state FIRST
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# 2. Apply theme CSS immediately (at top)
apply_theme()  # Function that injects CSS based on session state

# 3. Toggle with on_change callback
st.toggle("🌙", value=st.session_state.dark_mode, on_change=toggle_theme)
```

### Example Validation Output

```markdown
## Visual Validation - Iteration 2

**Screenshot Analysis:**

✅ Layout Match: Overall structure matches wireframe
✅ Left Icon Nav: 5 circular icons visible, first one active
✅ Right Tiles Panel: "Tiles" label visible with collapse arrow
✅ Top Navbar: Logo "Z", company name, search, profile all present
✅ Sidebar Cards: 3 insight cards with unique content
⚠️ Chart Titles: 4/6 charts have titles (missing 2)
✅ Right Panel: Metrics, suggestions, prompt input all visible
⚠️ Visual Polish: Some buttons need better styling
✅ Interactivity: Buttons respond, charts have tooltips

**Score: 85/100 (Good)**

**Fixes for Iteration 3:**
1. Add titles to "Traffic Distribution" and "Conversion by Channel" charts
2. Style action buttons with full-width and primary color

**Status:** Continue to Iteration 3
```

### Loop Completion Conditions

**The loop ends ONLY after completing ALL 5 iterations.**

| Iteration | Focus |
|-----------|-------|
| 1/5 | Major layout issues, missing elements |
| 2/5 | Content quality, placeholder text |
| 3/5 | Chart styling, colors, labels |
| 4/5 | Spacing, alignment, visual polish |
| 5/5 | Final touches, micro-interactions |

**Even if score is 100, continue to next iteration and find minor improvements:**
- Better spacing
- Improved hover effects
- Enhanced tooltips
- Color refinements
- Typography adjustments

**After iteration 5/5 is complete:**
1. Output: "✅ All 5 visual evaluations complete"
2. Output: "🌐 Localhost ready at http://localhost:8501"
3. Output: "📋 Say 'deploy to snowflake' when ready"
4. **STOP and WAIT** for user to review and request deployment

### Browser Tool Integration

If MCP browser tools are available, use them for automated screenshots:

```
# Using cursor-browser-extension or cursor-ide-browser MCP tools:

1. Navigate to http://localhost:8501
2. Wait for page to fully load (use wait/sleep if needed)
3. Take full-page screenshot
4. Analyze screenshot content against original wireframe
5. Identify issues and generate fixes
```

**Automated Screenshot Analysis Prompt:**
```
Look at this screenshot of the running Streamlit app.
Compare it against the original wireframe and:

1. Check all layout elements are present (icon-nav, tiles-panel, navbar)
2. Verify content quality (no placeholders, real data)
3. Assess visual polish (colors, spacing, typography)
4. Score from 0-100 based on Visual Quality Criteria
5. List specific issues and fixes needed
```

If browser tools are unavailable, prompt user:
```
Please provide a screenshot of the running Streamlit app at localhost:8501
so I can analyze it against the original wireframe.

After receiving the screenshot, I will:
1. Compare layout against wireframe
2. Check for missing elements
3. Score visual quality (0-100)
4. Identify specific fixes needed
```

### Visual Validation Script

A helper script is available for structured validation:

```bash
# Interactive validation (asks questions for each check)
python ~/.claude/skills/streamlit-snowflake-from-image/scripts/visual-validate.py . 1

# For iteration 2 after fixes:
python ~/.claude/skills/streamlit-snowflake-from-image/scripts/visual-validate.py . 2
```

The script:
- Provides a structured checklist for all visual criteria
- Calculates a score (0-100)
- Tracks issues and fixes across iterations
- Saves results to `.validation_iter_N.json`
- Outputs JSON for programmatic processing

## Self-Assessment Loop (Automated Validation + Auto-Fix)

After generating the Streamlit app, run the self-assessment script to validate and auto-fix issues:

### Step 1: Run Self-Assessment with Auto-Fix

```bash
# Check only (report issues)
python ~/.claude/skills/streamlit-snowflake-from-image/scripts/self-assess.py .

# Check AND auto-fix linting/formatting issues
python ~/.claude/skills/streamlit-snowflake-from-image/scripts/self-assess.py . --fix
```

### Step 2: Parse JSON Output

The script outputs JSON with structured results:

```json
{
  "passed": true,
  "score": 18,
  "max_score": 20,
  "score_percent": 90,
  "critical_issues": [],
  "warnings": ["Charts may use default colors"],
  "suggestions": ["Build with: docker build --platform linux/amd64"],
  "auto_fixed": ["ruff: Fixed 3 issues", "ruff format: Reformatted code"]
}
```

### Step 3: Decision Logic

```
IF passed == false:
    → Fix all critical_issues
    → Re-run with --fix
    → Repeat until passed == true

IF passed == true AND warnings exist:
    → Optionally fix warnings
    → Keep localhost running, wait for user

IF passed == true AND no warnings:
    → Localhost ready at http://localhost:8501
    → Wait for user to say "deploy to snowflake"
```

### Step 4: Automated Fix Loop

After generating code, Claude should:

```bash
# 1. Run self-assessment with auto-fix
python self-assess.py . --fix

# 2. If critical_issues remain:
#    - Read specific issue
#    - Fix manually in code
#    - Re-run assessment

# 3. Common critical issues:
#    - "st.column_config found" → Replace with pandas formatting
#    - "Syntax error at line X" → Fix the syntax
#    - "Missing import: altair" → Add import altair as alt
#    - "MUST use 'snowflake' channel" → Change to snowflake
```

### Self-Assessment Checks

| Check | Critical | Auto-Fix | What It Catches |
|-------|----------|----------|-----------------|
| Required files exist | ✅ | ❌ | Missing config files |
| No st.column_config | ✅ | ❌ | SiS Container compatibility |
| Python syntax valid | ✅ | ❌ | Code won't run |
| Snowflake channel | ✅ | ❌ | Wrong Conda channel |
| **Content quality** | ⚠️ | ❌ | **Placeholder text, missing real content** |
| **Chart titles/labels** | ⚠️ | ❌ | **Missing titles, axis labels, tooltips** |
| **Layout elements** | ⚠️ | ❌ | **Missing icon-nav, tiles-panel, navbar** |
| **Interactivity** | ⚠️ | ❌ | **Few buttons, no session_state, non-interactive charts** |
| **Chart variety** | ⚠️ | ❌ | **Only one chart type - add bar, line, area, pie** |
| **Dark/Light mode** | ⚠️ | ❌ | **Missing theme toggle** |
| Altair explicit colors | ⚠️ | ❌ | Inconsistent chart colors |
| No simple charts | ⚠️ | ❌ | st.bar_chart usage |
| Public SPCS endpoint | ⚠️ | ❌ | SPCS not accessible |
| Required imports | ⚠️ | ❌ | Missing dependencies |
| App size >= 50 lines | ⚠️ | ❌ | Incomplete generation |
| Ruff linting | ⚠️ | ✅ | Code quality issues |
| Ruff formatting | ⚠️ | ✅ | Style inconsistencies |
| Type checking (ty) | ⚠️ | ❌ | Type errors |

### Content Quality Checks (NEW)

The self-assessment now specifically catches placeholder issues:

| Issue Detected | Problem | Fix |
|----------------|---------|-----|
| "Predictive Item" found | Generic placeholder text | Replace with specific: "Revenue Forecast", "Churn Risk" |
| Too many ─── lines | Visual placeholders, not content | Replace with real text content |
| Charts without titles | Unlabeled charts | Add `st.markdown("**Chart Title**")` before each chart |
| No st.metric() found | Missing KPI metrics | Add metric cards with real values |
| No $ or % values | Missing realistic data | Add formatted values like "$45,231" or "3.24%" |
| Few action buttons | Limited interactivity | Add buttons: "View Details", "Export", etc. |
| Missing right panel | Incomplete layout | Add: metrics, AI suggestions, prompt input |
| Missing axis labels | Charts unclear | Add `title=` to `alt.X()` and `alt.Y()` |
| No tooltips | Can't explore data | Add `tooltip=[...]` to chart encoding |

### Example Output (with --fix)

```
============================================================
SELF-ASSESSMENT: 18/20 (90%)
============================================================

🔧 AUTO-FIXED:
   • ruff: Fixed 5 issues
   • ruff format: Reformatted code

⚠️  WARNINGS:
   • Explicit chart colors: Charts may use default colors

💡 SUGGESTIONS:
   • Build with: docker build --platform linux/amd64
   • Install ty: uv tool install ty

✅ RESULT: PASSED - Localhost ready, awaiting user review
```

### Required Tools

```bash
# Install modern Python tooling
uv tool install ruff   # Linting + formatting
uv tool install ty     # Type checking (optional)
```

## Validation Checklist (Manual)

If not using automated self-assessment:

### Technical Compatibility
- [ ] No `st.column_config` usage
- [ ] All charts use explicit Altair with hardcoded colors
- [ ] Number/percentage formatting via pandas
- [ ] Streamlit 1.51+ in all config files
- [ ] `environment.yml` uses `snowflake` channel
- [ ] SPCS Dockerfile uses `--platform linux/amd64`
- [ ] All 4 config files present and version-consistent

### Visual Richness & Layout
- [ ] **Left Icon Navigation** - Vertical bar with 4-5 circular icons
- [ ] **Top Navbar** - Logo, company name, search, profile
- [ ] **Right Tiles Panel** - Collapsible with `<` arrow and icons
- [ ] **Dark/Light Mode Toggle** - Theme switcher in sidebar
- [ ] **KPI Metrics Row** - 4 metrics with labels, values, deltas
- [ ] **Tabbed Content** - At least 2-3 tabs (Overview, Breakdown, Data)
- [ ] **Chart Variety** - Bar, line, area, pie/donut (at least 3 types)

### Interactivity
- [ ] **Clickable Metrics** - Buttons with `st.button()` on KPIs
- [ ] **Interactive Charts** - `.interactive()` on Altair charts with tooltips
- [ ] **Collapsible Filters** - `st.expander()` for filter controls
- [ ] **Session State** - Track selected items with `st.session_state`
- [ ] **Action Buttons** - "View Details", "Export", etc. with visual feedback
- [ ] **Activity Feed** - Clickable list items with timestamps

### Content Quality
- [ ] **No placeholder text** - "Predictive Item" replaced with specific names
- [ ] **Realistic values** - "$45,231", "1,247 users", "3.24%"
- [ ] **Chart titles** - Every chart has `st.markdown("**Title**")` above it
- [ ] **Axis labels** - Every chart has `title=` in x/y encoding
- [ ] **Tooltips** - Every chart has `tooltip=[...]`
- [ ] **Legends** - Multi-series charts have color legends

## Reference Implementation

The skill references a proven implementation at `examples/streamlit_app.py` which includes:

- **855 lines** of production-ready Streamlit code
- All mandatory layout elements (icon-nav, tiles-panel, navbar)
- 4 interactive insight cards with buttons
- 6 different chart types (bar, line, area, pie, stacked, multi-line)
- Tabbed content with Overview, Breakdown, Data Table views
- Right panel with metrics, AI suggestions, prompt input
- Fully clickable with session state tracking
- Works across all 4 deployment environments

When generating new dashboards, reference this file for:
- CSS structure and class naming
- HTML patterns for custom elements
- Altair chart patterns with explicit colors
- Interactivity patterns with buttons and session state
