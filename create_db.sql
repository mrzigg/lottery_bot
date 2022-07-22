/* Структура базы данных */

create table rate_plans (
    id                  smallserial             not null primary key,
    name                character varying(16)   not null unique,
    cost                money                   not null,
    draws_limit         smallint
);

insert into rate_plans (
    name,
    cost,
    draws_limit
) values (
    'Пробный',
    50,
    1
), (
    'Безлимит',
    250,
    null
);

create table customers (
    id                  serial                  not null primary key,
    email_address       character varying(256)  not null unique,
    password_hash       bytea                   not null,
    verified            boolean                 default false not null,
    rate_plan_id        smallint,
    draws_count         smallint                default 0 not null
);

create table bots (
    customer_id         integer                 not null references customers on delete cascade,
    id                  integer                 not null,
    token               character varying(64)   not null unique,
    username            character varying(32)   not null unique,
    first_name          character varying(64)   not null,
    primary key (customer_id, id)
);

create function bots_id_seq() returns trigger as $bots_id_seq$
    begin
        if new.id is null then
            new.id := (select
                coalesce(max(id) + 1, 1)
            from
                bots
            where
                customer_id = new.customer_id);
        end if;
        return new;
    end;
$bots_id_seq$ language plpgsql;

create trigger bots_id_seq before insert on bots
    for each row execute procedure bots_id_seq();

create function bots_bot_substitution() returns trigger as $bots_bot_substitution$
    begin
        if new.username <> old.username then
            raise exception 'BotSubstitution';
        end if;
        return new;
    end;
$bots_bot_substitution$ language plpgsql;

create trigger bots_bot_substitution before update on bots
    for each row execute procedure bots_bot_substitution();

create type age_range as enum (
    'до 18',
    '18-24',
    '25-34',
    '35-44',
    '45+'
);

create type country as enum (
    'Беларусь',
    'Казахстан',
    'Россия',
    'Узбекистан',
    'Украина'
);

create table tg_users (
    customer_id         integer                 not null,
    bot_id              integer                 not null,
    id                  bigint                  not null,
    init_timestamp      timestamp               default current_timestamp not null,
    ref_tg_user_id      bigint,
    is_male             boolean,
    age_range           age_range,
    country             country,
    button              boolean                 default false not null,
    button_2            boolean                 default false not null,
    primary key (customer_id, bot_id, id),
    foreign key (customer_id, bot_id) references bots(customer_id, id) on delete cascade
);

create table raffles (
    customer_id         integer                 not null,
    bot_id              integer                 not null,
    id                  integer                 not null,
    prizes              character varying(64)[] not null,
    description         character varying(1024) not null,
    sponsors            character varying(32)[] not null,
    begin_timestamp     timestamp               not null,
    end_timestamp       timestamp               not null,
    header              character varying(128)  not null,
    countries           country[]               not null,
    phone_number        character varying(16)   not null,
    tg_username         character varying(32)   not null,
    primary key (customer_id, bot_id, id),
    foreign key (customer_id, bot_id) references bots(customer_id, id) on delete cascade
);

create function raffles_id_seq() returns trigger as $raffles_id_seq$
    declare draws_count integer := (select
        draws_count
    from
        customers
    where
        id = new.customer_id);
    declare rate_plan_id smallint := (select
        rate_plan_id
    from
        customers
    where
        id = new.customer_id);
    declare draws_limit smallint := (select
        draws_limit
    from
        rate_plans
    where
        id = rate_plan_id);
    begin
        if rate_plan_id is null then
            raise exception 'RatePlanUnset';
        end if;
        if draws_count >= draws_limit then
            raise exception 'DrawsLimitReached';
        end if;
        if new.id is null then
            new.id := (select
                coalesce(max(id) + 1, 1)
            from
                raffles
            where
                customer_id = new.customer_id and
                bot_id = new.bot_id);
        end if;
        return new;
    end;
$raffles_id_seq$ language plpgsql;

create trigger raffles_id_seq before insert on raffles
    for each row execute procedure raffles_id_seq();

create function raffles_timestamp_range_intersection() returns trigger as $raffles_timestamp_range_intersection$
    declare other record;
    begin
        for other in
            (select
                begin_timestamp,
                end_timestamp
            from
                raffles
            where
                customer_id = new.customer_id and
                bot_id = new.bot_id and
                id <> new.id)
        loop
            if new.begin_timestamp < other.end_timestamp and (
                other.begin_timestamp <= new.begin_timestamp or
                other.end_timestamp <= new.end_timestamp
            ) or other.begin_timestamp < new.end_timestamp and (
                new.begin_timestamp <= other.begin_timestamp or
                new.end_timestamp <= other.end_timestamp
            ) then
                raise exception 'TimestampRangeIntersection';
            end if;
        end loop;
        return new;
    end;
$raffles_timestamp_range_intersection$ language plpgsql;

