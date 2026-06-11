# Authentication Testing Methodology

## Purpose

This document defines the authentication testing methodology used by Ted-AI.

The methodology combines concepts from:

* OWASP Web Security Testing Guide
* OWASP Authentication Cheat Sheet
* OWASP Top 10
* OWASP API Security Top 10
* NIST SP 800-63 Digital Identity Guidelines
* PTES Authentication Testing Principles
* Modern Bug Bounty Research

The purpose is to systematically evaluate how an application verifies identity and whether attackers can bypass, abuse, manipulate, or weaken authentication mechanisms.

---

# Core Philosophy

Authentication answers one question:

```text
Who are you?
```

The objective of authentication testing is to determine whether the application incorrectly answers that question.

Authentication weaknesses often result in:

* Account Takeover
* Privilege Escalation
* Unauthorized Access
* Session Hijacking
* Data Exposure

---

# Authentication Testing Workflow

```text
Authentication Discovery
          ↓
Credential Testing
          ↓
Registration Testing
          ↓
Login Testing
          ↓
Password Reset Testing
          ↓
MFA Testing
          ↓
Session Testing
          ↓
Token Testing
          ↓
Federation Testing
          ↓
Evidence Collection
          ↓
Reporting
```

---

# Phase 1: Authentication Discovery

## Objective

Identify all authentication mechanisms.

Questions:

* How do users authenticate?
* What identity providers exist?
* What tokens are used?
* Is MFA available?

Identify:

* Login pages
* API authentication endpoints
* SSO providers
* OAuth providers
* JWT implementations
* Session cookies

Examples:

```text
/login
/auth/login
/api/login
/oauth
/sso
```

Output:

```text
Authentication Inventory
```

---

# Phase 2: Registration Testing

## Objective

Evaluate account creation controls.

Test:

* Duplicate registrations
* Email verification bypasses
* Username enumeration
* Privilege assignment
* Registration race conditions

Questions:

* Can accounts be created without verification?
* Are administrative attributes assignable?
* Can restrictions be bypassed?

Example:

```json
{
  "role": "admin"
}
```

Output:

```text
Registration Findings
```

---

# Phase 3: Credential Testing

## Objective

Evaluate password security controls.

Test:

* Weak passwords
* Default passwords
* Password policy enforcement
* Credential stuffing protections
* Password reuse controls

Questions:

* Can common passwords be used?
* Is password complexity enforced?
* Are breached passwords accepted?

Output:

```text
Credential Security Assessment
```

---

# Phase 4: Login Testing

## Objective

Evaluate login functionality.

Test:

* Error messages
* Username enumeration
* Account lockout
* Rate limiting
* CAPTCHA protections

Questions:

* Can valid usernames be identified?
* Can accounts be brute forced?
* Are login attempts monitored?

Examples:

```text
Invalid Password

User Does Not Exist
```

Different responses may indicate enumeration.

Output:

```text
Login Assessment
```

---

# Phase 5: Password Reset Testing

## Objective

Evaluate account recovery mechanisms.

Password reset functionality is frequently weaker than primary authentication.

Test:

* Reset token generation
* Token expiration
* Token reuse
* Predictable tokens
* Email change workflows

Questions:

* Can reset tokens be guessed?
* Can tokens be reused?
* Can another user's account be reset?

Output:

```text
Password Reset Findings
```

---

# Phase 6: Multi-Factor Authentication Testing

## Objective

Determine whether MFA can be bypassed.

Test:

* MFA enforcement
* Alternate login paths
* Session reuse
* Recovery flows
* Trusted devices

Questions:

* Can MFA be skipped?
* Can recovery functions bypass MFA?
* Can existing sessions bypass enforcement?

Output:

```text
MFA Assessment
```

---

# Phase 7: Session Authentication Testing

## Objective

Determine whether authenticated sessions are secure.

Review:

* Session creation
* Session rotation
* Session expiration
* Logout functionality

Questions:

* Does login rotate sessions?
* Are old sessions invalidated?
* Are sessions terminated on logout?

Output:

```text
Session Authentication Findings
```

---

# Phase 8: JWT Testing

## Objective

Assess JWT implementation security.

Review:

* Algorithms
* Claims
* Expiration
* Signature validation

Test:

* Algorithm confusion
* Missing signature verification
* Weak secrets
* Claim manipulation

Review Claims:

```json
{
  "sub": "123",
  "role": "user",
  "exp": 1710000000
}
```

Questions:

* Are claims trusted excessively?
* Can authorization be influenced?

Output:

```text
JWT Findings
```

---

# Phase 9: OAuth Testing

## Objective

Assess OAuth implementation security.

Review:

* Authorization flows
* Scopes
* Redirect URIs
* Token handling

Test:

* Open redirects
* Scope escalation
* Authorization code leakage
* Access token leakage

Questions:

* Are redirect URIs validated?
* Can scopes be manipulated?

Output:

```text
OAuth Findings
```

---

# Phase 10: Single Sign-On Testing

## Objective

Evaluate federated authentication.

Review:

* SAML
* OAuth
* OpenID Connect

Questions:

* Are assertions validated?
* Can identities be spoofed?
* Are trust relationships secure?

Output:

```text
Federation Findings
```

---

# Phase 11: API Authentication Testing

## Objective

Assess API-specific authentication controls.

Review:

* API Keys
* Bearer Tokens
* JWT
* OAuth

Questions:

* Can tokens be reused?
* Are tokens scoped properly?
* Are credentials exposed?

Output:

```text
API Authentication Findings
```

---

# Phase 12: Authentication Abuse Testing

## Objective

Identify abuse opportunities.

Examples:

* Password spraying
* Credential stuffing
* Brute force attacks
* Token replay
* Session replay

Questions:

* Can authentication mechanisms be abused at scale?
* Are protections effective?

Output:

```text
Abuse Findings
```

---

# Phase 13: Evidence Collection

Every finding must include:

* Request
* Response
* Authentication state
* Reproduction steps
* Impact

Required evidence:

```text
Account A
Account B
Authentication Method
Observed Behavior
```

---

# Phase 14: Finding Validation

Before confirming a finding:

* Verify reproducibility
* Verify impact
* Verify consistency
* Verify evidence

Rejected hypotheses should be recorded.

---

# Phase 15: Reporting

Every authentication finding should contain:

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

1. MFA Bypass
2. Account Takeover
3. Password Reset Flaws
4. OAuth Misconfigurations
5. JWT Validation Issues
6. Session Fixation
7. Session Hijacking
8. Username Enumeration
9. Credential Stuffing Exposure
10. Weak Authentication Policies

---

# Relevant MITRE ATT&CK Techniques

Frequently associated techniques:

```text
T1078 - Valid Accounts
T1110 - Brute Force
T1556 - Modify Authentication Process
T1550 - Use Alternate Authentication Material
```

---

# Ted-AI Authentication Principle

The reasoning engine should continuously ask:

"Can an attacker become another user, remain authenticated longer than intended, bypass identity verification controls, or gain privileges beyond those originally granted?"
