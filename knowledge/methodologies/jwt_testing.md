# JSON Web Token (JWT) Testing Methodology

## Purpose

This document defines the JWT security testing methodology used by Ted-AI.

The methodology combines concepts from:

* OWASP Web Security Testing Guide
* OWASP JWT Cheat Sheet
* OWASP API Security Top 10
* RFC 7519 (JWT Specification)
* PortSwigger JWT Testing Research
* Modern API Security Research
* Bug Bounty Methodologies

The purpose is to systematically evaluate how JSON Web Tokens are generated, validated, trusted, refreshed, revoked, and used within an application.

JWTs are commonly used for:

* Authentication
* Authorization
* Session Management
* API Access Control
* Single Sign-On

A JWT weakness can often lead to:

* Account Takeover
* Privilege Escalation
* Authentication Bypass
* Authorization Bypass
* Sensitive Data Exposure

---

# Core Philosophy

JWT testing answers one question:

```text
Can trust represented by a token be abused?
```

The objective is to determine whether an attacker can:

* Forge tokens
* Modify claims
* Replay tokens
* Bypass validation
* Escalate privileges
* Abuse trust assumptions

---

# JWT Testing Workflow

```text
JWT Discovery
      ↓
Token Structure Analysis
      ↓
Claim Analysis
      ↓
Signature Validation Assessment
      ↓
Authorization Claim Testing
      ↓
Expiration Testing
      ↓
Refresh Token Testing
      ↓
Replay Testing
      ↓
Key Management Review
      ↓
Evidence Collection
      ↓
Reporting
```

---

# Phase 1: JWT Discovery

## Objective

Identify every JWT used by the application.

Common Locations:

### Authorization Header

```http
Authorization: Bearer eyJ...
```

### Cookies

```http
Cookie: access_token=eyJ...
```

### Local Storage

```javascript
localStorage.getItem("token")
```

### Session Storage

```javascript
sessionStorage.getItem("token")
```

Questions:

* Where are tokens stored?
* How many token types exist?
* What trust decisions depend on JWTs?

Output:

```text
JWT Inventory
```

---

# Phase 2: Token Structure Analysis

## Objective

Understand token construction.

JWT Structure:

```text
Header.Payload.Signature
```

Example:

```text
xxxxx.yyyyy.zzzzz
```

Review:

### Header

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### Payload

```json
{
  "sub": "123",
  "role": "user"
}
```

Questions:

* Which algorithm is used?
* Which claims exist?
* Which claims influence security decisions?

Output:

```text
JWT Structure Assessment
```

---

# Phase 3: Claim Analysis

## Objective

Identify security-sensitive claims.

Common Claims:

### Subject

```json
{
  "sub": "123"
}
```

### User Identifier

```json
{
  "user_id": "123"
}
```

### Role

```json
{
  "role": "admin"
}
```

### Permissions

```json
{
  "permissions": ["read","write"]
}
```

Questions:

* Which claims affect authorization?
* Which claims affect business logic?
* Are claims excessively trusted?

Output:

```text
Claim Assessment
```

---

# Phase 4: Signature Validation Testing

## Objective

Determine whether signatures are validated correctly.

Questions:

* Is the signature checked?
* Is verification enforced?
* Can tampered tokens be accepted?

Testing Workflow:

```text
Capture Token
      ↓
Modify Payload
      ↓
Replay Token
      ↓
Observe Response
```

Examples:

Change:

```json
{
  "role": "user"
}
```

To:

```json
{
  "role": "admin"
}
```

Output:

```text
Signature Validation Findings
```

---

# Phase 5: Authorization Claim Testing

## Objective

Determine whether authorization depends on client-controlled claims.

Review:

```json
{
  "role": "admin"
}
```

```json
{
  "is_admin": true
}
```

```json
{
  "permissions": ["all"]
}
```

Questions:

* Are privileges derived directly from JWT claims?
* Are server-side checks present?
* Can roles be manipulated?

Output:

```text
Authorization Claim Findings
```

---

# Phase 6: Expiration Testing

## Objective

Evaluate token lifetime controls.

Review Claims:

```json
{
  "exp": 1710000000
}
```

```json
{
  "iat": 1700000000
}
```

