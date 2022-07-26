create table rate_plans (
    id                  smallserial             not null,
    name                character varying(16)   not null,
    cost                money                   not null,
    draws_limit         smallint,
    constraint rate_plans_pkey primary key (id),
    constraint rate_plans_name_key unique (name)
);
comment on table rate_plans is 'Предназначена для хранения тарифных планов.';
comment on column rate_plans.id is 'Уникальный идентификатор тарифного плана.';
comment on column rate_plans.name is 'Название тарифного плана.';
comment on column rate_plans.cost is 'Стоимость в местной валюте.';
comment on column rate_plans.draws_limit is 'Максимальное количество розыгрышей. <code>null</code> обозначает отсутствие ограничений.';
comment on constraint rate_plans_pkey on rate_plans is 'Первичный ключ.';
comment on constraint rate_plans_name_key on rate_plans is 'Уникальный ключ по названию тарифа.';

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
    id                  serial                  not null,
    email_address       character varying(256)  not null,
    password_hash       bytea                   not null,
    verified            boolean                 default false not null,
    rate_plan_id        smallint,
    draws_count         smallint                default 0 not null,
    constraint customers_pkey primary key (id),
    constraint customers_email_address_key unique (email_address)
);
comment on table customers is 'Предназначена для хранения пользователей.';
comment on column customers.id is 'Уникальный идентификатор пользователя.';
comment on column customers.email_address is 'E-mail адрес пользователя.';
comment on column customers.password_hash is 'Хеш пароля по алгоритму SHA3-512.';
comment on column customers.verified is 'Пользователь прошёл верификацию по e-mail, телефону или вручную.';
comment on column customers.rate_plan_id is 'Уникальный идентификатор текущего тарифного плана.';
comment on column customers.draws_count is 'Количество ликвидных розыгрышей. Подразумевается сумма количества успешно проведённых розыгрышей, проводимых в данный момент, а также запланированных на будущее.';
comment on constraint customers_pkey on customers is 'Первичный ключ.';
comment on constraint customers_email_address_key on customers is 'Уникальный ключ по e-mail адресу пользователя.';

create table bots (
    customer_id         integer                 not null,
    id                  integer                 not null,
    token               character varying(64)   not null,
    username            character varying(32)   not null,
    first_name          character varying(64)   not null,
    constraint bots_pkey primary key (customer_id, id),
    constraint bots_token_key unique (token),
    constraint bots_username_key unique (username),
    constraint bots_customers_fkey foreign key (customer_id) references customers on delete cascade
);
comment on table bots is 'Предназначена для хранения ботов.';
comment on column bots.customer_id is 'Уникальный идентификатор владельца бота.';
comment on column bots.id is 'Уникальный идентификатор бота. Подразумевается локальный идентификатор, а не предоставленный Телеграм.';
comment on column bots.token is 'API-токен бота, предоставленный пользователем.';
comment on column bots.username is 'Псевдоним бота, предоставленный Телеграм.';
comment on column bots.first_name is 'Имя бота, предоставленное Телеграм.';
comment on constraint bots_pkey on bots is 'Составной первичный ключ.';
comment on constraint bots_token_key on bots is 'Уникальный ключ по API-токену бота.';
comment on constraint bots_username_key on bots is 'Уникальный ключ по псевдониму бота.';
comment on constraint bots_customers_fkey on bots is 'Внешний ключ на таблицу <code>customers</code>.';

create function bots_id_seq() returns trigger as $$
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
$$ language plpgsql;
comment on function bots_id_seq() is 'Предназначена для одноимённого триггера. Генерирует уникальное значение для столбца <code>id</code>.';

create trigger bots_id_seq before insert on bots
    for each row execute procedure bots_id_seq();
comment on trigger bots_id_seq on bots is 'Выполняет одноимённую функцию перед каждой вставкой.';

create function bots_bot_substitution() returns trigger as $$
    begin
        if new.username <> old.username then
            raise exception 'BotSubstitution';
        end if;
        return new;
    end;
$$ language plpgsql;
comment on function bots_bot_substitution() is 'Предназначена для одноимённого триггера. Выполняет проверку того, был подменён бот на другого или нет, путём сравнения старого и нового псевдонимов бота. Выбрасывает исключение в случае подмены бота.';

create trigger bots_bot_substitution before update on bots
    for each row execute procedure bots_bot_substitution();
comment on trigger bots_bot_substitution on bots is 'Выполняет одноимённую функцию перед каждым обновлением.';

