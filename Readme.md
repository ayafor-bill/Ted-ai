# Ted-AI

## About Ted-AI

Ted-AI is a local-first, objective-driven bug bounty and penetration testing copilot designed to assist security researchers throughout the lifecycle of a security assessment. Unlike traditional AI chatbots that focus primarily on answering questions, Ted-AI is being built to maintain awareness of an active engagement, track objectives, analyze collected evidence, document findings, and recommend the highest-value next actions. The system is intended to function as a research assistant, testing companion, and reporting aid while keeping the researcher focused on the primary objective of the engagement.

The project was created to solve a common problem encountered during bug bounty hunting and penetration testing: losing focus. Modern applications are complex, attack surfaces are large, and researchers often spend significant time pursuing low-probability attack paths. Ted-AI aims to reduce this problem by continuously tracking the engagement state, evaluating available evidence, identifying knowledge gaps, and prioritizing actions that are most likely to produce meaningful results.

The long-term vision is to create an AI system that behaves more like an experienced security consultant than a traditional chatbot. Rather than providing generic security information, Ted-AI should understand the current target, technologies in use, discovered findings, rejected hypotheses, and testing objectives. By maintaining this context throughout an engagement, the system can provide more focused guidance and improve both efficiency and consistency during testing.

---

# Complete Architecture

Ted-AI is designed using a modular architecture. Each component has a specific responsibility and communicates with other components through clearly defined interfaces. This approach allows individual parts of the system to evolve independently while maintaining a predictable workflow.

---

## High-Level Architecture

```text
                                    ┌─────────────────────┐
                                    │       User          │
                                    │ Bug Bounty Hunter   │
                                    └──────────┬──────────┘
                                               │
                                               ▼
                              ┌────────────────────────────────┐
                              │          CLI Interface         │
                              │            app.py             │
                              └──────────────┬────────────────┘
                                             │
             ┌───────────────────────────────┼───────────────────────────────┐
             │                               │                               │
             ▼                               ▼                               ▼

 ┌──────────────────┐        ┌──────────────────────┐       ┌────────────────────┐
 │ Objective Manager│        │   Evidence Manager   │       │  Findings Manager  │
 └─────────┬────────┘        └──────────┬───────────┘       └─────────┬──────────┘
           │                            │                             │
           └──────────────┬─────────────┴──────────────┬──────────────┘
                          │                            │
                          ▼                            ▼

                 ┌──────────────────────────────────────────┐
                 │            SQLite Database               │
                 │ Engagement State & Structured Data       │
                 └──────────────────────────────────────────┘

                                         │
                                         ▼

                 ┌──────────────────────────────────────────┐
                 │            Reasoning Engine              │
                 │               Qwen/Ollama               │
                 └──────────────────────────────────────────┘

                                         │
                                         ▼

                 ┌──────────────────────────────────────────┐
                 │             Research Layer               │
                 │ Dynamic Security Intelligence            │
                 └──────────────────────────────────────────┘

                                         │
          ┌──────────────────────────────┼──────────────────────────────┐
          │                              │                              │
          ▼                              ▼                              ▼

 ┌────────────────┐      ┌────────────────────┐      ┌────────────────────┐
 │ OWASP Sources  │      │ Security Research  │      │ Vendor Documentation│
 └────────────────┘      └────────────────────┘      └────────────────────┘

          │                              │                              │
          └──────────────────────────────┼──────────────────────────────┘
                                         │
                                         ▼

                       ┌──────────────────────────────┐
                       │ Recommended Next Actions     │
                       │ Testing Guidance             │
                       │ Reporting Assistance         │
                       └──────────────────────────────┘
```

---

# Architectural Philosophy

Ted-AI is designed around a simple principle:

```text
Objective
     ↓
Evidence
     ↓
Reasoning
     ↓
Action
```

Traditional AI assistants typically operate as:

```text
Question
     ↓
Knowledge
     ↓
Answer
```

Ted-AI instead operates as:

```text
Current Objective
        ↓
Current Evidence
        ↓
Current Findings
        ↓
Reasoning
        ↓
Recommended Action
```

