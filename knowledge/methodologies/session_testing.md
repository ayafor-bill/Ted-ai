# Session Management Testing Methodology

## Purpose

This document defines the session management testing methodology used by Ted-AI.

The methodology combines concepts from:

* OWASP Web Security Testing Guide
* OWASP Session Management Cheat Sheet
* OWASP Top 10
* PTES
* NIST Security Assessment Principles
* Modern Web Application Security Research
* Modern Bug Bounty Methodologies

The purpose is to systematically evaluate how an application establishes, maintains, validates, rotates, and terminates authenticated sessions.

Authentication verifies identity.

Session management maintains trust.

A secure authentication system can still be compromised through weak session management.

---

# Core Philosophy

Session management answers one question:

```text
How does the application remember who the user is?
```

The objective of session testing is to determine whether that trust can be:

* Stolen
* Reused
* Extended
* Manipulated
* Fixed
* Shared
* Bypassed

---

# Session Testing Workflow

```text
Session Discovery
        ↓
Token Analysis
        ↓
Cookie Analysis
        ↓
Session Creation Testing
        ↓
Session Rotation Testing
        ↓
Expiration Testing
        ↓
Logout Testing
        ↓
Session Fixation Testing
        ↓
Session Hijacking Testing
        ↓
Cross-Device Testing
        ↓
Evidence Collection
        ↓
Reporting
```

---

# Phase 1: Session Discovery

## Objective

Identify every mechanism used to maintain authenticated state.

Identify:

* Cookies
* JWTs
* Bearer Tokens
* Refresh Tokens
* API Keys
* Session Identifiers

Examples:

```http
Cookie:
sessionid=abc123

Authorization:
Bearer eyJ...
```

Questions:

* How is trust maintained?
* What identifies the user?
* How long does trust persist?

Output:

```text
Session Inventory
```

---

# Phase 2: Session Token Analysis

## Objective

Determine whether session identifiers are secure.

Review:

* Length
* Entropy
* Predictability
* Structure

Questions:

* Are session identifiers random?
* Are tokens guessable?
* Do identifiers contain sensitive information?

Examples of concerns:

```text
sessionid=1001
sessionid=1002
sessionid=1003
```

or

```text
user_123_timestamp
```

Output:

```text
Token Assessment
```

---

# Phase 3: Cookie Security Testing

## Objective

Evaluate cookie security controls.

Review:

* Secure Flag
* HttpOnly Flag
* SameSite Attribute
* Path Restrictions
* Domain Restrictions

Questions:

* Are cookies exposed to JavaScript?
* Can cookies be sent over HTTP?
* Are cookies unnecessarily shared?

Example:

```http
Set-Cookie:
sessionid=abc123;
Secure;
HttpOnly;
SameSite=Strict
```

Output:

```text
Cookie Security Findings
```

---

# Phase 4: Session Creation Testing

## Objective

Evaluate session generation after authentication.

Review:

* Session generation
* Token issuance
* Cookie creation

Questions:

* Is a new session created after login?
* Is trust established securely?
* Can sessions be reused?

Output:

```text
Session Creation Assessment
```

---

# Phase 5: Session Rotation Testing

## Objective

Determine whether sessions rotate appropriately.

Critical events:

* Login
* Password Change
* MFA Enrollment
* Privilege Changes

Questions:

* Does the session identifier change?
* Can old identifiers still be used?
* Are privileged sessions regenerated?

Output:

```text
Rotation Findings
```

---

# Phase 6: Session Expiration Testing

## Objective

Determine how long sessions remain valid.

Review:

* Idle Timeout
* Absolute Timeout
* Refresh Behavior

Questions:

* How long does trust persist?
* Can sessions survive indefinitely?
* Is user inactivity enforced?

Test:

```text
5 minutes
15 minutes
30 minutes
1 hour
24 hours
```

Output:

```text
Expiration Findings
```

---

# Phase 7: Logout Testing

## Objective

Determine whether logout properly terminates trust.

Questions:

* Is the session destroyed?
* Are refresh tokens invalidated?
* Can old tokens still be used?

Testing:

```text
Login
↓
Capture Session
↓
Logout
↓
Replay Session
```

Expected:

```text
Access Denied
```

Output:

```text
Logout Findings
```

---

# Phase 8: Session Fixation Testing

## Objective

Determine whether attackers can force users to use attacker-controlled sessions.

Workflow:

```text
Attacker Creates Session
          ↓
Victim Uses Session
          ↓
Victim Logs In
          ↓
Attacker Reuses Session
```

Questions:

* Does login regenerate identifiers?
* Can existing sessions become authenticated?

Output:

```text
Session Fixation Findings
```

---

# Phase 9: Session Hijacking Testing

## Objective

Determine whether active sessions can be stolen and reused.

Sources:

* XSS
* Leaked Cookies
* Network Exposure
* Browser Storage

Questions:

* Can stolen tokens be replayed?
* Are device bindings enforced?
* Is anomaly detection present?

Output:

```text
Session Hijacking Findings
```

---

# Phase 10: Cross-Device Testing

## Objective

Evaluate session behavior across devices.

Test:

```text
Device A
      ↓
Login

Device B
      ↓
Reuse Session
```

Questions:

* Are concurrent sessions allowed?
* Are sessions device-bound?
* Are alerts generated?

Output:

```text
Cross-Device Findings
```

---

# Phase 11: Privilege Change Testing

## Objective

Evaluate session behavior during privilege transitions.

Examples:

```text
User
  ↓
Admin

Password Change

Role Assignment
```

Questions:

* Does privilege elevation regenerate sessions?
* Can old sessions retain elevated access?

Output:

```text
Privilege Transition Findings
```

---

# Phase 12: Refresh Token Testing

## Objective

Evaluate token renewal mechanisms.

Review:

* Rotation
* Expiration
* Revocation
* Reuse Detection

Questions:

* Can refresh tokens be reused?
* Can revoked tokens still issue sessions?
* Are stolen refresh tokens valuable?

Output:

```text
Refresh Token Findings
```

---

# Phase 13: API Session Testing

## Objective

Evaluate API-specific session handling.

Review:

* JWT
* OAuth Tokens
* Bearer Tokens
* Refresh Tokens

Questions:

* Can tokens be replayed?
* Are scopes enforced?
* Are sessions invalidated correctly?

Output:

```text
API Session Findings
```

---

# Phase 14: Evidence Collection

Every session finding should include:

* Session Identifier Type
* Authentication Method
* Request
* Response
* Reproduction Steps
* Impact

Required Evidence:

```text
Authenticated State
Session Token
Observed Behavior
Security Impact
```

---

# Phase 15: Finding Validation

Before confirming a finding:

* Verify reproducibility
* Verify impact
* Verify consistency
* Verify session persistence

Rejected hypotheses should be documented.

---

# Phase 16: Reporting

Every finding should contain:

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

1. Session Fixation
2. Session Hijacking
3. Missing Session Rotation
4. Missing Session Expiration
5. Logout Failures
6. Refresh Token Abuse
7. Weak Session Identifiers
8. Cookie Security Misconfigurations
9. Privilege Transition Issues
10. Long-Lived Sessions

---

# Relevant MITRE ATT&CK Techniques

Frequently associated techniques:

```text
T1078 - Valid Accounts
T1550 - Use Alternate Authentication Material
T1539 - Steal Web Session Cookie
T1185 - Browser Session Hijacking
```

---

# Ted-AI Session Testing Principle

The reasoning engine should continuously ask:

"Can an attacker establish, steal, reuse, extend, manipulate, or maintain trust within the application without performing the intended authentication process?"