create type age_range as enum (
    'до 18',
    '18-24',
    '25-34',
    '35-44',
    '45+'
);
comment on type age_range is 'Определяет множество доступных возрастных диапазонов.';

create type country as enum (
    'Беларусь',
    'Казахстан',
    'Россия',
    'Узбекистан',
    'Украина'
);
comment on type country is 'Определяет множество доступных стран.';

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
    constraint tg_users_pkey primary key (customer_id, bot_id, id),
    constraint tg_users_bots_fkey foreign key (customer_id, bot_id) references bots(customer_id, id) on delete cascade
);
comment on table tg_users is 'Предназначена для хранения пользователей Телеграм, участвующих в розыгрышах.';
comment on column tg_users.customer_id is 'Уникальный идентификатор владельца бота.';
comment on column tg_users.bot_id is 'Уникальный идентификатор бота.';
comment on column tg_users.id is 'Уникальный идентификатор пользователя Телеграм. Подразумевается идентификатор, предоставленный Телеграм.';
comment on column tg_users.init_timestamp is 'Дата и время добавления пользователя.';
comment on column tg_users.ref_tg_user_id is 'Уникальный идентификатор пользователя, пригласившего данного пользователя. <b>Возможно, столбец лишний и нуждается в удалении.</b>';
comment on column tg_users.is_male is 'Пользователь является мужчиной.';
comment on column tg_users.age_range is 'Возрастной диапазон пользователя.';
comment on column tg_users.country is 'Страна пользователя. <code>null</code> может значить не только отсутствие значения, но и то, что страны пользователя нет в списке.';
comment on column tg_users.button is 'Пользователь нажал на кнопку «Начать». <b>По названию столбца неясно для чего он предназначен.</b>';
comment on column tg_users.button_2 is 'Пользователь нажал на кнопку «Я в деле». <b>По названию столбца неясно для чего он предназначен.</b>';
comment on constraint tg_users_pkey on tg_users is 'Составной первичный ключ.';
comment on constraint tg_users_bots_fkey on tg_users is 'Составной внешний ключ на таблицу <code>bots</code>.';

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
    constraint raffles_pkey primary key (customer_id, bot_id, id),
    constraint raffles_bots_fkey foreign key (customer_id, bot_id) references bots(customer_id, id) on delete cascade
);
comment on table raffles is 'Предназначена для хранения розыгрышей.';
comment on column raffles.customer_id is 'Уникальный идентификатор владельца бота.';
comment on column raffles.bot_id is 'Уникальный идентификатор бота, для которого предназначен данный розыгрыш.';
comment on column raffles.id is 'Уникальный идентификатор розыгрыша.';
comment on column raffles.prizes is 'Список названий призов. Первый элемент обозначает название приза за первое место, последний — за последнее.';
comment on column raffles.description is 'Описание розыгрыша.';
comment on column raffles.sponsors is 'Список псевдонимов пользователей Телеграм, являющихся спонсорами розыгрыша.';
comment on column raffles.begin_timestamp is 'Дата и время начала розыгрыша.';
comment on column raffles.end_timestamp is 'Дата и время окончания розыгрыша.';
comment on column raffles.header is 'Название розыгрыша.';
comment on column raffles.countries is 'Список стран, граждане которых могут участвовать в розыгрыше.';
comment on column raffles.phone_number is 'Контактный номер телефона лица, ответственного за проведение розыгрыша.';
comment on column raffles.tg_username is 'Псевдоним пользователя Телеграм, ответственного за проведение розыгрыша.';
comment on constraint raffles_pkey on raffles is 'Составной первичный ключ.';
comment on constraint raffles_bots_fkey on raffles is 'Составной внешний ключ на таблицу <code>bots</code>.';

create function raffles_id_seq() returns trigger as $$
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
$$ language plpgsql;
comment on function raffles_id_seq() is 'Предназначена для одноимённого триггера. Проверяет ограничения пользователя по выбранному тарифному плану. Генерирует уникальное значение для столбца <code>id</code>. Выбрасывает исключение, если тарифный план не установлен или установлен, но превышены ограничения по нему.';

create trigger raffles_id_seq before insert on raffles
    for each row execute procedure raffles_id_seq();
comment on trigger raffles_id_seq on raffles is 'Выполняет одноимённую функцию перед каждой вставкой.';

