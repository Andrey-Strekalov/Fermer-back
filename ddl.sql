-- =============================================================
-- DDL for Fermer-back (PostgreSQL)
-- Generated from Django models and migrations
-- =============================================================

-- ----------------------------
-- Django system tables
-- ----------------------------

CREATE TABLE django_migrations (
    id          BIGSERIAL    PRIMARY KEY,
    app         VARCHAR(255) NOT NULL,
    name        VARCHAR(255) NOT NULL,
    applied     TIMESTAMPTZ  NOT NULL
);

CREATE TABLE django_content_type (
    id        SERIAL       PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model     VARCHAR(100) NOT NULL,
    CONSTRAINT django_content_type_app_label_model_uniq UNIQUE (app_label, model)
);

CREATE TABLE auth_permission (
    id              SERIAL       PRIMARY KEY,
    name            VARCHAR(255) NOT NULL,
    content_type_id INTEGER      NOT NULL REFERENCES django_content_type (id) ON DELETE CASCADE,
    codename        VARCHAR(100) NOT NULL,
    CONSTRAINT auth_permission_content_type_id_codename_uniq UNIQUE (content_type_id, codename)
);

CREATE TABLE auth_group (
    id   SERIAL       PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE auth_group_permissions (
    id            BIGSERIAL PRIMARY KEY,
    group_id      INTEGER   NOT NULL REFERENCES auth_group (id) ON DELETE CASCADE,
    permission_id INTEGER   NOT NULL REFERENCES auth_permission (id) ON DELETE CASCADE,
    CONSTRAINT auth_group_permissions_group_id_permission_id_uniq UNIQUE (group_id, permission_id)
);

-- ----------------------------
-- users_user
-- ----------------------------

CREATE TABLE users_user (
    id           BIGSERIAL    PRIMARY KEY,
    password     VARCHAR(128) NOT NULL,
    last_login   TIMESTAMPTZ,
    is_superuser BOOLEAN      NOT NULL DEFAULT FALSE,
    first_name   VARCHAR(150) NOT NULL DEFAULT '',
    last_name    VARCHAR(150) NOT NULL DEFAULT '',
    email        VARCHAR(254) NOT NULL DEFAULT '',
    is_staff     BOOLEAN      NOT NULL DEFAULT FALSE,
    is_active    BOOLEAN      NOT NULL DEFAULT TRUE,
    date_joined  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    phone_number VARCHAR(20)  NOT NULL UNIQUE,
    role         VARCHAR(20)  NOT NULL DEFAULT 'farmer',
    company_logo VARCHAR(100)                          -- ImageField stores relative file path
);

CREATE TABLE users_user_groups (
    id       BIGSERIAL PRIMARY KEY,
    user_id  BIGINT    NOT NULL REFERENCES users_user (id) ON DELETE CASCADE,
    group_id INTEGER   NOT NULL REFERENCES auth_group (id) ON DELETE CASCADE,
    CONSTRAINT users_user_groups_user_id_group_id_uniq UNIQUE (user_id, group_id)
);

CREATE TABLE users_user_user_permissions (
    id            BIGSERIAL PRIMARY KEY,
    user_id       BIGINT    NOT NULL REFERENCES users_user (id) ON DELETE CASCADE,
    permission_id INTEGER   NOT NULL REFERENCES auth_permission (id) ON DELETE CASCADE,
    CONSTRAINT users_user_user_permissions_user_id_permission_id_uniq UNIQUE (user_id, permission_id)
);

-- ----------------------------
-- users_requisites
-- ----------------------------

CREATE TABLE users_requisites (
    id                   BIGSERIAL    PRIMARY KEY,
    user_id              BIGINT       NOT NULL UNIQUE REFERENCES users_user (id) ON DELETE CASCADE,
    company_name         VARCHAR(255) NOT NULL DEFAULT '',
    legal_address        TEXT         NOT NULL DEFAULT '',
    inn                  VARCHAR(12)  NOT NULL DEFAULT '',
    ogrn                 VARCHAR(15)  NOT NULL DEFAULT '',
    bik                  VARCHAR(9)   NOT NULL DEFAULT '',
    bank_name            VARCHAR(255) NOT NULL DEFAULT '',
    checking_account     VARCHAR(20)  NOT NULL DEFAULT '',
    correspondent_account VARCHAR(20) NOT NULL DEFAULT '',
    phone                VARCHAR(20)  NOT NULL DEFAULT '',
    fax                  VARCHAR(20)  NOT NULL DEFAULT '',
    email                VARCHAR(254) NOT NULL DEFAULT ''
);

-- ----------------------------
-- users_phoneotp
-- ----------------------------

CREATE TABLE users_phoneotp (
    id           BIGSERIAL   PRIMARY KEY,
    phone_number VARCHAR(20) NOT NULL,
    code         VARCHAR(6)  NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    is_used      BOOLEAN     NOT NULL DEFAULT FALSE
);

-- ----------------------------
-- bids_bid
-- ----------------------------

CREATE TABLE bids_bid (
    id           BIGSERIAL        PRIMARY KEY,
    author_id    BIGINT           NOT NULL REFERENCES users_user (id) ON DELETE CASCADE,
    type         VARCHAR(4)       NOT NULL CHECK (type IN ('buy', 'sell')),
    title        VARCHAR(255)     NOT NULL,
    quality      VARCHAR(255)     NOT NULL DEFAULT '',
    price        NUMERIC(12, 2)   NOT NULL,
    volume       NUMERIC(12, 3)   NOT NULL,
    region       VARCHAR(255)     NOT NULL,
    comment      TEXT             NOT NULL DEFAULT '',
    is_archived  BOOLEAN          NOT NULL DEFAULT FALSE,
    published_at TIMESTAMPTZ,
    created_at   TIMESTAMPTZ      NOT NULL DEFAULT NOW()
);

CREATE INDEX bids_bid_author_id_idx     ON bids_bid (author_id);
CREATE INDEX bids_bid_published_at_idx  ON bids_bid (published_at DESC NULLS LAST, id DESC);

-- ----------------------------
-- contacts_contactrequest
-- ----------------------------

CREATE TABLE contacts_contactrequest (
    id                          BIGSERIAL    PRIMARY KEY,
    bid_id                      BIGINT       NOT NULL REFERENCES bids_bid (id) ON DELETE CASCADE,
    sender_id                   BIGINT       NOT NULL REFERENCES users_user (id) ON DELETE CASCADE,
    receiver_id                 BIGINT       NOT NULL REFERENCES users_user (id) ON DELETE CASCADE,
    comment                     TEXT         NOT NULL DEFAULT '',
    sender_phone_snapshot       VARCHAR(20)  NOT NULL,
    sender_organization_snapshot VARCHAR(255) NOT NULL DEFAULT '',
    is_read                     BOOLEAN      NOT NULL DEFAULT FALSE,
    created_at                  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    updated_at                  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
    CONSTRAINT unique_contact_request_per_bid_sender UNIQUE (bid_id, sender_id)
);

CREATE INDEX contacts_co_receive_9f172a_idx ON contacts_contactrequest (receiver_id, is_read, created_at DESC);
CREATE INDEX contacts_co_sender__03bc94_idx ON contacts_contactrequest (sender_id, created_at DESC);
CREATE INDEX contacts_co_bid_id_6a06a8_idx  ON contacts_contactrequest (bid_id);

-- ----------------------------
-- notifications_notification
-- ----------------------------

CREATE TABLE notifications_notification (
    id                 BIGSERIAL   PRIMARY KEY,
    recipient_id       BIGINT      NOT NULL REFERENCES users_user (id) ON DELETE CASCADE,
    type               VARCHAR(32) NOT NULL CHECK (type IN ('contact_request_created')),
    contact_request_id BIGINT      REFERENCES contacts_contactrequest (id) ON DELETE CASCADE,
    payload            JSONB,
    is_read            BOOLEAN     NOT NULL DEFAULT FALSE,
    created_at         TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX notificatio_recipie_684eac_idx ON notifications_notification (recipient_id, is_read, created_at DESC);

-- ----------------------------
-- Django admin & session
-- ----------------------------

CREATE TABLE django_admin_log (
    id              SERIAL       PRIMARY KEY,
    action_time     TIMESTAMPTZ  NOT NULL,
    object_id       TEXT,
    object_repr     VARCHAR(200) NOT NULL,
    action_flag     SMALLINT     NOT NULL CHECK (action_flag > 0),
    change_message  TEXT         NOT NULL,
    content_type_id INTEGER      REFERENCES django_content_type (id) ON DELETE SET NULL,
    user_id         BIGINT       NOT NULL REFERENCES users_user (id) ON DELETE CASCADE
);

CREATE TABLE django_session (
    session_key  VARCHAR(40)  PRIMARY KEY,
    session_data TEXT         NOT NULL,
    expire_date  TIMESTAMPTZ  NOT NULL
);

CREATE INDEX django_session_expire_date_idx ON django_session (expire_date);
