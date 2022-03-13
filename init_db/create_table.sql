CREATE TABLE request
(
    id           SERIAL PRIMARY KEY,
    rq_body_hash VARCHAR,
    rq_body      JSONB,
    created_at   timestamp with time zone,
    modified_at  timestamp with time zone
);

CREATE INDEX body_hash_idx ON request (rq_body_hash);