This design allows the system to remain focused on engagement goals rather than generating generic responses.

---

# Component Breakdown

## 1. CLI Interface

### Purpose

The CLI serves as the primary user interaction layer.

### Responsibilities

* Accept commands from the user
* Display engagement information
* Present recommendations
* Manage active sessions
* Coordinate communication between modules

### Future Commands

```text
new
status
objective
add-evidence
list-evidence
add-finding
list-findings
research
report
exit
```

---

## 2. Objective Manager

### Purpose

The Objective Manager acts as the central brain of the engagement.

### Responsibilities

* Track target information
* Store testing objectives
* Maintain engagement state
* Monitor progress toward goals
* Record completed activities

### Example

```yaml
Target:
  app.example.com

Type:
  Web Application

Objective:
  Identify authorization flaws

Status:
  Active
```

---

## 3. Evidence Manager

### Purpose

Store factual observations collected during testing.

### Responsibilities

* Store requests
* Store responses
* Store screenshots
* Store endpoint discoveries
* Store reconnaissance data

### Example

```yaml
Evidence:
  Endpoint:
    /api/v1/users/12

  Observation:
    Returned another user's data

  Confidence:
    High
```

---

## 4. Findings Manager

### Purpose

Manage confirmed vulnerabilities.

### Responsibilities

* Store findings
* Track severity
* Store remediation guidance
* Link evidence to findings
* Prepare reporting information

### Example

```yaml
Finding:
  Broken Object Level Authorization

Severity:
  High

Evidence:
  #12
```

---

## 5. SQLite Database

### Purpose

Persistent structured storage.

### Stores

* Engagements
* Objectives
* Evidence
* Findings
* Notes
* Session history

### Why SQLite?

* Lightweight
* Local-first
* No external server
* Easy backups
* Fast querying

---

## 6. Reasoning Engine

### Current Implementation

```text
Ollama
+
Qwen
```

### Responsibilities

* Analyze evidence
* Compare hypotheses
* Prioritize testing paths
* Recommend next actions
* Assist reporting

### Important Principle

The model should not act as a search engine.

Instead it should answer:

```text
Given what we know,
what should we do next?
```

---

## 7. Research Layer

### Purpose

Acquire current security intelligence.

### Why It Exists

Security evolves continuously.

Static knowledge alone becomes outdated.

### Research Targets

* OWASP
* PortSwigger
* Security blogs
* Vendor documentation
* Framework documentation
* Bug bounty writeups
* Public advisories

### Responsibilities

* Gather information
* Validate findings
* Enrich context
* Support reasoning engine

---

# Engagement Lifecycle

```text
Create Engagement
        │
        ▼

Define Objective
        │
        ▼

Collect Evidence
        │
        ▼

Analyze Evidence
        │
        ▼

Generate Hypotheses
        │
        ▼

Validate Hypotheses
        │
        ▼

Confirm Findings
        │
        ▼

Map Findings
        │
        ▼

Generate Report
        │
        ▼

Close Engagement
```

---

# Long-Term System Vision

```text
                    Ted-AI

       ┌───────────────────────────┐
       │ Objective Management      │
       └─────────────┬─────────────┘
                     │
                     ▼

       ┌───────────────────────────┐
       │ Evidence Collection       │
       └─────────────┬─────────────┘
                     │
                     ▼

       ┌───────────────────────────┐
       │ Intelligent Research      │
       └─────────────┬─────────────┘
                     │
                     ▼

       ┌───────────────────────────┐
       │ Security Reasoning        │
       └─────────────┬─────────────┘
                     │
                     ▼

       ┌───────────────────────────┐
       │ Finding Validation        │
       └─────────────┬─────────────┘
                     │
                     ▼

       ┌───────────────────────────┐
       │ Report Generation         │
       └───────────────────────────┘
```

The ultimate goal of Ted-AI is not to replace the researcher but to function as a persistent engagement companion that maintains context, tracks progress, prioritizes actions, assists with research, and helps produce higher-quality security assessments while minimizing wasted effort and unnecessary rabbit holes.