Questions:

* Do tokens expire?
* Is expiration enforced?
* Can expired tokens still be used?

Output:

```text
Expiration Findings
```

---

# Phase 7: Replay Testing

## Objective

Determine whether stolen tokens remain valuable.

Workflow:

```text
User Logs In
      ↓
Capture Token
      ↓
Reuse Token
      ↓
Observe Result
```

Questions:

* Can tokens be replayed?
* Are sessions device-bound?
* Is reuse detected?

Output:

```text
Replay Findings
```

---

# Phase 8: Refresh Token Testing

## Objective

Assess token renewal mechanisms.

Review:

* Refresh token generation
* Rotation
* Expiration
* Revocation

Questions:

* Can refresh tokens be reused?
* Are old refresh tokens invalidated?
* Can stolen refresh tokens maintain access?

Output:

```text
Refresh Token Findings
```

---

# Phase 9: Revocation Testing

## Objective

Determine whether tokens can be invalidated.

Scenarios:

### Logout

```text
Login
 ↓
Logout
 ↓
Reuse Token
```

### Password Change

```text
Login
 ↓
Change Password
 ↓
Reuse Token
```

Questions:

* Are tokens revoked?
* Does logout terminate trust?
* Does password change invalidate sessions?

Output:

```text
Revocation Findings
```

---

# Phase 10: Key Management Assessment

## Objective

Evaluate signing key security.

Review:

* Secret management
* Key rotation
* Public key exposure
* JWKS implementation

Questions:

* Are weak secrets used?
* Are keys exposed publicly?
* Is rotation implemented?

Output:

```text
Key Management Findings
```

---

# Phase 11: JWKS Testing

## Objective

Assess JSON Web Key Set implementations.

Review:

```text
/.well-known/jwks.json
```

Questions:

* Are keys managed securely?
* Can key selection be abused?
* Are verification processes secure?

Output:

```text
JWKS Findings
```

---

# Phase 12: Multi-Tenant Testing

## Objective

Determine whether tokens can cross tenant boundaries.

Questions:

* Can Tenant A access Tenant B resources?
* Are tenant identifiers trusted?
* Is isolation enforced?

Review Claims:

```json
{
  "tenant_id": "123"
}
```

Output:

```text
Tenant Isolation Findings
```

---

# Phase 13: API JWT Testing

## Objective

Evaluate JWT use in APIs.

Review:

* Access tokens
* Refresh tokens
* Service tokens

Questions:

* Are scopes enforced?
* Are permissions validated server-side?
* Can tokens access unintended endpoints?

Output:

```text
API JWT Findings
```

---

# Phase 14: Evidence Collection

Every JWT finding should include:

* Original Token
* Modified Token (if applicable)
* Request
* Response
* Authentication Context
* Reproduction Steps

Required Evidence:

```text
JWT Type
Affected Endpoint
Observed Behavior
Security Impact
```

---

# Phase 15: Finding Validation

Before confirming a finding:

* Verify reproducibility
* Verify impact
* Verify authorization effect
* Verify trust abuse

Rejected hypotheses should be documented.

---

# Phase 16: Reporting

Every JWT finding should contain:

## Title

## Description

## Impact

## Evidence

## Reproduction Steps

## Severity

## Remediation

## Related OWASP Category

## Related MITRE Technique

---

# Common High-Value Findings

Prioritize investigation of:

1. Authorization Trust in JWT Claims
2. Missing Signature Validation
3. Refresh Token Abuse
4. Replayable Tokens
5. Missing Revocation
6. Long-Lived Tokens
7. Tenant Isolation Failures
8. Weak Key Management
9. Broken Scope Validation
10. Session Persistence After Logout

---

# Relevant MITRE ATT&CK Techniques

Frequently associated techniques:

```text
T1078 - Valid Accounts
T1550 - Use Alternate Authentication Material
T1539 - Steal Web Session Cookie
T1098 - Account Manipulation
```

---

# Ted-AI JWT Testing Principle

The reasoning engine should continuously ask:

"Does the application trust information contained within the JWT more than it should, and can that trust be manipulated to gain unauthorized access, elevated privileges, persistent access, or cross-boundary control?"
