CREATE TABLE request
(
    id           SERIAL PRIMARY KEY,
    rq_body_hash VARCHAR UNIQUE NOT NULL,
    rq_body      JSONB          NOT NULL,
    duplicates   BIGINT         NOT NULL
);