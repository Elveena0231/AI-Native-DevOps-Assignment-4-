ModSecurity WAF integration with Kong Gateway

Why ModSecurity
- ModSecurity is a mature, widely used open-source Web Application Firewall (WAF)
  with the OWASP Core Rule Set (CRS) available. It detects and blocks common web
  attacks (SQLi, XSS, RCE patterns) and can be deployed in multiple modes (deny,
  log-only) for staged rollout.
- Choosing ModSecurity gives flexible, rule-driven request inspection that
  complements API-layer plugins (rate-limiting, JWT) for broader protection
  against application-layer attacks and automated scanners.

Integration options with Kong on Kubernetes
- Kong Enterprise / Kong Gateway: the enterprise edition provides integrated
  WAF support (ModSecurity) via a plugin. If you use Kong Enterprise, enable the
  ModSecurity plugin in your Kong deployment and provide rules/CRS via a ConfigMap.
- Kong OSS: you can run ModSecurity as a reverse-proxy in front of Kong (sidecar
  or gateway listener) or use an ingress controller (nginx-ingress) with
  ModSecurity enabled in front of Kong.

Example Helm values (two approaches)

1) Kong Enterprise (illustrative values - use your Kong chart's structure):

```yaml
# values-kong-waf.yaml (Kong Enterprise)
kong:
  enterprise:
    enabled: true
    gateway:
      modsecurity:
        enabled: true
        mode: "blocking"    # or "detection_only"
        rulesConfigMap: kong-modsecurity-rules

# Provide CRS and custom rules in a ConfigMap named `kong-modsecurity-rules`
```

2) NGINX Ingress with ModSecurity as a WAF in front of Kong

```yaml
# values-ingress-nginx.yaml
controller:
  config:
    enable-modsecurity: "true"
    modsecurity-snippet: |
      SecRuleEngine On
      SecRequestBodyAccess On
  modsecurity:
    enabled: true
    auditLogEnabled: true
    transactionIndex: true
  modsecurityRules:
    - |-
      # include OWASP CRS and any custom rules here
      Include /etc/nginx/modsecurity.d/owasp-crs/rules/*.conf

# Deploy this ingress-nginx in front of Kong, and route traffic through it.
```

Demonstrating blocking of malicious requests

1. Deploy WAF in `blocking` mode (or enable ModSecurity `SecRuleEngine On`).
2. Send a known-malicious payload (SQLi-like). Example using curl:

```bash
curl -i -X GET "http://user-service.example.com/users?id=1' OR '1'='1" \
  -H "User-Agent: sqlmap" \
  --resolve user-service.example.com:80:<INGRESS_IP>
```

Expected result: HTTP 403 (or other rejection code) and ModSecurity logs showing
the matched rule and request details.

Notes and follow-ups
- If you run Kong OSS and prefer in-cluster WAF, the recommended production
  approach is to place a WAF-enabled ingress (nginx-ingress) or an API gateway
  edge proxy with ModSecurity in front of Kong.
- I can add a sample ConfigMap with OWASP CRS snippets and a `modsecurity` sidecar
  Deployment template to this chart if you want a fully automated deploy.

Sidecar WAF template in this chart

I added an optional sidecar-style WAF in the Helm chart driven by `values.yaml`:

- `waf.enabled`: enable the WAF Deployment + Service (default: false)
- `waf.image.repository` / `waf.image.tag`: image that provides ModSecurity + proxy
- `waf.mode`: `DetectionOnly` or `On` (blocking)
- `waf.rules`: small inline rule set (for demo); use OWASP CRS in production

To enable the sidecar WAF for `user-service`, set in `values.yaml`:

```yaml
waf:
  enabled: true
  image:
    repository: owasp/modsecurity-crs
    tag: latest
  mode: On
  rules:
    - "SecRule REQUEST_HEADERS:User-Agent \"sqlmap\" \\
        \"id:1000001,phase:1,deny,log,msg:\'Blocked sqlmap UA\'\""
```

Then render or install the chart. The WAF Deployment mounts `modsecurity.conf`
and `rules.conf` from a ConfigMap (template in the chart). The template does not
assume a specific WAF image entrypoint — you must use an image that reads the
standard ModSecurity config paths and proxies to `user-service`.

