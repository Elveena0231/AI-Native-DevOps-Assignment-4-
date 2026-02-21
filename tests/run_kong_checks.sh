#!/usr/bin/env bash
set -euo pipefail

# Kubernetes-native Kong checks for assignment requirements:
# - JWT auth + bypass endpoints
# - Custom Lua header injection (X-Custom-Trace)
# - Rate limiting (10 req/min/IP)
# - IP whitelist (allow + block)
# - WAF SQLi blocking

KONG_HOST=${KONG_HOST:-localhost:8000}
USER_SVC_HOST=${USER_SVC_HOST:-localhost:18000}
HOST_HEADER=${HOST_HEADER:-user-service.example.com}
NAMESPACE=${NAMESPACE:-user-service}

info(){ echo "[INFO] $*"; }
fail(){ echo "[FAIL] $*"; exit 2; }

ensure_port_forward(){
  local url=$1
  local cmd=$2
  local name=$3

  if ! curl -sS -m 2 "$url" >/dev/null 2>&1; then
    info "Starting port-forward for $name"
    nohup bash -lc "$cmd" >/tmp/${name}.log 2>&1 &
    sleep 2
    if ! curl -sS -m 2 "$url" >/dev/null 2>&1; then
      fail "Port-forward for $name did not become ready"
    fi
  fi
}

code(){
  curl -s -o /dev/null -w "%{http_code}" "$@"
}

json_field(){
  python3 -c 'import sys, json; print(json.load(sys.stdin).get(sys.argv[1], ""))' "$1"
}

info "Ensuring local access to Kong and user-service"
ensure_port_forward "http://${KONG_HOST}/" "kubectl port-forward -n kong svc/kong-kong-proxy 8000:80" "pf-kong"
ensure_port_forward "http://${USER_SVC_HOST}/health" "kubectl port-forward -n ${NAMESPACE} svc/user-service 18000:8000" "pf-usersvc"

info "Fetching JWT token from /login"
TOKEN=$(curl -s -X POST "http://${USER_SVC_HOST}/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}' | json_field access_token)

[ -n "$TOKEN" ] || fail "Failed to fetch JWT token"

BASE_URL="http://${KONG_HOST}/users"

info "Checking bypass/protected endpoints"
health=$(code -H "Host: ${HOST_HEADER}" "http://${KONG_HOST}/health")
verify=$(code -H "Host: ${HOST_HEADER}" "http://${KONG_HOST}/verify")
users_no_auth=$(code -H "Host: ${HOST_HEADER}" "${BASE_URL}")
users_with_auth=$(code -H "Host: ${HOST_HEADER}" -H "Authorization: Bearer ${TOKEN}" "${BASE_URL}")

echo "health=$health"
echo "verify_no_token=$verify"
echo "users_no_auth=$users_no_auth"
echo "users_with_auth=$users_with_auth"

[ "$health" = "200" ] || fail "Expected /health 200, got $health"
[ "$users_no_auth" = "401" ] || fail "Expected /users without token = 401, got $users_no_auth"
[ "$users_with_auth" = "200" ] || fail "Expected /users with token = 200, got $users_with_auth"

info "Checking custom Lua header injection"
trace_header=$(curl -i -s -H "Host: ${HOST_HEADER}" -H "Authorization: Bearer ${TOKEN}" "${BASE_URL}" | awk -F': ' '/^X-Custom-Trace:/ {print $2}' | tr -d '\r')
[ -n "$trace_header" ] || fail "Expected X-Custom-Trace header, but none found"
echo "X-Custom-Trace=$trace_header"

info "Checking WAF behavior (benign -> 200, SQLi -> 403)"
benign=$(code -H "Host: ${HOST_HEADER}" -H "Authorization: Bearer ${TOKEN}" "${BASE_URL}?name=normaluser")
sqli=$(code -H "Host: ${HOST_HEADER}" -H "Authorization: Bearer ${TOKEN}" "${BASE_URL}?name='%20OR%20'1'='1%20--%20")
echo "waf_benign=$benign"
echo "waf_sqli=$sqli"

[ "$benign" = "200" ] || fail "Expected benign request 200, got $benign"
[ "$sqli" = "403" ] || fail "Expected SQLi request 403, got $sqli"

info "Checking rate-limiting behavior"
sleep 65
codes=()
for i in $(seq 1 12); do
  c=$(code -H "Host: ${HOST_HEADER}" -H "Authorization: Bearer ${TOKEN}" "${BASE_URL}")
  echo "rate_req_$i=$c"
  codes+=("$c")
done

for i in $(seq 0 9); do
  [ "${codes[$i]}" = "200" ] || fail "Expected req $((i+1))=200, got ${codes[$i]}"
done
[ "${codes[10]}" = "429" ] || fail "Expected req 11=429, got ${codes[10]}"
[ "${codes[11]}" = "429" ] || fail "Expected req 12=429, got ${codes[11]}"

info "Waiting for rate-limit reset before whitelist test"
sleep 65

info "Checking whitelist block/restore by patching allow list"
kubectl patch kongplugin ip-whitelist -n "${NAMESPACE}" --type merge -p '{"config":{"allow":["172.19.0.1"]}}' >/dev/null
sleep 2
blocked=$(code -H "Host: ${HOST_HEADER}" -H "Authorization: Bearer ${TOKEN}" "${BASE_URL}")
echo "whitelist_block=$blocked"
[ "$blocked" = "403" ] || fail "Expected blocked whitelist request=403, got $blocked"

kubectl patch kongplugin ip-whitelist -n "${NAMESPACE}" --type merge -p '{"config":{"allow":["127.0.0.1"]}}' >/dev/null
sleep 2
restored=$(code -H "Host: ${HOST_HEADER}" -H "Authorization: Bearer ${TOKEN}" "${BASE_URL}")
echo "whitelist_restored=$restored"
[ "$restored" = "200" ] || fail "Expected restored whitelist request=200, got $restored"

info "All Kubernetes Kong checks passed"
