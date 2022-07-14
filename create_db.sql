/* Создание таблиц перед запуском приложения */


CREATE TABLE IF NOT EXISTS servers
(
    id smallint NOT NULL DEFAULT nextval('servers_id_seq'::regclass),
    ip_addr inet NOT NULL,
    CONSTRAINT servers_pkey PRIMARY KEY (id),
    CONSTRAINT servers_ip_addr_key UNIQUE (ip_addr)
);


CREATE TABLE IF NOT EXISTS public.customers
(
    id integer NOT NULL DEFAULT nextval('customers_id_seq'::regclass),
    email_addr character varying(256) COLLATE pg_catalog."default" NOT NULL,
    verified boolean NOT NULL DEFAULT false,
    password_hash bytea NOT NULL,
    phone_number character varying(16) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT customers_pkey PRIMARY KEY (id),
    CONSTRAINT customers_email_addr_key UNIQUE (email_addr)
);


CREATE TABLE IF NOT EXISTS public.bots
(
    customer_id integer NOT NULL,
    id integer NOT NULL,
    api_token character varying(64) COLLATE pg_catalog."default" NOT NULL,
    server_id smallint,
    CONSTRAINT bots_pkey PRIMARY KEY (customer_id, id),
    CONSTRAINT bots_api_token_key UNIQUE (api_token),
    CONSTRAINT bots_customer_id_fkey FOREIGN KEY (customer_id)
        REFERENCES public.customers (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT bots_server_id_fkey FOREIGN KEY (server_id)
        REFERENCES public.servers (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);


CREATE TYPE age_range AS enum (
    'до 18',
    '18-24',
    '25-34',
    '35-44',
    '45+'
);


CREATE TABLE IF NOT EXISTS public.tg_users
(
    customer_id integer NOT NULL,
    bot_id integer NOT NULL,
    id bigint NOT NULL,
    init_timestamp timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ref_tg_user_id bigint,
    is_male boolean,
    age_range age_range,
    country character varying(64) COLLATE pg_catalog."default",
    button boolean,
    CONSTRAINT tg_users_pkey PRIMARY KEY (customer_id, bot_id, id),
    CONSTRAINT tg_users_customer_id_bot_id_fkey FOREIGN KEY (bot_id, customer_id)
        REFERENCES public.bots (id, customer_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS public.raffles
(
    customer_id integer NOT NULL,
    bot_id integer NOT NULL,
    id integer NOT NULL,
    prize character varying(64) COLLATE pg_catalog."default" NOT NULL,
    description character varying(1024) COLLATE pg_catalog."default" NOT NULL,
    sponsors bigint[] NOT NULL,
    begin_timestamp timestamp without time zone NOT NULL,
    end_timestamp timestamp without time zone NOT NULL,
    photo text COLLATE pg_catalog."default" NOT NULL,
    header character varying(128) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT raffles_pkey PRIMARY KEY (customer_id, bot_id, id),
    CONSTRAINT raffles_customer_id_bot_id_fkey FOREIGN KEY (bot_id, customer_id)
        REFERENCES public.bots (id, customer_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS public.tickets
(
    customer_id integer NOT NULL,
    bot_id integer NOT NULL,
    raffle_id integer NOT NULL,
    id integer NOT NULL,
    owner_tg_user_id bigint NOT NULL,
    issue_timestamp timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tickets bigint[] COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT tickets_pkey PRIMARY KEY (customer_id, bot_id, raffle_id, id),
    CONSTRAINT tickets_customer_id_bot_id_raffle_id_fkey FOREIGN KEY (bot_id, customer_id, raffle_id)
        REFERENCES public.raffles (bot_id, customer_id, id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);