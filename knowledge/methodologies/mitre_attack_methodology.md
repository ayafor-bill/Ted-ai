# MITRE ATT&CK Methodology

## Purpose

This document defines how Ted-AI utilizes the MITRE ATT&CK framework during penetration testing and bug bounty engagements.

The objective is not to memorize ATT&CK.

The objective is to use ATT&CK as:

* An attacker behavior model
* A testing guide
* A finding classification framework
* A reporting framework
* A hypothesis generation framework

Ted-AI should use ATT&CK to understand:

```text
What attackers do
Why attackers do it
What attack path comes next
How findings connect together
```

---

# What is MITRE ATT&CK?

MITRE ATT&CK is a knowledge base of real-world attacker behaviors.

It documents:

* Tactics
* Techniques
* Procedures

Used by:

* Red Teams
* Blue Teams
* Threat Hunters
* Incident Responders
* Security Researchers

ATT&CK is not a vulnerability database.

ATT&CK describes:

```text
Attacker Behavior
```

instead of:

```text
Software Vulnerabilities
```

---

# ATT&CK Structure

The framework consists of:

```text
Tactic
    ↓
Technique
    ↓
Sub-Technique
```

Example:

```text
Initial Access
    ↓
T1190
Exploit Public Facing Application
```

---

# ATT&CK Philosophy

Every attacker follows a progression.

```text
Gain Access
       ↓
Execute Code
       ↓
Escalate Privileges
       ↓
Access Credentials
       ↓
Move Laterally
       ↓
Collect Data
       ↓
Exfiltrate Data
```

Ted-AI should continuously determine:

```text
What phase are we in?
What phase comes next?
```

---

# ATT&CK Tactics

The ATT&CK Enterprise Matrix contains multiple tactics.

For Web Application and API Testing, the most relevant are:

```text
Reconnaissance
Resource Development
Initial Access
Execution
Persistence
Privilege Escalation
Defense Evasion
Credential Access
Discovery
Collection
Exfiltration
Impact
```

---

# Reconnaissance

## Objective

Gather information about the target.

### Common Activities

```text
Subdomain Enumeration
Technology Fingerprinting
Endpoint Discovery
Employee Enumeration
Metadata Collection
DNS Enumeration
```

### Relevant Techniques

```text
T1595 Active Scanning

T1590 Gather Victim Network Information

T1592 Gather Victim Host Information

T1593 Search Open Websites

T1596 Search Open Technical Databases
```

### Ted-AI Questions

```text
What attack surface exists?

What technologies are present?

What endpoints exist?

What trust boundaries exist?
```

---

# Resource Development

## Objective

Prepare attack infrastructure.

### Examples

```text
Domains
Servers
Cloud Resources
Email Accounts
```

### Relevant Techniques

```text
T1583 Acquire Infrastructure

T1584 Compromise Infrastructure
```

### Ted-AI Usage

Often less relevant for bug bounty engagements but important during red team operations.

---

# Initial Access

## Objective

Gain entry into the target.

### Common Web Examples

```text
Authentication Bypass

Authorization Bypass

SSRF

File Upload

Remote Code Execution

Public-Facing Vulnerabilities
```

### Relevant Techniques

```text
T1190 Exploit Public Facing Application

T1133 External Remote Services

T1078 Valid Accounts
```

### Ted-AI Questions

```text
How can trust be established?

Can access controls be bypassed?

Can valid credentials be abused?
```

---

# Execution

## Objective

Execute attacker-controlled actions.

### Examples

```text
Command Injection

Server-Side Template Injection

RCE

Unsafe Deserialization

XXE
```

### Relevant Techniques

```text
T1059 Command and Scripting Interpreter
```

### Ted-AI Questions

```text
Can the application execute attacker-controlled input?

Can server-side functionality be abused?
```

---

# Persistence

## Objective

Maintain access.

### Examples

```text
Long-Lived Sessions

Persistent API Tokens

Refresh Token Abuse

Backdoor Accounts

API Key Abuse
```

### Relevant Techniques

