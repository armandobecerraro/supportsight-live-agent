# SupportSight Live — Architecture

## System Overview

SupportSight Live is a multimodal incident support agent built on a polyglot microservices architecture. It uses the Gemini Live API for real-time voice, vision, and text reasoning, combined with specialized agents for log analysis, runbook retrieval, and safe action execution.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                             │
│   ┌──────────────────────┐     ┌───────────────────────────────┐   │
│   │  Next.js Web Client  │     │   Flutter Desktop/Mobile App  │   │
│   │    (TypeScript)      │     │          (Dart)                │   │
│   └──────────┬───────────┘     └──────────────┬────────────────┘   │
└──────────────┼──────────────────────────────────┼───────────────────┘
               │ HTTP/REST                         │ HTTP/REST
               ▼                                   ▼
┌─────────────────────────────────────────────────────────────────────┐
│              BACKEND ORCHESTRATOR (Python + FastAPI)                │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                     Orchestrator Service                      │  │
│  │  ┌─────────────┐ ┌──────────────┐ ┌────────────────────────┐ │  │
│  │  │ Vision      │ │  Incident    │ │  Runbook / RAG          │ │  │
│  │  │ Agent       │ │  Analyst     │ │  Agent                  │ │  │
│  │  └──────┬──────┘ └──────┬───────┘ └──────────┬─────────────┘ │  │
│  │         │               │                      │              │  │
│  │         └───────────────┴──────────────────────┘              │  │
│  │                         │                                     │  │
│  │                   ┌─────▼──────┐                             │  │
│  │                   │  Gemini    │ ← Google GenAI SDK           │  │
│  │                   │  Live API  │                             │  │
│  │                   └────────────┘                             │  │
│  │  ┌─────────────┐ ┌──────────────┐  ┌─────────────────────┐  │  │
│  │  │ Action      │ │  Session     │  │  Safety Layer       │  │  │
│  │  │ Agent       │ │  Service     │  │  + Guardrails       │  │  │
│  │  └─────────────┘ └──────────────┘  └─────────────────────┘  │  │
│  └──────────────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────┬──────────────────┘
                       │                           │
          ┌────────────▼──────┐    ┌──────────────▼──────────────┐
          │   LOGS SERVICE    │    │      ACTIONS SERVICE         │
          │  (Rust + Python)  │    │      (Java + Spring Boot)    │
          │                   │    │                               │
          │  Rust parser:     │    │  • Allowlist execution       │
          │  500MB/s, <50ms   │    │  • Human confirmation gate   │
          │  PyO3 bridge      │    │  • Audit log (PostgreSQL)    │
          └───────────────────┘    └───────────────────────────────┘
                       │                           │
          ┌────────────▼───────────────────────────▼──────────────┐
          │                    PERSISTENCE                         │
          │  PostgreSQL (sessions, incidents, action logs)         │
          │  Redis (short-term session state, optional)            │
          └───────────────────────────────────────────────────────┘
```

## Technology Decisions

| Layer | Technology | Reason |
|-------|-----------|--------|
| Orchestration | Python + FastAPI | Native async, Google GenAI SDK |
| AI Model | Gemini 2.0 Flash Live | Multimodal, real-time, Live API |
| Log Parsing | Rust (PyO3) | 500MB/s throughput, <50ms P99 |
| Action Execution | Java 21 + Spring Boot 3 | Enterprise reliability, SOLID |
| Web Frontend | Next.js 14 (TypeScript) | SSR, type safety, CDN ready |
| Mobile/Desktop | Flutter (Dart) | Cross-platform, single codebase |
| Database | PostgreSQL | ACID, pgvector ready for RAG |
| Deployment | Google Cloud Run | Serverless, scales to zero |

## Design Principles

- **SOLID** — Each agent has single responsibility, injected via constructor
- **Hexagonal Architecture** — Domain independent of frameworks
- **OWASP Top 10** — Input validation, API key auth, no info leakage
- **12-Factor App** — All config via env vars, stateless services
- **Human-in-the-loop** — All destructive actions require explicit approval
- **Observability-first** — Correlation IDs, structured JSON logs, timeline audit
