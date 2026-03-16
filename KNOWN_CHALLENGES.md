# AutomatePortal — Known Challenges, Gaps & Deployment Risks

> **Last updated**: March 2026
> **Audience**: Internal — do not distribute with commercial edition

---

## 1. MFA / Human Verification (NOT HANDLED)

These are the most common blockers when automating portal logins.

| Challenge | Status | Impact |
|-----------|--------|--------|
| Image CAPTCHA ("select all traffic lights") | **Not handled** | Task fails immediately |
| reCAPTCHA v2 / v3 checkbox | **Not handled** | Task fails or hangs |
| Email verification code (OTP sent to inbox) | **Not handled** | Task hangs — no way to read email |
| SMS / text message OTP | **Not handled** | Task hangs — no way to read SMS |
| Authenticator app TOTP (Google Auth, etc.) | **Not handled** | Task fails — no TOTP generation |
| "Approve this login" push notification | **Not handled** | Task hangs waiting for approval |
| Security questions ("mother's maiden name") | **Not handled** | Could be handled via stored answers |

### Recommended Solution: Pause-and-Assist via Live Monitor

Build a **"Wait for User"** step type:

1. Task instruction includes: `"Wait for user to complete MFA"`
2. Automation **pauses**, dashboard shows alert
3. User opens **Live Monitor** (noVNC on port 6080), interacts with the real browser
4. User solves CAPTCHA / enters OTP / approves push notification
5. User clicks **Resume** in dashboard
6. Automation continues from where it paused

**Files to modify:**
- `portal_automation_agent.py` — new pause/resume signaling
- `live_monitor.html` — Resume button + status indicator
- `agent_dashboard_v2.py` — API endpoint for pause/resume

---

## 2. IP Address Detection & Blocking (NOT HANDLED)

Most portals and financial sites detect and block cloud/datacenter IPs.

| Issue | Detail |
|-------|--------|
| **AWS IP ranges are public** | Amazon publishes all their IP ranges at https://ip-ranges.amazonaws.com/ip-ranges.json — firewalls and anti-bot services use this list to block |
| **Azure / GCP same problem** | All major cloud providers have published IP ranges |
| **Anti-bot services** | Cloudflare, Akamai, DataDome, PerimeterX, Shape Security — all flag datacenter IPs |
| **Residential IP expectation** | Utility portals, banks, and government sites expect traffic from residential ISPs |
| **GeoIP mismatch** | If your account is in New Jersey but traffic comes from us-east-1 (Virginia), some sites flag this |

### Current State in Code

- `portal_automation_agent.py`: **No proxy support** — connects directly from host IP
- `direct_api_download.py`: **No proxy support** — direct requests with spoofed User-Agent only
- Nova Act: **No proxy passthrough configured**

### Mitigation Options

| Option | Complexity | Cost | Effectiveness |
|--------|-----------|------|---------------|
| **Residential proxy service** (Bright Data, Oxylabs, SmartProxy) | Medium | $15-75/mo | High — real residential IPs |
| **ISP proxy** (static residential) | Medium | $3-5/IP/mo | High — fixed clean IP |
| **Run on your home Ubuntu machine** (current approach) | None | $0 | Best — it IS your real IP |
| **VPN on AWS instance** (NordVPN, Mullvad) | Low | $5-10/mo | Medium — some VPN IPs also blocked |
| **AWS Wavelength / Outpost** | High | $$$ | Overkill |

### Recommendation

**For standard edition (personal use): run Docker on your home Ubuntu machine.** Your home ISP IP is the cleanest, cheapest, most reliable option. No proxy needed.

**For commercial edition (multi-tenant SaaS):** integrate residential proxy rotation. This becomes a must-have feature.

---

## 3. Browser Fingerprinting & Bot Detection (PARTIALLY HANDLED)

Modern anti-bot systems check more than just IP address.