create trigger raffles_timestamp_range_intersection before insert or update on raffles
    for each row execute procedure raffles_timestamp_range_intersection();

create function raffles_update_too_late() returns trigger as $raffles_update_too_late$
    begin
        if current_timestamp >= old.begin_timestamp then
            raise exception 'UpdateTooLate';
        end if;
        return new;
    end;
$raffles_update_too_late$ language plpgsql;

create trigger raffles_update_too_late before update on raffles
    for each row execute procedure raffles_update_too_late();

create function raffles_count_increment() returns trigger as $raffles_count_increment$
    begin
        update
            customers
        set
            draws_count = draws_count + 1
        where
            id = new.customer_id;
        return new;
    end;
$raffles_count_increment$ language plpgsql;

create trigger raffles_count_increment after insert on raffles
    for each row execute procedure raffles_count_increment();

create function raffles_return_removed_raffle() returns trigger as $raffles_return_removed_raffle$
    begin
        if old.begin_timestamp > current_timestamp then
            update
                customers
            set
                draws_count = draws_count - 1
            where
                id = old.customer_id;
        end if;
        return null;
    end;
$raffles_return_removed_raffle$ language plpgsql;

create trigger raffles_return_removed_raffle after delete on raffles
    for each row execute procedure raffles_return_removed_raffle();

create table tickets (
    customer_id         integer                 not null,
    bot_id              integer                 not null,
    raffle_id           integer                 not null,
    id                  bigint                  not null, -- номер билета
    tg_user_id          bigint                  not null,
    primary key (customer_id, bot_id, raffle_id, id),
    foreign key (customer_id, bot_id, raffle_id) references raffles(customer_id, bot_id, id) on delete cascade
);

create function tickets_id_seq() returns trigger as $$
    begin
        if new.id is null then
            new.id := (select
                coalesce(max(id) + 1, 1)
            from
                tickets
            where
                customer_id = new.customer_id and
                bot_id = new.bot_id and
                raffle_id - new.raffle_id);
        end if;
        return new;
    end;
$$ language plpgsql;

create trigger tickets_id_seq before insert on tickets
    for each row execute procedure tickets_id_seq();

create table raffle_progresses (
    customer_id             integer                 not null,
    bot_id                  integer                 not null,
    raffle_id               integer                 not null,
    tg_user_id              bigint                  not null,
    latest_daily            date                    default current_date not null,
    daily_bonus_duration    smallint                default 1 not null,
    super_game_duration     smallint                default 0 not null,
    super_game_stage        smallint                default 0 not null,
    invites                 smallint                default 0 not null,
    super_game_invites      smallint                default 0 not null,
    primary key (customer_id, bot_id, raffle_id, tg_user_id),
    foreign key (customer_id, bot_id, tg_user_id) references tg_users(customer_id, bot_id, id) on delete cascade
);

create function super_game_to_invite(super_game_duration smallint, super_game_stage smallint) returns smallint as $$
    declare to_invite smallint := case
        when super_game_stage = 1 then super_game_duration
        when super_game_stage = 2 then 1
        else super_game_duration * 2 ^ (super_game_stage - 2)
    end;
    begin
        return to_invite;
    end;
$$ language plpgsql;

create view raffle_progresses_extends as
    select
        *,
        super_game_to_invite(super_game_duration, super_game_stage)
    from raffle_progresses;

create function raffle_progresses_latest_daily_update() returns trigger as $raffle_progresses_latest_daily_update$
    declare interval smallint;
    begin
        new.latest_daily := current_date;
        interval := new.latest_daily - old.latest_daily;
        if interval > 0 then
            new.super_game_stage := 0;
            new.super_game_invites := 0;
        end if;
        if interval > 1 then
            new.daily_bonus_duration := 1;
        end if;
        return new;
    end;
$raffle_progresses_latest_daily_update$ language plpgsql;

create trigger raffle_progresses_latest_daily_update before update on raffle_progresses
    for each row execute procedure raffle_progresses_latest_daily_update();

/* Возможно, не стоит использовать OLD */
create function raffle_progresses_give_super_game_bonus() returns trigger as $$
    declare to_invite smallint := super_game_to_invite(old.super_game_duration, old.super_game_stage);
    declare tickets_number smallint := old.super_game_duration * 10 * 2 ^ (super_game_stage - 1);
    begin
        if new.super_game_invites >= to_invite then
            for i in 1..tickets_number loop
                insert into tickets (
                    customer_id,
                    bot_id,
                    raffle_id,
                    tg_user_id
                ) values (
                    new.customer_id,
                    new.bot_id,
                    new.raffle_id,
                    new.tg_user_id
                );
            end loop;
        end if;
        return new;
    end;
$$ language plpgsql;

create trigger raffle_progresses_give_super_game_bonus before update on raffle_progresses
    for each row execute procedure raffle_progresses_give_super_game_bonus();