create function raffles_timestamp_range_intersection() returns trigger as $$
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
$$ language plpgsql;
comment on function raffles_timestamp_range_intersection() is 'Предназначена для одноимённого триггера. Выявляет попытки запустить два или более розыгрышей одновременно на одном боте. Выбрасывает исключение, если хотя бы один розыгрыш пересекается по дате и времени проведения с текущим.';

create trigger raffles_timestamp_range_intersection before insert or update on raffles
    for each row execute procedure raffles_timestamp_range_intersection();
comment on trigger raffles_timestamp_range_intersection on raffles is 'Выполняет одноимённую функцию перед каждой вставкой и обновлением.';

create function raffles_update_too_late() returns trigger as $$
    begin
        if current_timestamp >= old.begin_timestamp then
            raise exception 'UpdateTooLate';
        end if;
        return new;
    end;
$$ language plpgsql;
comment on function raffles_update_too_late() is 'Предназначена для одноимённого триггера. Выявляет попытки изменить запущенный или завершённый розыгрыш. Выбрасывает исключение, если текущее время больше или равно, чем время начала розыгрыша.';

create trigger raffles_update_too_late before update on raffles
    for each row execute procedure raffles_update_too_late();
comment on trigger raffles_update_too_late on raffles is 'Выполняет одноимённую функцию перед каждым обновлением.';

create function raffles_count_increment() returns trigger as $$
    begin
        update
            customers
        set
            draws_count = draws_count + 1
        where
            id = new.customer_id;
        return new;
    end;
$$ language plpgsql;
comment on function raffles_count_increment() is 'Предназначена для одноимённого триггера. Увеличивает количество ликвидных розыгрышей на единицу.';

create trigger raffles_count_increment after insert on raffles
    for each row execute procedure raffles_count_increment();
comment on trigger raffles_count_increment on raffles is 'Выполняет одноимённую функцию после каждой вставки.';

create function raffles_count_decrement() returns trigger as $$
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
$$ language plpgsql;
comment on function raffles_count_decrement() is 'Предназначена для одноимённого триггера. Уменьшает количество ликвидных розыгрышей на единицу только в том случае, если пользователь удаляет розыгрыш, который ещё не начался.';

create trigger raffles_count_decrement after delete on raffles
    for each row execute procedure raffles_count_decrement();
comment on trigger raffles_count_decrement on raffles is 'Выполняет одноимённую функцию после каждого удаления.';

create table tickets (
    customer_id         integer                 not null,
    bot_id              integer                 not null,
    raffle_id           integer                 not null,
    id                  bigint                  not null,
    tg_user_id          bigint                  not null,
    constraint tickets_pkey primary key (customer_id, bot_id, raffle_id, id),
    constraint tickets_raffles_fkey foreign key (customer_id, bot_id, raffle_id) references raffles(customer_id, bot_id, id) on delete cascade
);
comment on table tickets is 'Предназначена для хранения билетов пользователей.';
comment on column tickets.customer_id is 'Уникальный идентификатор владельца бота.';
comment on column tickets.bot_id is 'Уникальный идентификатор бота.';
comment on column tickets.raffle_id is 'Уникальный идентификатор розыгрыша.';
comment on column tickets.id is 'Уникальный идентификатор билета. Подразумевается, что данное поле также является публичным номером билета.';
comment on column tickets.tg_user_id is 'Уникальный идентификатор пользователя Телеграм, которому принадлежит билет.';
comment on constraint tickets_pkey on tickets is 'Составной первичный ключ.';
comment on constraint tickets_raffles_fkey on tickets is 'Составной внешний ключ на таблицу <code>raffles</code>.';

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
                raffle_id = new.raffle_id);
        end if;
        return new;
    end;
$$ language plpgsql;
comment on function tickets_id_seq() is 'Предназначена для одноимённого триггера. Генерирует уникальное значение для столбца <code>id</code>.';

create trigger tickets_id_seq before insert on tickets
    for each row execute procedure tickets_id_seq();
comment on trigger tickets_id_seq on tickets is 'Выполняет одноимённую функцию перед каждой вставкой.';

create function tickets_create(customer_id integer, bot_id integer, raffle_id integer, tg_user_id bigint, count_to_create smallint) returns void as $$
    begin
        for i in 1..count_to_create loop
            insert into tickets (
                customer_id,
                bot_id,
                raffle_id,
                tg_user_id
            ) values (
                tickets_create.customer_id,
                tickets_create.bot_id,
                tickets_create.raffle_id,
                tickets_create.tg_user_id
            );
        end loop;
    end;
