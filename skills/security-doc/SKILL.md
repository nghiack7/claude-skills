---
name: security-doc
description: This skill should be used when the user asks to "create security doc", "write security documentation", "tạo tài liệu bảo mật", "viết security doc", "document security vulnerability", "security assessment", or needs a security documentation template for engineering.
---

# Security Documentation: [Title]

> **Purpose:** [Brief description of security concern, policy, or assessment]

---

## Document Classification

**Security ID:** `SEC-XXX`
**Type:** Vulnerability Report | Security Audit | Security Policy | Risk Assessment | Incident Report
**Severity:** Critical | High | Medium | Low | Informational
**Confidentiality:** Public | Internal | Confidential | Restricted
**Status:** Draft | Under Review | Approved | Resolved | Archived

---

## Executive Summary

[2-3 paragraphs summarizing the security issue, policy, or findings. Should be understandable by non-technical stakeholders.]

### Key Points

- **Risk Level:** [Critical/High/Medium/Low]
- **Affected Systems:** [List of systems/components]
- **Business Impact:** [Potential impact if exploited/not addressed]
- **Recommendation:** [Primary action required]
- **Timeline:** [Urgency for remediation]

---

## Detailed Description

### Background

[Context about the system, component, or situation being documented]

### Security Concern

[Detailed explanation of the security issue, vulnerability, or policy requirement]

### Technical Details

**Affected Components:**
- Component 1: [Name and description]
- Component 2: [Name and description]

**Attack Surface:**
- [Area of vulnerability]
- [Potential entry points]

**Threat Actors:**
- [Who might exploit this]
- [Motivation for attack]

---

## Vulnerability Details (If Applicable)

### CWE Classification

**CWE ID:** [CWE-XXX]
**CWE Name:** [Common Weakness Enumeration name]
**CWE Link:** https://cwe.mitre.org/data/definitions/XXX.html

### CVE Information (If Applicable)

**CVE ID:** CVE-YYYY-XXXXX
**CVE Score (CVSS v3):** X.X (Critical/High/Medium/Low)

### Vulnerability Type

- [ ] SQL Injection
- [ ] Cross-Site Scripting (XSS)
- [ ] Cross-Site Request Forgery (CSRF)
- [ ] Authentication Bypass
- [ ] Authorization Issues
- [ ] Insecure Direct Object Reference (IDOR)
- [ ] Security Misconfiguration
- [ ] Sensitive Data Exposure
- [ ] Missing Encryption
- [ ] Insufficient Logging & Monitoring
- [ ] Server-Side Request Forgery (SSRF)
- [ ] Broken Access Control
- [ ] Using Components with Known Vulnerabilities
- [ ] Other: [Specify]

---

## Risk Assessment

### Likelihood

**Rating:** Certain | Likely | Possible | Unlikely | Rare

**Justification:**
[Why is exploitation likely or unlikely?]

### Impact

**Rating:** Catastrophic | Major | Moderate | Minor | Insignificant

**Impact Areas:**
- **Confidentiality:** [Data exposure risk]
- **Integrity:** [Data modification risk]
- **Availability:** [Service disruption risk]
- **Financial:** [Estimated cost if exploited]
- **Reputational:** [Brand damage potential]
- **Legal/Compliance:** [Regulatory violations]

### Risk Score

**Overall Risk:** [Critical (9-10) | High (7-8) | Medium (4-6) | Low (1-3)]

---

## Affected Systems

### Production Systems

| System | Environment | Severity | Status | Patched Version |
|--------|-------------|----------|--------|----------------|
| Web App | Production | Critical | Vulnerable | Pending v2.1.5 |
| API Gateway | Production | High | Vulnerable | Pending v1.8.2 |

---

## Remediation

### Immediate Actions (Critical - Within 24 hours)

1. **Action:** [Immediate mitigation step]
   - **Owner:** [Name/Team]
   - **Status:** [ ] Not Started | [ ] In Progress | [x] Complete
   - **Deadline:** YYYY-MM-DD HH:MM

### Short-term Fix (High - Within 7 days)

1. **Action:** [Proper fix implementation]
   - **Owner:** [Name/Team]
   - **Status:** [ ] Not Started | [ ] In Progress | [x] Complete
   - **Deadline:** YYYY-MM-DD

### Long-term Improvements (Medium - Within 30 days)

1. **Action:** [Architectural improvement]
   - **Owner:** [Name/Team]
   - **Status:** [ ] Not Started | [ ] In Progress | [x] Complete
   - **Deadline:** YYYY-MM-DD

---

## Recommended Solution

### Preferred Approach

**Solution:** [Describe the recommended fix]

**Implementation Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Code Changes:**
```javascript
// BEFORE (Vulnerable)
app.get('/user/:id', (req, res) => {
  const query = `SELECT * FROM users WHERE id = ${req.params.id}`;
  db.query(query);
});

// AFTER (Secure)
app.get('/user/:id', (req, res) => {
  const query = 'SELECT * FROM users WHERE id = ?';
  db.query(query, [req.params.id]);
});
```

**Testing:**
- [ ] Unit tests added for security validation
- [ ] Integration tests verify fix
- [ ] Penetration test confirms vulnerability resolved

---

## Compliance Impact

### Regulatory Requirements

- [ ] **PCI DSS:** [Requirement X.X - Impact]
- [ ] **GDPR:** [Article XX - Impact]
- [ ] **SOC 2:** [Control X.X - Impact]

---

## Detection & Monitoring

### Detection Methods

**How was this discovered?**
- [ ] Internal security audit
- [ ] Automated scanning (tool: [name])
- [ ] Penetration testing
- [ ] Bug bounty report
- [ ] Monitoring/SIEM alert

### Monitoring & Alerts

**Metrics to Track:**
- Failed authentication attempts
- Unusual API request patterns
- Data exfiltration indicators

---

## Prevention

### Root Cause Analysis

**Why did this happen?**
- [Root cause 1]
- [Root cause 2]

### Preventative Measures

**Code-Level:**
- [ ] Implement input validation library
- [ ] Add output encoding
- [ ] Use parameterized queries

**Process-Level:**
- [ ] Add security review to code review process
- [ ] Automated security scanning in CI/CD pipeline
- [ ] Regular penetration testing schedule

**Architecture-Level:**
- [ ] Implement Web Application Firewall (WAF)
- [ ] Add rate limiting
- [ ] Enable least-privilege access

---

## References

### Internal Documents

- [Related ADR documenting security decision]
- [Runbook for incident response]
- [Architecture diagram]

### External Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Details](https://cwe.mitre.org/)

---

## Testing & Validation

### Security Testing Checklist

- [ ] Vulnerability scanner confirms issue resolved
- [ ] Manual penetration test performed
- [ ] Code review by security team
- [ ] Automated security tests added to CI/CD
- [ ] Regression testing completed

---

## Lessons Learned

### What Went Well

- [Positive aspect of response/discovery]

### What Could Be Improved

- [Area for improvement]

### Action Items

1. [ ] [Action to prevent similar issues] - Owner: [Name] - Due: [Date]

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | YYYY-MM-DD | [Name] | Initial security assessment |
| 2.0.0 | YYYY-MM-DD | [Name] | Vulnerability resolved |

---

## Approval & Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Security Lead | [Name] | YYYY-MM-DD | Approved |
| Engineering Lead | [Name] | YYYY-MM-DD | Approved |

---

## Notes

- This document contains sensitive security information and should be handled according to company security policy
- Access should be restricted to authorized personnel only
- Do not share full exploit details publicly until responsible disclosure timeline is complete
