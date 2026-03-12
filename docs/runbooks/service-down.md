# Runbook: Service Down / 503 Errors

## Symptoms
- API returning 503 Service Unavailable
- High error rate in logs
- Health check failing

## Diagnostic Steps
1. Check service health: `curl -f http://<service-url>/health`
2. Check recent logs: `tail -100 /var/log/app.log | grep ERROR`
3. Check pod/container status: `kubectl get pods -n production`
4. Check resource usage: `kubectl top pods`
5. Check upstream dependencies: `curl -f http://<dependency>/health`

## Resolution
- If memory issue: scale up replicas or increase memory limit
- If connection pool exhausted: restart service with `kubectl rollout restart deployment/<name>`
- If dependency down: escalate to dependency owner

## Escalation
- SEV1: Page on-call SRE
- SEV2: Notify in #incidents Slack channel