| Signal | Current State | Risk |
|--------|--------------|------|
| **User-Agent string** | Static, Chrome 91 (outdated) | Medium — old version is a red flag |
| **Headless detection** | `headless=False` (good) | Low — headed mode avoids basic checks |
| **WebDriver flag** | Playwright sets `navigator.webdriver=true` | High — instant bot detection |
| **Browser fingerprint** (canvas, WebGL, fonts) | Default Playwright fingerprint | Medium — doesn't match real Chrome |
| **TLS fingerprint** (JA3/JA4) | Playwright's default | Medium — known automation fingerprint |
| **Mouse/keyboard patterns** | Nova Act generates human-like actions | Low — AI-driven interaction is natural |
| **Viewport / screen size** | Set to 1280x720 in supervisord | Low — normal resolution |
| **Timezone** | Server timezone (UTC on AWS) | Medium — mismatch with account location |
| **Language / locale** | Default (en-US) | Low |

### Current Code References

```
# supervisord.conf — fixed screen size
command=/usr/bin/Xvfb :99 -screen 0 1280x720x24

# portal_automation_agent.py — always headed
self.nova_config["headless"] = False

# direct_api_download.py — outdated static User-Agent
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...Chrome/91.0...'
```

### Quick Wins

1. **Update User-Agent** to current Chrome version (Chrome 123+)
2. **Set timezone** to match account's geographic location (`TZ=America/New_York`)
3. **Set locale** to match (`LANG=en_US.UTF-8`)

### Longer-term

4. Patch `navigator.webdriver` flag (Playwright stealth plugin)
5. Randomize canvas/WebGL fingerprints
6. Rotate User-Agent strings across sessions

---

## 4. AWS-Specific Deployment Challenges

| Challenge | Detail | Mitigation |
|-----------|--------|------------|
| **Xvfb + VNC on ECS/Fargate** | No GPU, limited display support | Use EC2 with Docker, not Fargate |
| **EBS volume for /app/data** | SQLite doesn't work on EFS | Use EBS-backed EC2 or switch to RDS/Postgres |
| **Port exposure (5000 + 6080)** | Two ports needed: app + VNC viewer | ALB with path-based routing or two listeners |
| **noVNC security** | Currently no auth on VNC stream | Add VNC password or restrict to VPN/IP whitelist |
| **Long-running tasks** | ALB default timeout is 60s | Set ALB idle timeout to 300s; gunicorn already at 120s |
| **Chromium memory usage** | Each browser session uses 200-500MB RAM | t3.small minimum (2GB), t3.medium recommended (4GB) |
| **Playwright browser install** | Downloads ~200MB Chromium at build time | Already handled — pre-installed in Dockerfile |
| **Cost** | EC2 t3.medium = ~$30/mo + ALB ~$16/mo + data transfer | Budget $50-75/mo for single instance |

### Current CloudFormation

Your `cloudformation/infrastructure.yaml` uses:
- `t3.micro` (1GB RAM) — **too small** for Chromium automation
- Elastic Beanstalk — works but limited for VNC port exposure
- No persistent volume configuration for SQLite

### Recommended AWS Architecture

```
[User] → [ALB :443] → [EC2 t3.medium]
                            ├── Docker container
                            │    ├── Gunicorn :5000 (app)
                            │    ├── Xvfb :99 (virtual display)
                            │    ├── x11vnc :5900 (VNC server)
                            │    └── noVNC :6080 (browser viewer)
                            └── EBS volume → /app/data (SQLite + vault)
```

---

## 5. Session & Cookie Challenges

| Challenge | Current State | Risk |
|-----------|--------------|------|
| **Session timeout** | No session persistence between task runs | Each run starts fresh login |
| **Cookie storage** | Not persisted across runs | Re-authenticates every time |
| **Concurrent sessions** | Portal may block multiple logins | One task at a time per credential |
| **"New device" detection** | No device fingerprint persistence | May trigger MFA every run |

### Impact

Every scheduled task run = full login cycle. This increases:
- Detection risk (frequent logins from same IP)
- MFA trigger frequency
- Execution time (login adds 30-60s per run)

### Potential Fix

Persist browser cookies/session between runs so returning visits look like the same "device." Nova Act would need cookie save/restore support.

---

## 6. Error Handling & Resilience Gaps

