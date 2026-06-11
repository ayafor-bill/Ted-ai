# Security Assessment Methodology Framework

## Purpose

This document serves as the foundational methodology layer for Ted-AI. It combines concepts from five major security testing frameworks:

* Open Source Security Testing Methodology Manual (OSSTMM)
* Open Web Application Security Project (OWASP)
* Penetration Testing Execution Standard (PTES)
* Information Systems Security Assessment Framework (ISSAF)
* NIST SP 800-115 Technical Guide to Information Security Testing and Assessment

The purpose of this framework is not to replace these methodologies but to extract their most valuable concepts and create a unified process that can guide objective-driven penetration testing engagements.

---

# Methodology Comparison

## OSSTMM

### Primary Focus

Security measurement and operational security assessment.

### Strengths

* Measurable and repeatable testing
* Emphasis on attack surface analysis
* Objective and evidence-driven assessments
* Strong focus on trust relationships
* Comprehensive coverage of human, physical, wireless, telecommunications, and data networks

### Weaknesses

* Highly theoretical
* Limited practical testing guidance
* Complex metrics that are difficult to apply during modern engagements

### Key Concept For Ted-AI

Always measure and document attack surface rather than relying on assumptions. Evidence should be separated from interpretation. Findings should be based on observable facts.

---

## OWASP

### Primary Focus

Web application security testing.

### Strengths

* Highly practical
* Modern web application focus
* Strong vulnerability categorization
* Excellent testing guidance
* Widely adopted by industry

### Weaknesses

* Primarily web focused
* Less emphasis on engagement management

### Key Concept For Ted-AI

Use structured testing workflows and prioritize testing based on attack surface, authentication, authorization, input handling, business logic, and application architecture.

---

## PTES

### Primary Focus

End-to-end penetration testing lifecycle.

### Strengths

* Defines complete engagement process
* Strong focus on planning
* Clear testing phases
* Excellent reporting workflow

### Weaknesses

* Limited technical depth
* Requires supporting methodologies

### Key Concept For Ted-AI

Every engagement should follow a structured lifecycle from scoping through reporting. Testing should always be linked to a defined objective.

---

## ISSAF

### Primary Focus

Structured security assessment methodology.

### Strengths

* Detailed assessment process
* Strong documentation practices
* Comprehensive assessment coverage

### Weaknesses

* Less commonly used today
* Can become documentation heavy

### Key Concept For Ted-AI

Testing activities should be traceable, repeatable, and fully documented.

---

## NIST SP 800-115

### Primary Focus

Information security testing and assessment.

### Strengths

* Strong planning requirements
* Rules of engagement focus
* Formal assessment structure
* Strong reporting practices

### Weaknesses

* Less focused on modern bug bounty workflows
* More enterprise oriented

### Key Concept For Ted-AI

Every assessment begins with planning and rules of engagement. Evidence collection and reporting are mandatory phases, not optional activities.

---

# Unified Ted-AI Methodology

Ted-AI combines the strongest aspects of all five methodologies into a single operational workflow.

```text
Objective
    ↓
Reconnaissance
    ↓
Discovery
    ↓
Hypothesis Generation
    ↓
Validation
    ↓
Evidence Collection
    ↓
Finding Confirmation
    ↓
Reporting
```

---

# Phase 1: Objective Definition

Before testing begins, establish:

* Target
* Scope
* Objective
* Constraints
* Rules of Engagement

Questions:

* What is the target?
* What are we trying to achieve?
* What systems are in scope?
* What actions are prohibited?

Output:

* Engagement Record

---

# Phase 2: Reconnaissance

Collect information about the target.

Examples:

* Subdomains
* Endpoints
* Technologies
* Frameworks
* Authentication methods
* Third-party integrations

Output:

* Attack Surface Inventory

---

# Phase 3: Discovery

Identify potential weaknesses.

Examples:

* Exposed functionality
* Hidden endpoints
* Weak access controls
* Misconfigurations
* Business logic weaknesses

Output:

* Potential Attack Paths

---

# Phase 4: Hypothesis Generation

Generate testable assumptions.

Examples:

* Authorization checks may be missing.
* Rate limiting may not exist.
* Object references may be predictable.

Rules:

* Hypotheses must be evidence-based.
* Avoid assumptions unsupported by observations.

Output:

* Prioritized Testing Queue

---

# Phase 5: Validation

Attempt to prove or disprove hypotheses.

Examples:

* Request manipulation
* Role switching
* Parameter modification
* Workflow abuse

Rules:

* Validation must be repeatable.
* Results must be reproducible.

Output:

* Confirmed or Rejected Hypothesis

---

# Phase 6: Evidence Collection

Every finding requires evidence.

Required Evidence:

* Request
* Response
* Steps to reproduce
* Impact
* Affected asset

Rules:

* Evidence precedes conclusions.
* Evidence must support every finding.

Output:

* Evidence Record

---

# Phase 7: Finding Confirmation

Convert validated issues into findings.

Required Elements:

* Title
* Description
* Impact
* Severity
* Evidence
* Remediation

Output:

* Finding Record

---

# Phase 8: Reporting

Document the engagement.

Required Sections:

* Executive Summary
* Scope
* Methodology
* Findings
* Evidence
* Risk Ratings
* Recommendations

Output:

* Assessment Report

---

# Ted-AI Operating Principles

The reasoning engine should always follow these rules:

1. Objectives override curiosity.
2. Evidence overrides assumptions.
3. Validation overrides speculation.
4. Findings require proof.
5. Rejected hypotheses must be tracked.
6. Testing should prioritize the highest probability attack path.
7. Avoid rabbit holes when evidence is weak.
8. Recommendations should be based on current engagement context.
9. Reporting begins during testing, not after testing.
10. Every action should move the engagement closer to its objective.

---

# Framework Influence Summary

| Framework       | Contribution                                           |
| --------------- | ------------------------------------------------------ |
| OSSTMM          | Evidence-driven testing and attack surface measurement |
| OWASP           | Web application testing methodology                    |
| PTES            | Engagement lifecycle management                        |
| ISSAF           | Structured assessment documentation                    |
| NIST SP 800-115 | Planning, evidence collection, and reporting           |

---

# Ted-AI Core Philosophy

Ted-AI is not a vulnerability encyclopedia.

Ted-AI is an objective-driven security assessment assistant.

The system should continuously answer one question:

"What is the highest-value action we should perform next based on the current objective, available evidence, and known attack surface?"
