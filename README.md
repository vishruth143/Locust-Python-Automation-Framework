# 🧪 Appium-Python-Automation-Framework

A robust and scalable test automation framework using **Locust**, **Pytest**, and **Python**. Supports performance testing with environment-driven configuration and Docker integration.

---
## 📁 Project Structure

Locust-Python-Automation-Framework

├── locustfile.py

├── config/

│ └── config.py

├── tasks/

│ └── user_behaviour.py

├── utils/

│ └── helpers.py

└── requirements.txt

### Explanation:
**locustfile.py**

The main entry point for Locust tests. It defines the user classes and the load test scenarios.

**config/**

Contains configuration files for the framework.


**config.py:** 

Holds environment-specific settings like URLs, user credentials, and other constants.

**tasks/**

Contains user behavior definitions and task sets that simulate real user actions.

**user_behaviour.py:** 

Defines the different tasks and flows that virtual users will perform during the test.

**utils/**

Utility helper functions and reusable code modules to support test execution.

**helpers.py:** 

Contains helper functions used across tasks and tests.

**requirements.txt**

Lists all Python dependencies required to run the framework and tests.

---

## 🔹 To know the installer locust version
```bash
  locust --version
```
---
## 🔹 To run locust script
```bash
  locust -f  .\myfirsttest.py
```
---
## 🔹 To generate html report
```bash
  locust -f locustfile.py --headless -u 10 -r 2 -t 1m --html=reports/report.html
```
---
| **Part**                     | **Meaning**                                                                                                                   |
|------------------------------|-------------------------------------------------------------------------------------------------------------------------------|
| `locust`                     | This is the command to start Locust.                                                                                          |
| `-f locustfile.py`           | Specifies the file that contains your Locust user class and tasks (in this case, `locustfile.py`).                            |
| `--headless`                 | Runs the test without the web UI (ideal for automation, CI/CD, or terminal-only usage).                                       |
| `-u 2`                       | Sets the number of total users (virtual users) to simulate = **10 users**.                                                    |
| `-r 2`                       | Sets the spawn rate = how many users to start **per second**. Here, it starts 2 users every second until it reaches 10 users. |
| `-t 1m`                      | Duration of the test = **1 minute**. After 1 minute, the test stops automatically.                                            |
| `--html=reports/report.html` | Generates an HTML report after the test finishes and saves it as `reports/report.html`.                                       |