$$ language plpgsql;
comment on function tickets_create(customer_id integer, bot_id integer, raffle_id integer, tg_user_id bigint, count_to_create smallint) is 'Предназначена для создания определённого количества билетов для определённого пользователя в определённом розыгрыше.';

create function tickets_remove(customer_id integer, bot_id integer, raffle_id integer, tg_user_id bigint, count_to_remove smallint) returns void as $$
    begin
        delete from
            tickets
        where
            id in (select
                id
            from
                tickets
            where
                tickets.customer_id = tickets_remove.customer_id and
                tickets.bot_id = tickets_remove.bot_id and
                tickets.raffle_id = tickets_remove.raffle_id and
                tickets.tg_user_id = tickets_remove.tg_user_id
            order by
                id
            desc
            limit
                count_to_remove);
    end;
$$ language plpgsql;
comment on function tickets_remove(customer_id integer, bot_id integer, raffle_id integer, tg_user_id bigint, count_to_remove smallint) is 'Предназначена для удаления определённого количества билетов у определённого пользователя в определённом розыгрыше. В первую очередь удаляются самые свежие билеты. Не будет выбрасывать исключений даже при попытке удалить больше билетов, чем есть у данного пользователя.';

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
    constraint raffle_progresses_pkey primary key (customer_id, bot_id, raffle_id, tg_user_id),
    constraint raffle_progresses_tg_users_fkey foreign key (customer_id, bot_id, tg_user_id) references tg_users(customer_id, bot_id, id) on delete cascade
);
comment on table raffle_progresses is 'Предназначена для хранения прогресса розыгрышей.';
comment on column raffle_progresses.customer_id is 'Уникальный идентификатор владельца бота.';
comment on column raffle_progresses.bot_id is 'Уникальный идентификатор бота.';
comment on column raffle_progresses.raffle_id is 'Уникальный идентификатор розыгрыша.';
comment on column raffle_progresses.tg_user_id is 'Уникальный идентификатор пользователя Телеграм.';
comment on column raffle_progresses.latest_daily is 'Дата последнего получения пользователем ежедневного бонуса.';
comment on column raffle_progresses.daily_bonus_duration is 'Количество дней подряд, на протяжении которых пользователь получал ежедневный бонус.';
comment on column raffle_progresses.super_game_duration is 'Количество дней, на протяжении которых пользователь участвовал в супер-игре.';
comment on column raffle_progresses.super_game_stage is 'Стадия супер-игры.';
comment on column raffle_progresses.invites is 'Количество пользователей, приглашённых данным пользователем вне супер-игры.';
comment on column raffle_progresses.super_game_invites is 'Количество пользователей, приглашённых данным пользователем в процессе супер-игры.';
comment on constraint raffle_progresses_pkey on raffle_progresses is 'Составной первичный ключ.';
comment on constraint raffle_progresses_tg_users_fkey on raffle_progresses is 'Составной внешний ключ на таблицу <code>tg_users</code>.';

create function raffle_progresses_latest_daily_update() returns trigger as $$
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
$$ language plpgsql;
comment on function raffle_progresses_latest_daily_update() is 'Предназначена для обновления даты последнего получения пользователем ежедневного бонуса. Если интервал между старой и новой датами превышает ноль суток, проводится сброс стадии супер игры, и количества пользователей, приглашённых в процессе супер-игры. Так же, если интервал между старой и новой датами превышает одни сутки, проводится сброс счётчика ежедневного бонуса.';

create trigger raffle_progresses_latest_daily_update before update on raffle_progresses
    for each row execute procedure raffle_progresses_latest_daily_update();
comment on trigger raffle_progresses_latest_daily_update on raffle_progresses is 'Выполняет одноимённую функцию перед каждым обновлением.';

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
comment on function super_game_to_invite(super_game_duration smallint, super_game_stage smallint) is 'Предназначена для вычисления количества пользователей, которых необходимо пригласить для победы в супер-игре.';

create view raffle_progresses_extends as
    select
        *,
        super_game_to_invite(super_game_duration, super_game_stage)
    from raffle_progresses;
comment on view raffle_progresses_extends is 'Включает в себя все столбцы таблицы <code>raffle_progresses</code>, а также дополнительные столбцы, вычисляемые «на месте». <b>Не рекомендуется к использованию: предпочтительно вызывать функцию <code>super_game_to_invite()</code> при необходимости.</b>';
