# Resume Analysis and Job Recommendation System

[![Testing Suite](https://img.shields.io/badge/Automated%20Tests-30%20Passed%20(100%25)-success?style=for-the-badge&logo=pytest)](TEST_REPORT.md)
[![Live ML API](https://img.shields.io/badge/FastAPI%20ML%20API-Live%20on%20Render-blue?style=for-the-badge&logo=fastapi)](https://careerlens-6woq.onrender.com)
[![Live Backend API](https://img.shields.io/badge/Flask%20Backend%20API-Live%20on%20Render-emerald?style=for-the-badge&logo=flask)](https://resume-analyser-kvs7.onrender.com)
[![Frontend UI](https://img.shields.io/badge/React%2018%20UI-Live%20on%20Render-cyan?style=for-the-badge&logo=react)](DEPLOYMENT_GUIDE.md)

An end-to-end AI-powered academic mini-project designed to evaluate candidate resumes, predict career families and IT job roles, extract technical skills, conduct skill-gap analysis, provide curated learning resources, and evaluate candidate interview preparedness.

---

## 👥 Project Team & Work Distribution

| Member | Academic Role | Technology Stack | Key Responsibilities |
| :--- | :--- | :--- | :--- |
| **Rakshini** | **Lead: QA, Testing & Cloud Deployment** | Python Unittest, Pytest, Render, Docker | Designed 30-case test suite, achieved 100% test pass rate, deployed microservices to cloud. |
| **Sushmita Naik** | AI & Machine Learning Lead | FastAPI, Scikit-Learn, PyPDF, AMEO Dataset | Trained career family & role prediction models (`.pkl`), ML classification pipeline. |
| **Rakshitha H.M** | Backend & Database Lead | Flask, SQLite, Werkzeug, PyPDF, python-docx | User auth (Register/Login), database schemas, interview question & evaluation engine. |
| **H.R. Shobha** | Frontend & UI/UX Lead | React 18, Vite, Tailwind CSS, Recharts | Interactive candidate dashboard, drag-and-drop resume ingestion, visual reports. |

---

## 🌐 Live Production Cloud Deployments

The application is deployed under a production **Microservices Architecture**:

* 🧠 **AI / Machine Learning Prediction Service:** [https://careerlens-6woq.onrender.com](https://careerlens-6woq.onrender.com)
* 🗄️ **User Management & Database API:** [https://resume-analyser-kvs7.onrender.com](https://resume-analyser-kvs7.onrender.com)
* 💻 **Interactive React Frontend:** Render Static Site Production Build

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    Client(["Candidate / User Browser"])

    subgraph PresentationTier["Frontend Tier (React + Vite)"]
        UI["React 18 Dashboard\n- Resume Upload\n- Competency Visualizer\n- Mock Interview Portal\n- PDF Readiness Report"]
    end

    subgraph ApplicationTier["Application & Auth Tier (Flask REST API)"]
        FlaskAPI["Flask Server (Port: 5000)\n- Authentication (Register/Login)\n- Resume Text Extraction\n- Interview Evaluation Engine\n- Learning Resource Generator"]
        SQLiteDB[("SQLite Database\n(database.db)")]
    end

    subgraph AITier["Machine Learning Tier (FastAPI Service)"]
        FastAPI_ML["FastAPI ML Service (Port: 8000)\n- Career Family Classifier\n- IT Role Matcher\n- AMEO Benchmark Scoring"]
    end

    Client --> UI
    UI -->|JSON / Multipart| FlaskAPI
    UI -->|JSON / Multipart| FastAPI_ML
    FlaskAPI <--> SQLiteDB
```

---

## 🧪 Software Testing & Verification

A comprehensive 30-case automated test suite was developed and executed using Python's testing framework:

```text
=======================================================================
               CAREERLENS AUTOMATED TEST RESULTS
=======================================================================
Total Tests Planned:     30
Total Tests Executed:    30
Total Tests Passed:      30 (100% Pass Rate)
Failures / Errors:       0
Execution Time:          5.26 seconds
Status:                  READY FOR PRODUCTION DEPLOYMENT
=======================================================================
```

### Complete Test Case Matrix
Full details with test inputs, preconditions, expected outcomes, and actual results can be reviewed in [TEST_REPORT.md](TEST_REPORT.md).

---

## ⚡ Quick Start & Local Execution

### 1. Run Automated Test Suite
Double-click `RUN_TESTS.bat` or run:
```bash
cd Resume_analyser
python -m unittest discover -s tests -p "test_*.py" -v
```

### 2. Run Local Backend Server
Double-click `START_LOCAL_DEMO.bat` or run:
```bash
cd Resume_analyser
python app.py
```
Backend will be available on `http://127.0.0.1:5000`.

### 3. Run with Docker Compose
```bash
docker compose up --build
```

---

## 📄 Documentation Links
* 📑 **Software Test Report:** [TEST_REPORT.md](TEST_REPORT.md)
* 🚀 **Deployment Operations Manual:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

---
*Developed for College Mini Project 2026.*
