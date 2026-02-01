# Ollama Bench — FastAPI infra

This folder contains the minimal scaffolding for the Ollama benchmarking infra.

## What this provides ✅
- FastAPI service running on `0.0.0.0:8080`
- CORS enabled and configurable via `ALLOWED_ORIGINS`
- Endpoints:
  - `GET /` — small HTML page with links to `/health` and `/config`
  - `GET /health` — returns plain text `ok`
  - `GET /config` — returns non-sensitive config values from environment
- `results/` directory intended to be bind-mounted from the host (`./results:/app/results`) and persisted there

## Quick start (Docker Compose)

1. Ensure `results/` exists and is writable by your user (the project creates `./results` automatically, but check permissions if you see write errors).
2. Start the service:

```bash
docker compose up --build
```

3. Visit `http://localhost:8080/` or check `http://localhost:8080/health`

## Environment variables (set in `docker-compose.yml` defaults)
- `OLLAMA_BASE_URL` (default: `http://host.docker.internal:11434`) — where the host Ollama service is expected
- `RESULTS_CSV` (default: `/app/results/benchmark.csv`) — path inside container for CSV output
- `DEFAULT_NUM_CTX` (default: `2048`)
- `DEFAULT_NUM_PREDICT` (default: `256`)
- `DEFAULT_TEMPERATURE` (default: `0`)
- `GPU_VRAM_GB` (default: `8`) — note: MacBook Pro M2 typically reports 8 GB of unified memory
- `MAX_EST_VRAM_UTIL` (default: `0.80`)
- `ALLOWED_ORIGINS` (default: `*`) — if set to `*` or unset, all origins are allowed; otherwise treat as comma-separated allowed origins

## Notes & Dev tips 💡
- On Windows, use Docker Desktop with the WSL2 backend for best compatibility and `host.docker.internal` support.
- The `docker-compose.yml` adds `extra_hosts: ['host.docker.internal:host-gateway']` so Linux containers can resolve the host.
- The service ensures the results folder is writable at startup; if you bind-mount a host folder, ensure the host folder permissions allow writes from the container.

## Next steps (not implemented yet)
- Add model discovery and `/run` endpoint
- Implement CSV printout and HTML templates for results viewing
- Add tests and CI

---

For now this repo is intentionally minimal — it's just infra to wire later benchmarking steps.