| Gap | Current State | Impact |
|-----|--------------|--------|
| **No step-level retry** | Only full-task retry (max 3) | One flaky step = restart entire task |
| **No screenshot on failure** | Error logged as text only | Hard to debug what the browser showed |
| **No network error handling** | If page doesn't load, step fails | Transient network issues kill tasks |
| **No timeout per step** | Nova Act may hang indefinitely | Zombie tasks consume resources |
| **Alert on failure** | No email/Slack/webhook notification | Failures go unnoticed until you check dashboard |

### What Exists Today

```python
# portal_automation_agent.py — task-level retry only
retry_count: int = 0
max_retries: int = 3
# Retry delay: 5 minutes between attempts
```

---

## 7. Legal & Terms of Service Considerations

| Concern | Detail |
|---------|--------|
| **ToS violations** | Most portals prohibit automated access in their Terms of Service |
| **CFAA (US)** | Computer Fraud and Abuse Act — automated access without "authorization" is legally gray |
| **Rate of access** | Hitting a portal every minute could be construed as abuse |
| **Data scraping laws** | Varies by state/country; some jurisdictions restrict even your own data |
| **Credential sharing** | Storing portal credentials in your system may violate the portal's ToS |

### For Standard (Personal) Edition

Low risk — you're accessing your own accounts, your own data, from your own IP. Most legal frameworks consider this acceptable personal use.

### For Commercial Edition

Higher risk — you'd be automating access on behalf of customers. Need:
- Clear Terms of Service for your product
- Customer consent and indemnification
- Compliance review per target portal

---

## 8. Priority Action Items

### Must-Fix Before AWS Deployment

| # | Item | Effort | Files |
|---|------|--------|-------|
| 1 | Add `AUTOMATEPORTAL_EDITION` and `AUTOMATEPORTAL_LICENSE_SECRET` to supervisord env | **Done** | `supervisord.conf`, `entrypoint.sh` |
| 2 | Upgrade CloudFormation to `t3.medium` (1GB too small for Chromium) | Small | `cloudformation/infrastructure.yaml` |
| 3 | Add VNC password or IP restriction to noVNC | Small | `supervisord.conf`, `docker-compose.yml` |
| 4 | Update static User-Agent to current Chrome version | Trivial | `direct_api_download.py` |
| 5 | Set timezone in Docker to match account location | Trivial | `Dockerfile` |

### Should-Build Soon

| # | Item | Effort |
|---|------|--------|
| 6 | "Wait for User" pause/resume for MFA handling | Medium |
| 7 | Screenshot capture on task failure | Small |
| 8 | Email/webhook notification on task failure | Medium |
| 9 | Step-level timeout (prevent zombie tasks) | Small |
| 10 | Per-step retry (not just full-task retry) | Medium |

### Build for Commercial Edition

| # | Item | Effort |
|---|------|--------|
| 11 | Residential proxy integration | Medium |
| 12 | Browser cookie persistence across runs | Medium |
| 13 | User-Agent rotation | Small |
| 14 | Stealth patches (WebDriver flag, fingerprint) | Medium |
| 15 | Multi-tenant with per-customer proxy config | Large |

---

## 9. "It Works on My Ubuntu Machine" vs AWS — Quick Comparison

| Factor | Home Ubuntu + Docker | AWS EC2 + Docker |
|--------|---------------------|-----------------|
| IP address | Residential (clean) | Datacenter (flagged) |
| Cost | $0 (you own it) | ~$50-75/month |
| Uptime | Depends on your machine/ISP | 99.9% SLA |
| MFA handling | Walk over and type it in | Need Live Monitor VNC |
| Speed | LAN-speed to local sites | Cloud network speed |
| Scaling | One machine | Auto-scale to multiple |
| Maintenance | You manage OS updates | You manage + AWS overhead |
| Security | Behind your home router | Public internet (needs hardening) |

### Bottom Line

**For personal/standard use:** Keep running Docker on your home Ubuntu machine. It's simpler, cheaper, and avoids the IP detection problem entirely.

**For commercial/SaaS:** AWS is necessary for uptime and multi-tenant, but requires residential proxy + MFA pause/resume + browser stealth to actually work reliably.
