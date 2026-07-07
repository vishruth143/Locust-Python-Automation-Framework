# 🦗 Locust-Python-Automation-Framework

<div align="center">

Performance test automation framework with **Locust** and **Python**.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Locust](https://img.shields.io/badge/Locust-2.x-orange)
![Docker](https://img.shields.io/badge/Docker-ready-2496ED)

</div>

---

## 📚 Table of Contents

1. [🎓 How This Framework Works — A Beginner's Guide](#-how-this-framework-works--a-beginners-guide)
2. [✅ Features](#-features)
3. [🛠 Prerequisites](#-prerequisites)
4. [⚡ Quick Start](#-quick-start)
5. [🚀 Project Structure](#-project-structure)
6. [🚀 Running Load Tests](#-running-load-tests)
7. [📖 Command Reference](#-command-reference)
8. [📊 Reports](#-reports)
9. [🐳 Docker](#-docker)
10. [🔧 Troubleshooting](#-troubleshooting)

---

## 🎓 How This Framework Works — A Beginner's Guide

> **New to Locust or this project?** Read this section first. It explains every layer of the framework in plain English, with examples from the actual code.

---

### 🧠 The Big Picture

This framework simulates **virtual users** hitting real web APIs. You tell Locust:
- **Who** the users are (user classes)
- **What** they do (tasks / scenarios)
- **How many** users and **how fast** to spawn them

Locust then runs all those users in parallel and gives you live metrics: requests/sec, response times, failure rates.

```
You run: locust -f locustfile.py
              │
              ▼
   ┌─────────────────────┐
   │    locustfile.py    │  ← Entry point: registers users & Prometheus metrics
   └────────┬────────────┘
            │ creates virtual users of type:
            ▼
   ┌─────────────────────────────────────────┐
   │           users/  (User Classes)        │  ← Defines who the user is
   │  BlazeDemoUserTaskSetUserClass          │
   │  JsonPlaceholderUserTaskSetUserClass    │
   └────────┬────────────────────────────────┘
            │ each user executes tasks from:
            ▼
   ┌─────────────────────────────────────────┐
   │        users/  (TaskSets)               │  ← Defines what actions the user performs
   │  BlazeDemoUserTaskSet                   │
   │  JsonPlaceholderUserTaskset             │
   └────────┬────────────────────────────────┘
            │ each task calls a function in:
            ▼
   ┌─────────────────────────────────────────┐
   │         scenarios/  (Flows)             │  ← The actual HTTP requests
   │  blaze_demo_flows.py                    │
   │  json_placeholder_flows.py              │
   └────────┬────────────────────────────────┘
            │ uses shared helpers from:
            ▼
   ┌─────────────────────────────────────────┐
   │         utilities/                      │  ← Reusable building blocks
   │  helpers.py   → builds HTTP headers     │
   │  common.py    → logs every response     │
   │  logger.py    → sets up the logger      │
   └────────┬────────────────────────────────┘
            │ all URLs and constants come from:
            ▼
   ┌─────────────────────────────────────────┐
   │         config/config.py                │  ← Central configuration
   │  BLAZEDEMO_BASE_URL                     │
   │  JSON_PLACEHOLDER_BASE_URL              │
   │  DEFAULT_THINK_TIME                     │
   └─────────────────────────────────────────┘
```

---

### 📦 Layer 1 — `config/config.py` (The Settings File)

This is the **single source of truth** for all configurable values.

```python
DEFAULT_THINK_TIME = 2                                   # seconds a user "thinks" between actions
BLAZEDEMO_BASE_URL = "https://www.blazedemo.com"         # target URL for BlazeDemo tests
JSON_PLACEHOLDER_BASE_URL = "https://jsonplaceholder.typicode.com"  # target URL for API tests
```

> **Why this matters:** If the target URL ever changes, you update it in one place here — not scattered across every test file.

---

### 🔧 Layer 2 — `utilities/` (Shared Building Blocks)

These three files are helper modules imported by the scenarios. You don't run them directly.

**`utilities/helpers.py`** — Builds the HTTP headers used in every request:
```python
def build_headers():
    return {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
```

**`utilities/logger.py`** — Sets up a logger that writes to both the console and a `logs/locust.log` file:
```python
logger = setup_logger()    # called once at the top of each scenario file
logger.info("message")     # INFO and above → console + file
logger.debug("message")    # DEBUG → file only
```

**`utilities/common.py`** — Logs every HTTP response in a consistent format:
```python
log_response("GET", url, response)
# Prints: GET https://... | Status: 200 | Request: N/A | Response: [first 200 chars]...
# If status >= 400, logs as ERROR instead of INFO
```

---

### 🌐 Layer 3 — `scenarios/` (The Actual HTTP Requests)

This is where the **real web traffic** is defined. Each function sends one HTTP request using `user.client` (Locust's built-in HTTP session).

**`scenarios/blaze_demo_flows.py`** — Simulates a flight booking journey:

| Function | HTTP Method | Endpoint | What it does |
|---|---|---|---|
| `search_flights(user)` | GET | `/` | Loads the BlazeDemo homepage |
| `select_flight(user)` | POST | `/reserve.php` | Picks a random departure/arrival city using `Faker` |
| `book_flight(user)` | POST | `/confirmation.php` | Submits fake booking details (name, address, card) |

**`scenarios/json_placeholder_flows.py`** — Simulates REST API usage:

| Function | HTTP Method | Endpoint | What it does |
|---|---|---|---|
| `get_posts(user)` | GET | `/posts` | Fetches all posts |
| `get_post_by_id(user)` | GET | `/posts/1` | Fetches a single post by ID |
| `create_posts(user)` | POST | `/posts` | Creates a new post with a static payload |

> **`Faker`** is a library that generates realistic random data (names, addresses, cities, card numbers) so each simulated user sends unique-looking requests.

---

### 👤 Layer 4 — `users/` (The Virtual Users)

Each file in `users/` defines **who the virtual user is** and **what list of tasks they run**. This layer has two concepts:

#### 1. TaskSet — Random order execution
```python
# users/blaze_demo_user_taskset.py

class BlazeDemoUserTaskSet(TaskSet):        # ← defines the actions
    @task
    def search_flight(self):               # all @task methods have equal weight
        blaze_demo_flows.search_flights(self)

    @task
    def select_flight(self):
        blaze_demo_flows.select_flight(self)

    @task
    def book_flight(self):
        blaze_demo_flows.book_flight(self)

class BlazeDemoUserTaskSetUserClass(HttpUser):   # ← the actual Locust user
    host = BLAZEDEMO_BASE_URL              # where to send requests
    wait_time = constant(DEFAULT_THINK_TIME)  # 2 seconds between each task
    tasks = [BlazeDemoUserTaskSet]         # which TaskSet to run
```

> With `TaskSet`, Locust picks a random `@task` each time — tasks run in any order.

#### 2. SequentialTaskSet — Fixed order execution
```python
# users/blaze_demo_user_sequential_taskset.py

class BlazeDemoUserSequentialTaskSet(SequentialTaskSet):
    @task
    def search_flight(self): ...    # Step 1 — always runs first

    @task
    def select_flight(self): ...    # Step 2 — always runs second

    @task
    def book_flight(self): ...      # Step 3 — always runs last
```

> With `SequentialTaskSet`, tasks run **in the exact order they are defined** — useful for multi-step flows like search → select → book.

#### 3. Task weights (JSONPlaceholder example)
```python
class JsonPlaceholderUserTaskset(TaskSet):
    @task(2)                        # runs ~33% of the time  (weight 2 out of 6 total)
    def get_posts(self): ...

    @task(3)                        # runs ~50% of the time  (weight 3 out of 6 total)
    def get_post_by_id(self): ...

    @task(1)                        # runs ~17% of the time  (weight 1 out of 6 total)
    def create_posts(self): ...
```

> The number inside `@task(n)` is the **relative weight**. Higher numbers = called more often.

---

### 🚀 Layer 5 — `locustfile.py` (The Entry Point)

This is the file Locust reads when you run `locust -f locustfile.py`. It does two things:

#### 1. Registers the user classes
```python
user_classes = [BlazeDemoUserTaskSetUserClass, JsonPlaceholderUserTaskSetUserClass]
```
Locust sees both user classes and spawns them during the test run.

#### 2. Starts Prometheus metrics tracking
```python
@events.init.add_listener
def on_locust_init(environment, **kwargs):
    start_http_server(8000)          # exposes metrics at http://localhost:8000

@events.request.add_listener
def track_request(request_type, name, response_time, exception, **kwargs):
    if exception is None:
        REQUEST_COUNT.inc()          # count successes
    else:
        REQUEST_FAILURE_COUNT.inc()  # count failures
    REQUEST_LATENCY.observe(response_time / 1000.0)  # record latency in seconds
```

> Prometheus metrics allow external monitoring tools (like Grafana) to scrape and visualise real-time test results beyond the built-in Locust UI.

---

### 🔁 End-to-End Request Flow (Step by Step)

Here is exactly what happens when Locust sends one request, traced from start to finish:

```
1.  You run:   locust -f locustfile.py -u 5 -r 1
                                │
2.  Locust reads locustfile.py and finds:
    user_classes = [BlazeDemoUserTaskSetUserClass, JsonPlaceholderUserTaskSetUserClass]
                                │
3.  Locust spawns virtual users (e.g., 5 total, 1 per second)
                                │
4.  Each BlazeDemoUserTaskSetUserClass user:
    - connects to host = "https://www.blazedemo.com"
    - picks a random @task from BlazeDemoUserTaskSet
    - e.g., picks book_flight()
                                │
5.  book_flight() calls:
    blaze_demo_flows.book_flight(self)
                                │
6.  book_flight() in scenarios/blaze_demo_flows.py:
    - builds fake payload using Faker (name, address, card number)
    - calls build_headers() → {"Content-Type": "application/json", ...}
    - sends: user.client.POST("https://www.blazedemo.com/confirmation.php", json=payload)
                                │
7.  Response comes back
    - log_response() logs: POST https://... | Status: 200 | Request: {...} | Response: ...
    - Locust records: response time, success/failure
                                │
8.  locustfile.py event listener fires:
    - REQUEST_COUNT.inc()  (or REQUEST_FAILURE_COUNT.inc() if exception)
    - REQUEST_LATENCY.observe(response_time / 1000.0)
                                │
9.  User waits DEFAULT_THINK_TIME (2 seconds), then picks the next random task
```

---

### 🗂 Quick Reference: Which File to Edit for What

| I want to… | Edit this file |
|---|---|
| Change the target URL | `config/config.py` |
| Change wait time between tasks | `config/config.py` → `DEFAULT_THINK_TIME` |
| Add a new HTTP request | `scenarios/blaze_demo_flows.py` or `scenarios/json_placeholder_flows.py` |
| Add a new task for a user | `users/blaze_demo_user_taskset.py` |
| Change task execution order | Switch `TaskSet` → `SequentialTaskSet` in `users/` |
| Change how often a task runs | Update the `@task(weight)` number |
| Add a new user type | Create a new file in `users/` |
| Modify log format | `utilities/logger.py` |
| Modify response logging | `utilities/common.py` |
| Modify HTTP headers | `utilities/helpers.py` |
| Add Prometheus metrics | `locustfile.py` |

---

## ✅ Features

| Feature | Status | Details |
|---|---|---|
| Modular architecture | ✅ | Separate modules for `scenarios`, `users`, `tasks`, and shared utilities |
| Config-driven execution | ✅ | Environment values are centralized in `config/config.py` |
| Headless execution | ✅ | Suitable for CI/CD and scheduled performance runs |
| HTML reporting | ✅ | Generates a run summary with `--html` |
| Distributed mode | ✅ | Supports Locust master/worker load generation |

---

## 🛠 Prerequisites

| Tool | Purpose |
|---|---|
| Python | Runtime for Locust scripts |
| pip | Dependency installation |
| Locust | Load testing engine |
| Docker (optional) | Containerized execution |

---

## ⚡ Quick Start

### 1) Install dependencies

```bash
pip install -r requirements.txt
```

### 2) Verify Locust installation

```bash
locust --version
```

### 3) Start Locust in UI mode

```bash
locust -f locustfile.py
```

### 4) Run in headless mode and generate HTML report

```bash
locust -f locustfile.py --headless -u 3 -r 3 -t 1m --html reports/report.html
```

---

## 🚀 Project Structure

```text
Locust-Python-Automation-Framework/
├── .github/                                               # GitHub Actions workflows and config
│   └── workflows/                                         # CI/CD workflow definitions
│       └── locust-ci.yml                                  # Locust CI pipeline
│
├── config/                                                # Configuration files
│   └── config.py                                          # Main config values
│
├── scenarios/                                             # Reusable load test flows
│   ├── blaze_demo_flows.py                                # Blaze demo flows
│   └── json_placeholder_flows.py                          # JSONPlaceholder API flows
│
├── tasks/                                                 # User task definitions
│
├── users/                                                 # Locust user definitions
│   ├── blaze_demo_user_sequential_taskset.py              # Sequential Blaze taskset user
│   ├── blaze_demo_user_taskset.py                         # Standard Blaze taskset user
│   └── json_placeholder_user_taskset.py                   # JSONPlaceholder taskset user
│
├── utilities/                                             # Shared helper modules
│   ├── common.py                                          # Common utility functions
│   ├── helpers.py                                         # Generic helper functions
│   └── logger.py                                          # Logging utilities
│
├── utils/                                                 # Additional utility modules
│
├── .gitignore                                             # Git ignored files and directories
├── Dockerfile                                             # Container configuration
├── locustfile.py                                          # Main Locust entry point
├── README.md                                              # Project documentation
└── requirements.txt                                       # Python dependencies
```

---

## 🚀 Running Load Tests

### UI mode

```bash
locust -f locustfile.py
```

### Headless mode

```bash
locust -f locustfile.py --headless -u 3 -r 3 -t 1m
```

### Distributed mode

Run the following in separate terminals.

**Terminal 1 (Master)**

```bash
locust -f locustfile.py --master --expect-workers 2 --headless -u 3 -r 3 -t 1m --html reports/report.html
```

**Terminal 2 (Worker 1)**

```bash
locust -f locustfile.py --worker --master-host 127.0.0.1
```

**Terminal 3 (Worker 2)**

```bash
locust -f locustfile.py --worker --master-host 127.0.0.1
```

---

## 📖 Command Reference

| Argument | Description |
|---|---|
| `locust` | Starts Locust. |
| `-f locustfile.py` | Uses `locustfile.py` as the test entry file. |
| `--headless` | Runs without the web UI. |
| `-u 3` | Total virtual users to simulate. |
| `-r 3` | User spawn rate per second. |
| `-t 1m` | Test duration (1 minute). |
| `--master` | Starts Locust in master mode. |
| `--worker` | Starts Locust as a worker node. |
| `--expect-workers 2` | Waits for 2 workers before starting. |
| `--html reports/report.html` | Exports HTML report for the run. |

---

## 📊 Reports

- Use `--html reports/report.html` to generate an HTML report after headless execution.
- Use UI mode (`locust -f locustfile.py`) for real-time metrics and charts during test runs.

---

## 🐳 Docker

Use the included `Dockerfile` for containerized test execution.

```bash
docker build -t locust-framework .
docker run --rm locust-framework
```

> **Note:** Docker run arguments may vary depending on how `locustfile.py` and runtime options are configured in your image.

---

## 🔧 Troubleshooting

| Issue | Possible Cause | Suggested Fix |
|---|---|---|
| `locust` command not found | Locust not installed in current environment | Run `pip install -r requirements.txt` and verify with `locust --version` |
| Report file not generated | `reports` path missing or command not completed | Ensure the command includes `--html reports/report.html` and test run finishes |
| Workers not connecting | Master host/port mismatch | Verify `--master-host 127.0.0.1` and active master process |
| Port already in use | Another process uses Locust default port | Stop existing process or run Locust on a different port |

