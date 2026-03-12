# Runbook: Database Issues

## Symptoms
- Connection timeout errors
- "Too many connections" errors
- Slow queries > 5s

## Diagnostic Steps
1. Check connection count: `SELECT count(*) FROM pg_stat_activity;`
2. Check long-running queries: `SELECT pid, now() - query_start AS duration, query FROM pg_stat_activity WHERE state = 'active' ORDER BY duration DESC LIMIT 10;`
3. Check disk usage: `df -h /var/lib/postgresql`
4. Check replication lag (if replica): `SELECT now() - pg_last_xact_replay_timestamp() AS lag;`

## Resolution
- Kill long-running queries: `SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE duration > interval '5 minutes';`
- If connection pool full: restart application instances
- If disk full: archive old data, clean logs
