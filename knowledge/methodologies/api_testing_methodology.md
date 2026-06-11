# API Security Testing Methodology

## Purpose

This document defines the standard API security testing methodology used by Ted-AI.

The methodology combines principles from:

* OWASP API Security Top 10
* OWASP Web Security Testing Guide
* OWASP API Security Testing Framework
* PortSwigger API Testing Methodology
* NIST Assessment Principles
* Modern REST, GraphQL, and API Security Research

The purpose is not to identify every possible vulnerability.

The purpose is to systematically discover, prioritize, validate, and document the highest-value attack paths within an API ecosystem.

---

# Core Philosophy

API security testing should always follow:

```text
Discovery
    ↓
Authentication
    ↓
Authorization
    ↓
Data Exposure
    ↓
Business Logic
    ↓
Abuse Testing
    ↓
Evidence Collection
    ↓
Reporting
```

Most critical API vulnerabilities are not caused by technical exploits.

Most critical vulnerabilities are caused by:

* Broken authorization
* Broken authentication
* Excessive trust
* Business logic flaws
* Inventory failures

---

# Phase 1: Discovery and Reconnaissance

## Objective

Understand the API ecosystem.

## Questions

* What APIs exist?
* What technologies are used?
* Which endpoints are exposed?
* What versions are running?
* Is documentation available?

## Sources

* OpenAPI
* Swagger
* GraphQL schemas
* Mobile applications
* JavaScript files
* API documentation
* Postman collections
* Burp traffic

## Actions

Identify:

* Base URLs
* Endpoints
* Methods
* Parameters
* Content types
* Authentication methods

Output:

```text
API Inventory
```

---

# Phase 2: Endpoint Enumeration

## Objective

Build a complete endpoint map.

## Techniques

Review:

* JavaScript
* Mobile applications
* Swagger documentation
* OpenAPI specifications

Test:

* Hidden endpoints
* Legacy endpoints
* Deprecated endpoints
* Development endpoints

Examples:

```text
/api/
/v1/
/v2/
/admin/
/internal/
/graphql
```

Output:

```text
Endpoint Inventory
```

---

# Phase 3: Authentication Testing

## Objective

Evaluate identity verification mechanisms.

## Areas

### Credentials

Test:

* Weak passwords
* Password spraying
* Brute force protection
* Account lockout

### Tokens

Test:

* Expiration
* Revocation
* Replay
* Refresh mechanisms

### JWT

Test:

* Algorithm confusion
* Missing signature validation
* Weak secrets
* Claim manipulation

### OAuth

Test:

* Redirect URI validation
* Scope validation
* Token leakage

Output:

```text
Authentication Assessment
```

---

# Phase 4: Authorization Testing

## Objective

Determine whether users can perform unauthorized actions.

This phase receives the highest priority.

Most severe API vulnerabilities originate here.

---

## BOLA

Broken Object Level Authorization

Examples:

```text
/api/users/123
/api/users/124
```

Questions:

* Can User A access User B data?
* Can identifiers be manipulated?

---

## BOPLA

Broken Object Property Level Authorization

Questions:

* Can hidden fields be modified?
* Can restricted attributes be updated?

Example:

```json
{
  "role": "admin"
}
```

---

## BFLA

Broken Function Level Authorization

Questions:

* Can low-privilege users access administrative functions?
* Can endpoints be accessed directly?

Example:

```text
POST /admin/create-user
```

Output:

```text
Authorization Findings
```

---

# Phase 5: Data Exposure Testing

## Objective

Identify excessive data disclosure.

Review:

* Responses
* Metadata
* Hidden fields
* Internal identifiers

Examples:

```json
{
  "id": 5,
  "internal_notes": "...",
  "password_hash": "...",
  "role": "admin"
}
```

Questions:

* Is more data returned than required?
* Are internal attributes exposed?

Output:

```text
Data Exposure Findings
```

---

# Phase 6: Input Validation Testing

## Objective

Evaluate how the API handles unexpected input.

Test:

* SQL Injection
* NoSQL Injection
* Command Injection
* XML Injection
* XXE
* Server-Side Template Injection
* Header Manipulation
* Parameter Pollution

Examples:

```text
'
"
${7*7}
{{7*7}}
```

Output:

```text
Input Validation Findings
```

---

# Phase 7: Resource Consumption Testing

## Objective

Determine whether resources can be exhausted.

Test:

* Rate limits
* Pagination abuse
* Large payloads
* Deep nesting
* File uploads

Examples:

```text
?page_size=1000000
```

Questions:

* Can resources be exhausted?
* Can costs be amplified?

Output:

```text
Resource Consumption Findings
```

---

# Phase 8: Business Logic Testing

## Objective

Identify flaws in application workflows.

Examples:

* Discount abuse
* Coupon reuse
* Payment manipulation
* Race conditions
* Workflow bypasses

Questions:

* Can business rules be violated?
* Can intended workflows be bypassed?

Output:

```text
Business Logic Findings
```

---

# Phase 9: GraphQL Testing

## Objective

Assess GraphQL-specific attack surface.

Test:

* Introspection
* Query complexity
* Nested queries
* Authorization controls
* Mutations
* Field exposure

Questions:

* Can hidden schema elements be discovered?
* Can resource exhaustion occur?

Output:

```text
GraphQL Assessment
```

---

# Phase 10: SSRF Testing

## Objective

Identify server-side request execution.

Targets:

* Webhooks
* URL fetchers
* Import functions
* Preview functionality

Questions:

* Can internal systems be reached?
* Can cloud metadata services be accessed?

Output:

```text
SSRF Findings
```

---

# Phase 11: Inventory Management Testing

## Objective

Identify unmanaged API assets.

Review:

* Deprecated APIs
* Legacy versions
* Test environments
* Forgotten endpoints

Questions:

* Are undocumented APIs exposed?
* Are old versions still active?

Output:

```text
Inventory Findings
```

---

# Phase 12: Evidence Collection

Every finding must include:

* Request
* Response
* Reproduction steps
* Impact
* Affected endpoint

Rules:

* Evidence before conclusions
* Reproducibility before reporting

---

# Phase 13: Finding Validation

A finding is not confirmed until:

* Reproducible
* Repeatable
* Supported by evidence

Rejected hypotheses should also be tracked.

---

# Phase 14: Reporting

Every finding should contain:

## Title

## Description

## Impact

## Evidence

## Reproduction Steps

## Severity

## Remediation

## Related OWASP API Category

## Related MITRE Technique

---

# Priority Order

When time is limited, prioritize:

1. BOLA
2. BFLA
3. Authentication
4. Business Logic
5. Data Exposure
6. Resource Consumption
7. SSRF
8. Inventory Management
9. Input Validation

---

# Ted-AI API Testing Principle

The reasoning engine should continuously ask:

"What endpoint, workflow, permission boundary, or business process is most likely to produce a high-impact finding based on the evidence currently available?"