```text
T1098 Account Manipulation

T1136 Create Account
```

### Ted-AI Questions

```text
Can access survive logout?

Can tokens remain valid indefinitely?

Can new trusted identities be created?
```

---

# Privilege Escalation

## Objective

Gain higher privileges.

### Examples

```text
Role Manipulation

JWT Claim Abuse

Admin Endpoint Access

Broken Access Control
```

### Relevant Techniques

```text
T1078 Valid Accounts

T1548 Abuse Elevation Control Mechanism
```

### Ted-AI Questions

```text
Can a user become an administrator?

Can trust levels be increased?
```

---

# Defense Evasion

## Objective

Avoid detection.

### Examples

```text
Log Manipulation

Input Obfuscation

Alternate Endpoints

Session Rotation Abuse
```

### Relevant Techniques

```text
T1070 Indicator Removal

T1027 Obfuscated Files or Information
```

### Ted-AI Questions

```text
Can activity avoid monitoring?

Can logs be manipulated?
```

---

# Credential Access

## Objective

Obtain credentials.

### Examples

```text
Credential Exposure

JWT Secrets

Password Reset Abuse

API Key Leakage

Source Code Exposure
```

### Relevant Techniques

```text
T1552 Unsecured Credentials

T1110 Brute Force

T1555 Credentials from Password Stores
```

### Ted-AI Questions

```text
Can credentials be disclosed?

Can credentials be generated?

Can credentials be abused?
```

---

# Discovery

## Objective

Learn more about the environment.

### Examples

```text
User Enumeration

Role Enumeration

API Enumeration

GraphQL Introspection

Tenant Enumeration
```

### Relevant Techniques

```text
T1087 Account Discovery

T1046 Network Service Discovery
```

### Ted-AI Questions

```text
What additional information becomes available after access?
```

---

# Collection

## Objective

Gather valuable information.

### Examples

```text
PII

Financial Data

Administrative Data

Internal Documents

API Responses
```

### Relevant Techniques

```text
T1213 Data from Information Repositories
```

### Ted-AI Questions

```text
What sensitive data can be accessed?
```

---

# Exfiltration

## Objective

Remove data from the target.

### Examples

```text
API Export Functions

Bulk Downloads

Reporting Features

File Exports
```

### Relevant Techniques

```text
T1041 Exfiltration Over Web Services
```

### Ted-AI Questions

```text
Can collected data leave the environment?
```

---

# Impact

## Objective

Demonstrate business impact.

### Examples

```text
Account Takeover

Financial Loss

Data Disclosure

Service Disruption

Privilege Escalation
```

### Relevant Techniques

```text
T1499 Endpoint Denial of Service

T1485 Data Destruction
```

### Ted-AI Questions

```text
What is the real business consequence?
```

---

# MITRE Mapping Process

Every confirmed finding should be mapped.

Example:

```text
Finding:
Broken Access Control

OWASP:
A01 Broken Access Control

MITRE:
T1078 Valid Accounts

Impact:
Privilege Escalation
```

---

# ATT&CK-Based Hypothesis Generation

Ted-AI should use ATT&CK to identify missing attack paths.

Example:

```text
Current Evidence:

User Access
      ↓
Admin Endpoint Exists
      ↓
JWT Used
```

Potential ATT&CK Hypotheses:

```text
Privilege Escalation

Credential Access

Persistence

Discovery
```

The framework should help identify:

```text
What has not been tested yet?
```

---

# ATT&CK Reporting Framework

Every finding should contain:

## ATT&CK Tactic

## ATT&CK Technique

## Attack Objective

## Business Impact

## Evidence

## Reproduction Steps

## Mitigation

---

# Ted-AI MITRE Principle

The reasoning engine should continuously ask:

"What would a real attacker attempt next based on the access, trust, privileges, credentials, and information currently available?"

The purpose of ATT&CK inside Ted-AI is not classification.

The purpose is prediction.

ATT&CK should help Ted-AI predict likely attack paths, identify missing tests, prioritize high-value actions, and map findings to real-world attacker behavior.
