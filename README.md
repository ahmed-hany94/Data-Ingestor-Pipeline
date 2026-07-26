### Real-Time Data Ingestion & Analytics Platform

A production-grade, event-driven polyglot platform for high-throughput data processing. Beyond the core ingestion pipeline, two domain-specific fullstack services (fintech risk scoring, proptech recommendation) and a live dashboard demonstrate end-to-end fullstack ownership across five languages and frameworks.

### 📐 System Architecture Overview

```
                          [ Client Event Streams ]
                                     │
                                     ▼ HTTP POST (Port 8080)
                         ┌─────────────────────────┐
                         │    Ingestion API (Go)   │
                         └────────────┬────────────┘
                                      │ LPUSH
                                      ▼
                            [ Redis Event Queue ]
                                      │
                                      ▼ BRPOP
                         ┌────────────────────────┐
                         │  Orchestrator (Python) │
                         │ Strategy / Factory /   │
                         │ Adapter dispatch       │
                         └──────────┬───────────┬─┘
                          HTTP call │           │ HTTP call
                                    ▼           ▼
               ┌───────────────────────┐   ┌───────────────────────────┐
               │ Fintech Risk Engine   │   │ Proptech Recommender      │
               │ (Django)              │   │ (Next.js)                 │
               └───────────┬───────────┘   └─────────────┬─────────────┘
                           │                             │
                           └──────────────┬──────────────┘
                                          ▼
                          [ Orchestrator aggregates result ]
                                 │                     │
                        PUBLISH  │                     │ INSERT
                                 ▼                     ▼
                  [ Redis Pub/Sub Channel ]   [ Event Store (Postgres) ]
                                 │                     │
                       SUBSCRIBE │                     │ REST / GraphQL query
                                 ▼                     │
                  ┌─────────────────────────┐          │
                  │ Notification WS (TS)    │          │
                  └───────────┬─────────────┘          │
                              │ WebSockets (Port 3000) │
                              ▼                        ▼
                     [ Live client alerts ] ◄──── [ Dashboard (React) ]
```

1. **Ingestion API (Go):** Validates and enriches high-velocity payload schemas concurrently before dropping them into a Redis queue.
2. **Orchestrator (Python):** Consumes queued events and routes each one to the appropriate domain service. Built around explicit OOP design patterns — Strategy for routing, Factory for constructing service adapters, Adapter for normalizing each domain service's API behind one interface — rather than embedding domain logic directly.
3. **Fintech Risk Engine (Django):** A standalone fullstack service scoring transaction risk. Includes its own data model, admin panel for reviewing flagged transactions, and REST endpoint the orchestrator calls.
4. **Proptech Recommender (Next.js):** A standalone fullstack service matching/recommending properties based on incoming listing or sensor data. Includes its own API routes and a small browsing UI, independent of the main dashboard.
5. **Event Store (Postgres):** Durable, queryable history of every processed event — what the original design lacked entirely. Powers the dashboard's historical views; the live pipeline (Pub/Sub → WebSocket) remains unaffected by its presence.
6. **Notification Engine (TypeScript):** Subscribes to the processed-event Pub/Sub channel and broadcasts real-time alerts via WebSockets. Unchanged in role from the original design.
7. **Dashboard (React):** The primary fullstack showcase surface — a WebSocket client for live updates, a REST/GraphQL client against the event store for historical views and filtering, and real UI (charts, tables, filters).
