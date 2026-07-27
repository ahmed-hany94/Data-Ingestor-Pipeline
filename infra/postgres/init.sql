CREATE TABLE IF NOT EXISTS events (
    id            BIGSERIAL PRIMARY KEY,
    domain        TEXT NOT NULL,
    payload       JSONB NOT NULL,
    result_ok     BOOLEAN NOT NULL,
    result_data   JSONB NOT NULL,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_events_domain ON events (domain);
CREATE INDEX IF NOT EXISTS idx_events_created_at ON events (created_at DESC);