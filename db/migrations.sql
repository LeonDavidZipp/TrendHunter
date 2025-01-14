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

CREATE TABLE IF NOT EXIST "tokens" (
    "cmc_id" BIGSERIAL PRIMARY KEY,
    "name" VARCHAR NOT NULL,
    "symbol" VARCHAR NOT NULL,
    "address" VARCHAR NOT NULL,
    "last_checked" TIMESTAMPTZ NOT NULL DEFAULT(NOW()),
);

CREATE INDEX ON "observations" ("cmc_id");
CREATE INDEX ON "observations" ("symbol");

CREATE TABLE IF NOT EXIST "token_time_series" (
    "id" BIGSERIAL PRIMARY KEY,
    "timestamp" TIMESTAMPTZ NOT NULL,
    "price": usd_quote["price"],
    "currency": VARCHAR NOT NULL DEFAULT("USD"),
    "volume_24h": BIGINT,
    "market_cap": BIGINT,
    "circulating_supply": BIGINT,
    "total_supply": BIGINT
);

CREATE TABLE "tweets" (
    "id" BIGSERIAL PRIMARY KEY,
    "created_at" TIMESTAMPTZ,
    "date" TIMESTAMPTZ,
    "timezone" VARCHAR,
    "tweet" TEXT,
    "language" VARCHAR,
    "hashtags" TEXT[],
    "cashtags" TEXT[],
    "user_id" BIGINT,
    "user_id_str" VARCHAR,
    "username" VARCHAR,
    "name" VARCHAR,
    "day" INTEGER,
    "hour" INTEGER,
    "retweet" BOOLEAN,
    "nlikes" INTEGER,
    "nreplies" INTEGER,
    "nretweets" INTEGER,
    "quote_url" TEXT,
    "search" TEXT,
    "near" VARCHAR,
    "source" VARCHAR,
    "user_rt_id" BIGINT,
    "user_rt" VARCHAR,
    "retweet_id" BIGINT,
    "reply_to" TEXT[],
    "retweet_date" TIMESTAMPTZ,
);

CREATE INDEX ON "tweets" ("date");
CREATE INDEX ON "tweets" ("id");
