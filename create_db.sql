/* Создание таблиц перед запуском приложения */

CREATE TABLE rate_plans (
    id                  smallserial             not null primary key,
    name                character varying(16)   not null unique,
    cost                money                   not null,
    draws_limit         smallint
);

INSERT INTO rate_plans (
    name,
    cost,
    draws_limit
) VALUES (
    'Пробный',
    50,
    1
), (
    'Безлимит',
    250,
    NULL
);

CREATE TABLE customers (
    id                  serial                  not null primary key,
    email_address       character varying(256)  not null unique,
    phone_number        character varying(16)   not null,
    password_hash       bytea                   not null,
    verified            boolean                 default false not null,
    rate_plan_id        smallint
);

CREATE TABLE bots (
    customer_id         integer                 not null references customers on delete cascade,
    id                  integer                 not null,
    token               character varying(64)   not null unique,
    username            character varying(32)   not null unique,
    first_name          character varying(64)   not null,
    primary key (customer_id, id)
);

CREATE FUNCTION bots_id_seq() RETURNS trigger AS $bots_id_seq$
    BEGIN
        IF NEW.id IS null THEN
            NEW.id := (SELECT
                coalesce(max(id) + 1, 1)
            FROM
                bots
            WHERE
                customer_id = NEW.customer_id);
        END IF;
        RETURN NEW;
    END;
$bots_id_seq$ LANGUAGE plpgsql;

CREATE TRIGGER bots_id_seq BEFORE INSERT ON bots
    FOR EACH ROW EXECUTE PROCEDURE bots_id_seq();

CREATE TYPE age_range AS enum (
    'до 18',
    '18-24',
    '25-34',
    '35-44',
    '45+'
);

CREATE TYPE country AS enum (
    '🇧🇾 ',
    '🇰🇿',
    '🇷🇺',
    '🇺🇿',
    '🇺🇦',
    'Any'
);

CREATE TABLE tg_users (
    customer_id         integer                 not null,
    bot_id              integer                 not null,
    id                  bigint                  not null,
    init_timestamp      timestamp               default current_timestamp not null,
    ref_tg_user_id      bigint,
    is_male             boolean,
    "age_range"         age_range,
    country             country,
    button              boolean                 default false not null,
    button2             boolean                 default false not null,
    primary key (customer_id, bot_id, id),
    foreign key (customer_id, bot_id) references bots(customer_id, id) on delete cascade
);

CREATE TABLE raffles (
    customer_id         integer                 not null,
    bot_id              integer                 not null,
    id                  integer                 not null,
    prize               character varying(64)   not null,
    description         character varying(1024) not null,
    sponsors            character varying(32)[] not null,
    begin_timestamp     timestamp               not null,
    end_timestamp       timestamp               not null,
    header              character varying(128)  not null,
    primary key (customer_id, bot_id, id),
    foreign key (customer_id, bot_id) references bots(customer_id, id) on delete cascade
);

CREATE FUNCTION raffles_id_seq() RETURNS trigger AS $raffles_id_seq$
    DECLARE raffles_count integer := (SELECT
        coalesce(count(*), 0)
    FROM
        raffles
    WHERE
        customer_id = NEW.customer_id);
    DECLARE rate_plan_id smallint := (SELECT
        rate_plan_id
    FROM
        customers
    WHERE
        id = NEW.customer_id);
    DECLARE draws_limit smallint := (SELECT
        draws_limit
    FROM
        rate_plans
    WHERE
        id = rate_plan_id);
    BEGIN
        IF rate_plan_id IS null THEN
            RAISE EXCEPTION 'RatePlanUnset';
        END IF;
        IF raffles_count >= draws_limit THEN
            RAISE EXCEPTION 'DrawsLimitReached';
        END IF;
        raffles_count := (SELECT
            coalesce(count(*), 0)
        FROM
            raffles
        WHERE
            customer_id = NEW.customer_id);
        IF NEW.id IS null THEN
            NEW.id := (SELECT
                coalesce(max(id) + 1, 1)
            FROM
                raffles
            WHERE
                customer_id = NEW.customer_id AND
                bot_id = NEW.bot_id);
        END IF;
        RETURN NEW;
    END;
$raffles_id_seq$ LANGUAGE plpgsql;

CREATE TRIGGER raffles_id_seq BEFORE INSERT ON raffles
    FOR EACH ROW EXECUTE PROCEDURE raffles_id_seq();

CREATE TABLE tickets (
    customer_id         integer                 not null,
    bot_id              integer                 not null,
    raffle_id           integer                 not null,
    id                  integer                 not null,
    owner_tg_user_id    bigint                  not null,
    issue_timestamp     timestamp               default current_timestamp not null,
    tickets             bigint[]                default '{}'::bigint[] not null,
    invites             smallint                default 0 not null,
    primary key (customer_id, bot_id, raffle_id, id),
    foreign key (customer_id, bot_id, raffle_id) references raffles(customer_id, bot_id, id) on delete cascade
);
