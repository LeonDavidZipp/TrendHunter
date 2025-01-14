GRANT ALL PRIVILEGES ON SCHEMA public TO "app_user";

CREATE TYPE SOURCETYPE AS ENUM (
    'twitter', 'reddit', 'telegram',
    'discord', 'tiktok', 'github', 'onchain',
    'farcaster', 'lenster'
);

CREATE TABLE IF NOT EXISTS "sources" (
    "id" BIGSERIAL PRIMARY KEY,
    "name" VARCHAR NOT NULL,
    "type" VARCHAR NOT NULL,
    "num_observations" INTEGER NOT NULL DEFAULT 0,
    "last_checked" TIMESTAMPTZ NOT NULL DEFAULT (NOW()),
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT (NOW())
);

CREATE INDEX ON "sources" ("id");
CREATE INDEX ON "sources" ("name");

CREATE TABLE IF NOT EXISTS "observations" (
    "id" BIGSERIAL PRIMARY KEY,
    "date" TIMESTAMPTZ NOT NULL,
    "source" VARCHAR NOT NULL,
    "source_type" VARCHAR NOT NULL,
    "action" INTEGER NOT NULL,
    "token" VARCHAR NOT NULL,
    "token_address" VARCHAR NOT NULL,
    "price" NUMERIC NOT NULL
);

CREATE INDEX ON "observations" ("id");
CREATE INDEX ON "observations" ("date");
CREATE INDEX ON "observations" ("token");
