# Ted-AI

> Local, privacy-focused penetration testing copilot
---

## Overview

Ted-AI is a command-line penetration testing assistant designed to operate entirely on your local machine.

The long-term goal is to create an objective-driven security copilot capable of:

* Maintaining engagement state
* Tracking evidence and findings
* Retrieving relevant knowledge
* Prioritizing high-probability attack paths
* Assisting with Web Application Testing
* Assisting with API Security Testing
* Assisting with Mobile Application Testing
* Reducing wasted effort and rabbit holes

The current version implements the foundation required for those capabilities:

* Local LLM integration through Ollama
* Engagement tracking through SQLite
* Retrieval-Augmented Generation (RAG) through ChromaDB
* Local knowledge base
* Interactive CLI

No cloud APIs are required.

---

# Features

## Local LLM

Uses Ollama to run language models entirely on your machine.

Current model:

```text
qwen3:8b
```

Benefits:

* No API costs
* No external data transmission
* Full control over model selection

---

## Engagement Tracking

Stores active penetration testing engagements.

Current fields:

* Target
* Objective
* Status

Example:

```text
Target:
paypal.com

Objective:
Identify authorization vulnerabilities
```

---

## Retrieval-Augmented Generation (RAG)

Ted-AI can search local notes and methodologies before generating responses.

Knowledge is stored in:

```text
knowledge/
```

and indexed using ChromaDB.

Example knowledge sources:

* API testing notes
* JWT methodologies
* GraphQL testing workflows
* Mobile testing notes
* Internal playbooks

---

## Command Line Interface

Simple interactive terminal interface.

Example:

```text
Ted-ai> ask What should I investigate next?
```

---

# Architecture

```text
User
 │
 ▼
app.py
 │
 ├── objective_manager.py
 │         │
 │         ▼
 │      SQLite
 │
 ├── rag.py
 │         │
 │         ▼
 │      ChromaDB
 │
 └── llm.py
           │
           ▼
        Ollama
```

---

# Project Structure

```text
Ted-ai/
├── app.py
├── database/
│   ├── init_db.py
│   ├── pentest.db
│   └── chroma/
│
├── knowledge/
│   └── api.md
│
├── memory/
│
├── llm.py
├── objective_manager.py
├── rag.py
├── ingest.py
│
└── venv/
```

---

# How It Works

When a user asks a question, Ted-AI performs the following workflow:

```text
User Question
      │
      ▼
Load Active Engagement
      │
      ▼
Search Knowledge Base
      │
      ▼
Build Context Prompt
      │
      ▼
Send Prompt To Ollama
      │
      ▼
Generate Response
      │
      ▼
Display Result
```

Example:

```text
Ted-ai> ask How should I test JWT authentication?
```

Workflow:

1. Load current engagement from SQLite.
2. Search ChromaDB for relevant notes.
3. Combine engagement + notes + question.
4. Send prompt to Qwen.
5. Display generated answer.

---

# Installation

## Prerequisites

### Python

Verify:

```bash
python3 --version
```

Recommended:

```text
Python 3.10+
```

---

### Ollama

Install Ollama:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Verify:

```bash
ollama --version
```

---

### Download Qwen

```bash
ollama pull qwen3:8b
```

Verify:

```bash
ollama list
```

Expected output:

```text
NAME
qwen3:8b
```

---

# Setup

## Clone Repository

```bash
git clone https://github.com/yourusername/Ted-ai.git

cd Ted-ai
```

---

## Create Virtual Environment

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install ollama chromadb sentence-transformers rich pyyaml
```

---

# Initialize Database

Run once:

```bash
python database/init_db.py
```

Creates:

```text
database/pentest.db
```

---

# Add Knowledge

Create files inside:

```text
knowledge/
```

Example:

```bash
echo "JWT testing methodology" > knowledge/api.md
```

Example structure:

```text
knowledge/
├── api.md
├── jwt.md
├── graphql.md
├── mobile.md
└── auth.md
```

---

# Build Vector Database

Index knowledge:

```bash
python ingest.py
```

This:

1. Reads files in `knowledge/`
2. Generates embeddings
3. Stores vectors in ChromaDB

Output:

```text
Knowledge ingested
```

---

# Running Ted-AI

## Start Ollama

Open a separate terminal:

```bash
ollama serve
```

---

## Launch Ted-AI

```bash
python app.py
```

Expected:

```text
Ted-ai>
```

---

# Usage

## Create Engagement

```text
Ted-ai> new
```

Example:

```text
Target:
paypal.com

Objective:
Find authorization flaws
```

Result:

```text
Engagement created
```

---

## View Current Engagement

```text
Ted-ai> status
```

Example output:

```text
(1, 'paypal.com', 'Find authorization flaws')
```

---

## Ask Questions

```text
Ted-ai> ask What should I investigate next?
```

Example:

```text
Ted-ai> ask How should I test JWT authentication?
```

Ted-AI will:

* Load engagement
* Search knowledge
* Query Qwen
* Return response

---

## Exit

```text
Ted-ai> exit
```

---

# Database Design

## engagements

Stores active penetration testing engagements.

| Column    | Type    | Description       |
| --------- | ------- | ----------------- |
| id        | INTEGER | Unique ID         |
| target    | TEXT    | Target system     |
| objective | TEXT    | Testing objective |
| status    | TEXT    | Engagement status |

---

## findings

Stores findings discovered during testing.

| Column        | Type    | Description         |
| ------------- | ------- | ------------------- |
| id            | INTEGER | Unique ID           |
| engagement_id | INTEGER | Related engagement  |
| finding       | TEXT    | Finding description |
| confidence    | REAL    | Confidence score    |

Note:

The table currently exists but is not yet integrated into the workflow.

---

# ChromaDB

Purpose:

Store searchable knowledge.

Unlike SQLite:

```text
SQLite
=
Structured data
```

```text
ChromaDB
=
Semantic knowledge retrieval
```

Example:

User asks:

```text
JWT vulnerabilities
```

ChromaDB can return:

```text
Token confusion attacks
Algorithm confusion
JWT validation flaws
```

even when exact keywords do not match.

---

# Current Limitations

The current version does not yet support:

* Finding tracking
* Evidence management
* Multi-session memory
* Automated web research
* CVE intelligence
* Mobile application workflows
* API-specific workflows
* Autonomous planning
* Multi-agent architecture

---

# Planned Roadmap

## Phase 2

Finding Management

Commands:

```text
addfinding
listfindings
removefinding
```

---

## Phase 3

Evidence Tracking

Store:

* Confirmed findings
* Rejected hypotheses
* Assumptions
* Testing history

---

## Phase 4

Web Research Agent

Capabilities:

* Framework discovery
* Version research
* CVE investigation
* Technology fingerprinting

---

## Phase 5

Session Memory

Capabilities:

* Save engagement state
* Resume testing sessions
* Historical analysis

---

## Long-Term Vision

Ted-AI is intended to become an objective-driven penetration testing copilot that:

* Understands the current engagement
* Tracks collected evidence
* Maintains testing context
* Retrieves relevant methodologies
* Prioritizes likely attack paths
* Assists with Web, API, and Mobile testing
* Operates entirely locally through Ollama

without relying on cloud-based AI services.
